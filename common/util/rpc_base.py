import sys
import uuid
import time
import traceback
import queue
import json
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
from common.util import rpc_serialize
from common.util import local_exec
from common.util.remote_base import RpcBaseClass

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

class RpcTimeoutError(RuntimeError):
	pass
class RpcExceptionError(RuntimeError):
	pass

# DO_LOCAL = True
DO_LOCAL = False

class RpcMixin():


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.rpc_interfaces = {}
		self.job_map = {}
		self.job_counter = 0
		self.rpc_timeout_s = 60 * 20

		self.remote_log = logging.getLogger("Main.RPC.Remote")

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

	def put_outbound_callable(self, jobid, serialized, meta={}, call_kwargs={}, early_ack=False, job_unique_id=None):
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
			unique_id      = job_unique_id,
		)

		self.put_outbound_raw(raw_job)



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



	def put_job(self, remote_cls, call_kwargs=None, meta=None, early_ack=False, job_unique_id=None):

		if call_kwargs is None:
			call_kwargs = {}

		if not meta:
			meta = {}

		jid = str(uuid.uuid4())

		if 'drain' in sys.argv:
			print("Consuming replies only")
			self.check_open_rpc_interface()
		else:
			scls = rpc_serialize.serialize_class(remote_cls)
			# print("Putting job:", jid, call_kwargs)
			self.put_outbound_callable(jid, scls, call_kwargs=call_kwargs, meta=meta, early_ack=early_ack, job_unique_id=job_unique_id)

		return jid


	def __blocking_dispatch_call_local(self, remote_cls, call_kwargs, meta=None, expect_partials=False):
		self.log.info("Dispatching new callable job to local executor")

		print("Kwargs:", call_kwargs)
		scls = rpc_serialize.serialize_class(remote_cls)
		call_kwargs_out = {'code_struct' : scls}
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


		print(local_exec)
		print(dir(local_exec))

		jid = self.job_counter
		self.job_counter += 1

		raw_job = buildjob(
			module         = 'RemoteExec',
			call           = 'callCode',
			dispatchKey    = "rwp-rpc-system",
			jobid          = jid,
			kwargs         = call_kwargs_out,
			additionalData = meta,
			postDelay      = 0,
			early_ack      = False,
			serialize      = self.pluginName,
			unique_id      = None,
		)

		rpc_interface = common.get_rpyc.RemoteFetchInterface()
		rpc_interface.check_ok()
		ret = rpc_interface.dispatch_request(raw_job)
		rpc_interface.close()

		ret['jobid'] = jid

		ret = self.process_response_items([jid], expect_partials, preload_rets=[ret])
		if not expect_partials:
			ret = next(ret)
		return ret


	def __blocking_dispatch_call_remote(self, remote_cls, call_kwargs, meta=None, expect_partials=False, job_unique_id=None):



		jobid = self.put_job(remote_cls, call_kwargs, meta, job_unique_id=job_unique_id)
		ret = self.process_response_items([jobid], expect_partials)
		if not expect_partials:
			ret = next(ret)
		return ret


	def blocking_dispatch_call(self, remote_cls, call_kwargs, meta=None, expect_partials=False, local=DO_LOCAL, job_unique_id=None):
		if local:
			return self.__blocking_dispatch_call_local(remote_cls=remote_cls, call_kwargs=call_kwargs, meta=meta, expect_partials=expect_partials)
		else:
			return self.__blocking_dispatch_call_remote(remote_cls=remote_cls, call_kwargs=call_kwargs, meta=meta, expect_partials=expect_partials, job_unique_id=job_unique_id)


	def pprint_resp(self, resp):
		if len(resp) == 2:
			logmsg, response_data = resp
			self.print_remote_log(logmsg)
		for line in pprint.pformat(resp).split("\n"):
			self.log.info(line)
		if 'traceback' in resp:
			if isinstance(resp['traceback'], str):
				trace_arr = resp['traceback'].split("\n")
			else:
				trace_arr = resp['traceback']

			for line in trace_arr:
				self.log.error(line)

	def print_remote_log(self, log_lines, debug=False):
		calls = {
				"[DEBUG] ->"    : self.remote_log.debug if debug else None,
				"[INFO] ->"     : self.remote_log.info,
				"[ERROR] ->"    : self.remote_log.error,
				"[CRITICAL] ->" : self.remote_log.critical,
				"[WARNING] ->"  : self.remote_log.warning,
			}

		for line in log_lines:
			for key, log_call in calls.items():
				if key in line and log_call:
					log_call(line)


	def process_response_items(self, jobids, preload_rets = [], timeout=None):
		self.log.info("Waiting for remote response (preloaded: %s)", len(preload_rets) if preload_rets else "None")

		if not timeout:
			timeout = self.rpc_timeout_s

		assert isinstance(jobids, list)

		while timeout or preload_rets:
			timeout -= 1
			if preload_rets:
				self.log.info("Have preloaded item. Using.")
				ret = preload_rets.pop(0)
			else:
				ret = self.process_responses()

			if ret:
				if 'ret' in ret:
					if len(ret['ret']) == 2:
						self.print_remote_log(ret['ret'][0])

						if 'partial' in ret and ret['partial']:
							timeout = self.rpc_timeout_s
							yield ret, ret['ret'][1]
						else:
							yield ret, ret['ret'][1]
							if 'jobid' in ret and ret['jobid'] in jobids:
								jobids.remove(ret['jobid'])
								self.log.info("Last partial received for job %s, %s remaining.", ret['jobid'], len(jobids))

								if not jobids:
									return
							else:
								if 'jobid' in ret:
									self.log.info("Received completed job response from a previous session (%s, waiting for %s, have: %s)?",
										ret['jobid'], jobids, ret['jobid'] in jobids)
								else:
									self.log.error("Response that's not partial, and yet has no jobid?")


					else:
						self.pprint_resp(ret)
						raise RuntimeError("Response not of length 2 (%s, %s)!" % (len(ret), len(ret['ret']) == 2))
				else:
					with open('rerr-{}.json'.format(time.time()), 'w', encoding='utf-8') as fp:
						fp.write(json.dumps(ret, indent=4, sort_keys=True))
					self.pprint_resp(ret)
					self.log.error("RPC Call has no ret value. Probably encountered a remote exception: %s", ret)

			time.sleep(1)
			print("\r`fetch_and_flush` sleeping for {} ({} items remaining)\r".format(str((timeout)).rjust(7), len(jobids)), end='', flush=True)

		raise RpcTimeoutError("No RPC Response within timeout period (%s sec)" % self.rpc_timeout_s)


