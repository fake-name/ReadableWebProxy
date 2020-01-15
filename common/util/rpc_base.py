import sys
import uuid
import time
import traceback
import queue
import datetime
import mprpc
import logging
import socket
import dill
import pprint
import threading
import multiprocessing
import os


import common.LogBase
import common.get_rpyc
from WebMirror.JobUtils import buildjob

from settings import settings

########################################################################################################################
#
#	##     ##    ###    #### ##    ##     ######  ##          ###     ######   ######
#	###   ###   ## ##    ##  ###   ##    ##    ## ##         ## ##   ##    ## ##    ##
#	#### ####  ##   ##   ##  ####  ##    ##       ##        ##   ##  ##       ##
#	## ### ## ##     ##  ##  ## ## ##    ##       ##       ##     ##  ######   ######
#	##     ## #########  ##  ##  ####    ##       ##       #########       ##       ##
#	##     ## ##     ##  ##  ##   ###    ##    ## ##       ##     ## ##    ## ##    ##
#	##     ## ##     ## #### ##    ##     ######  ######## ##     ##  ######   ######
#
########################################################################################################################


DO_LOCAL = True

class RpcMixin():


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.rpc_interfaces = {}
		self.job_map = {}
		self.job_counter = 0

		self.check_open_rpc_interface()
		self.log.info("RPC Interface initialized")



	@property
	def rpc_interface(self):
		'''
		Create a unique RPC interface per-thread, and
		don't share them.
		'''

		threadName = threading.current_thread().name
		procName   = multiprocessing.current_process().name

		thread_key = "{} - {}".format(threadName, procName)

		if thread_key not in self.rpc_interfaces:
			self.rpc_interfaces[thread_key] = common.get_rpyc.RemoteJobInterface("RWP-RPC-Fetcher")

		return self.rpc_interfaces[thread_key]

	def close_rpc_interface(self):
		threadName = threading.current_thread().name
		procName   = multiprocessing.current_process().name

		thread_key = "{} - {}".format(threadName, procName)

		if thread_key in self.rpc_interfaces:
			self.rpc_interfaces.pop(thread_key)
		else:
			self.log.warning("Closing RPC interface from a thread that hasn't opened it!")



	def put_outbound_raw(self, raw_job):
		# Recycle the rpc interface if it ded
		errors = 0
		while 1:
			try:
				self.rpc_interface.put_job(raw_job)
				return
			except TypeError:
				self.check_open_rpc_interface()
			except KeyError:
				self.check_open_rpc_interface()
			except BrokenPipeError:
				self.check_open_rpc_interface()
			except Exception as e:
				self.check_open_rpc_interface()
				errors += 1
				if errors > 5:
					raise e


	def put_outbound_fetch_job(self, jobid, joburl):
		self.log.info("Dispatching new fetch job")
		raw_job = buildjob(
			module         = 'WebRequest',
			call           = 'getItem',
			dispatchKey    = "rwp-rpc-system",
			jobid          = jobid,
			args           = [joburl],
			kwargs         = {},
			additionalData = {'mode' : 'fetch'},
			postDelay      = 0
		)

		self.put_outbound_raw(raw_job)

	def put_outbound_callable(self, jobid, serialized, meta={}, call_kwargs={}, early_ack=False):
		self.log.info("Dispatching new callable job")
		call_kwargs_out = {'code_struct' : serialized}
		for key, value in call_kwargs.items():
			call_kwargs_out[key] = value

		raw_job = buildjob(
			module         = 'RemoteExec',
			call           = 'callCode',
			dispatchKey    = "rwp-rpc-system",
			jobid          = jobid,
			kwargs         = call_kwargs_out,
			additionalData = meta,
			postDelay      = 0,
			early_ack      = early_ack,
			serialize      = self.pluginName,

		)

		self.put_outbound_raw(raw_job)

	def serialize_class(self, tgt_class, exec_method='go'):
		ret = {
			'source'      : dill.source.getsource(tgt_class),
			'callname'    : tgt_class.__name__,
			'exec_method' : exec_method,
		}
		return ret

	def deserialize_class(self, class_blob):
		assert 'source'      in class_blob
		assert 'callname'     in class_blob
		assert 'exec_method' in class_blob

		code = compile(class_blob['source'], "no filename", "exec")
		exec(code)
		cls_def = locals()[class_blob['callname']]
		# This call relies on the source that was exec()ed having defined the class
		# that will now be unserialized.
		return cls_def, class_blob['exec_method']




	def process_responses(self):
		# Something in the RPC stuff is resulting in a typeerror I don't quite
		# understand the source of. anyways, if that happens, just reset the RPC interface.
		try:
			return self.rpc_interface.get_job()
		except queue.Empty:
			return None

		except TypeError:
			self.check_open_rpc_interface()
			return None
		except socket.timeout:
			self.check_open_rpc_interface()
			return None
		except KeyError:
			self.check_open_rpc_interface()
			return None


	def check_open_rpc_interface(self):

		try:
			if self.rpc_interface.check_ok():
				return


		except Exception:
			self.log.error("Failure when probing RPC interface")
			for line in traceback.format_exc().split("\n"):
				self.log.error(line)
			try:
				self.rpc_interface.close()
				self.log.warning("Closed interface due to connection exception.")
			except Exception:
				self.log.error("Failure when closing errored RPC interface")
				for line in traceback.format_exc().split("\n"):
					self.log.error(line)
			self.close_rpc_interface()
			self.rpc_interface.check_ok()



	def put_job(self, remote_cls, call_kwargs=None, meta=None, early_ack=False):

		if call_kwargs is None:
			call_kwargs = {}

		if not meta:
			meta = {}

		jid = str(uuid.uuid4())

		if 'drain' in sys.argv:
			print("Consuming replies only")
			self.check_open_rpc_interface()
		else:
			scls = self.serialize_class(remote_cls)
			# print("Putting job:", jid, call_kwargs)
			self.put_outbound_callable(jid, scls, call_kwargs=call_kwargs, meta=meta, early_ack=early_ack)

		return jid


	def __blocking_dispatch_call_local(self, remote_cls, call_kwargs, meta=None, expect_partials=False):
		self.log.info("Dispatching new callable job to local executor")

		print("Kwargs:", call_kwargs)
		call_kwargs_out = {}
		# call_kwargs_out = {'code_struct' : serialized}
		for key, value in call_kwargs.items():
			call_kwargs_out[key] = value
		# job = {
		# 		'call'                 : 'callCode',
		# 		'module'               : 'RemoteExec',
		# 		'args'                 : (),
		# 		'kwargs'               : call_kwargs_out,
		# 		'extradat'             : meta,
		# 		'dispatch_key'         : "rpc-system",
		# 		'response_routing_key' : 'response'
		# 	}

		scls = self.serialize_class(remote_cls)

		instance = local_exec.PluginInterface_RemoteExec()
		resp_tup = instance.call_code(code_struct=scls, **call_kwargs_out)
		jid = self.job_counter
		self.job_counter += 1
		cont_proxy = {
			'jobid' : jid,
			'ret'   : resp_tup
		}

		ret = self.process_response_items([jid], expect_partials, preload_rets=[cont_proxy])
		if not expect_partials:
			ret = next(ret)
		return ret


	def __blocking_dispatch_call_remote(self, remote_cls, call_kwargs, meta=None, expect_partials=False):



		jobid = self.put_job(remote_cls, call_kwargs, meta)
		ret = self.process_response_items([jobid], expect_partials)
		if not expect_partials:
			ret = next(ret)
		return ret


	def blocking_dispatch_call(self, remote_cls, call_kwargs, meta=None, expect_partials=False, local=DO_LOCAL):
		if local:
			return self.__blocking_dispatch_call_local(remote_cls=remote_cls, call_kwargs=call_kwargs, meta=meta, expect_partials=expect_partials)
		else:
			return self.__blocking_dispatch_call_remote(remote_cls=remote_cls, call_kwargs=call_kwargs, meta=meta, expect_partials=expect_partials)


