
import threading
import traceback
import os.path
import queue
import sys
import time
import common.LogBase as LogBase
import runStatus

import mprpc
import settings



class RemoteJobInterface(LogBase.LoggerMixin):

	loggerPath = "Main.RemoteJobInterface"

	def __init__(self, interfacename):
		self.interfacename = interfacename

		# Execute in self.rpc_client:
		for x in range(99999):
			try:
				self.log.info("Creating rpc_client")
				mp_conf = {"use_bin_type":True}
				self.rpc_client = mprpc.RPCClient(settings.RPC_AGENT_HOST, 4315, pack_params=mp_conf)
				self.log.info("Validating RPC connection")

				# self.rpc_client = self.rpc.get_peer_proxy(timeout=10)
				self.check_ok()
				return
			except AttributeError as e:
				self.log.error("Failed to create RPC interface?")
				if x > 3:
					raise e

			except Exception as e:
				if x > 3:
					raise e

	def __del__(self):
		if hasattr(self, 'rpc_client'):
			try:
				self.rpc_client.close() # Closes the socket 's' also
			except AttributeError:
				pass

	def get_job(self):
		try:
			j = self.rpc_client.call('getJob', self.interfacename)
			return j
		except Exception as e:
			raise e

	def get_job_nowait(self):
		try:
			j = self.rpc_client.call('getJobNoWait', self.interfacename)
			return j
		except Exception as e:
			raise e

	def put_feed_job(self, message):
		assert isinstance(message, (str, bytes, bytearray))
		self.rpc_client.call('putRss', message)

	def put_many_feed_job(self, messages):
		assert isinstance(messages, (list, set))
		self.rpc_client.call('putManyRss', messages)

	def put_job(self, job):
		self.rpc_client.call('putJob', self.interfacename, job)


	def check_ok(self):
		ret, bstr = self.rpc_client.call('checkOk')
		assert ret is True
		assert len(bstr) > 0

		return ret

	def close(self):
		self.rpc_client.close()
		del self.rpc_client


class RemoteFetchInterface(LogBase.LoggerMixin):

	loggerPath = "Main.RemoteFetchInterface"

	def __init__(self):
		# Execute in self.rpc_client:
		for x in range(99999):
			try:
				self.log.info("Creating rpc_client")
				mp_conf = {"use_bin_type" : True}
				self.rpc_client = mprpc.RPCClient(settings.SYNC_RPC_SERVER, 4315, pack_params=mp_conf, timeout=30)
				self.log.info("Validating RPC connection")

				self.check_ok()
				return
			except AttributeError as e:
				self.log.error("Failed to create RPC interface?")
				if x > 3:
					raise e

			except Exception as e:
				if x > 3:
					raise e

	def __del__(self):
		if hasattr(self, 'rpc_client'):
			try:
				self.rpc_client.close() # Closes the socket 's' also
			except AttributeError:
				pass

	def dispatch_request(self, *args, **kwargs):
		try:
			j = self.rpc_client.call('dispatch_request', *args, **kwargs)
			return j
		except Exception as e:
			raise e


	def check_ok(self):
		ret, bstr = self.rpc_client.call('checkOk')
		assert ret is True
		assert len(bstr) > 0

		return ret

	def close(self):
		self.rpc_client.close()
		del self.rpc_client