class RpcTestClass(RpcBaseClass):
	logname = "Main.RemoteExec.TestClass"

	def _go(self, partial_resp_interface, lock_interface, param_1, param_2):
		print("%s, %s" % (param_1, param_2))
		self.log.info("%s, %s", param_1, param_2)
		self.log.info("WG: %s", self.wg)
		self.log.info("partial_resp_interface: %s", partial_resp_interface)
		self.log.info("lock_interface: %s", lock_interface)
		self.log.info("WG.twocaptcha_api_key: %s", self.wg.twocaptcha_api_key)
		self.log.info("WG.anticaptcha_api_key: %s", self.wg.anticaptcha_api_key)
		self.log.info("lock_interface dir: %s", dir(lock_interface))
		self.log.info("lock_interface seen: %s", lock_interface.get_seen())

		return None

class TestClass(common.LogBase.LoggerMixin, RpcMixin):
	loggerPath = "Main.RPC-Test-Class"
	pluginName = "RpcGet"


def test():
	print("Test")
	instance = TestClass()
	print(instance)

	instance.blocking_dispatch_call(remote_cls=RpcTestClass, call_kwargs={"param_1" : "Val 1", "param_2": "Val 2"})




if __name__ == '__main__':
	import logSetup
	logSetup.initLogging()
	test()



