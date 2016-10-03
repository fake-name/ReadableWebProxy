
import runStatus
import threading
import traceback
import queue
import sys
import common.LogBase as LogBase

import rpyc
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
import rpyc.core.vinegar


class RemoteJobInterface(LogBase.LoggerMixin):

	loggerPath = "Main.RemoteJobInterface"

	def __init__(self, interfacename):
		self.interfacename = interfacename
		self.remote = rpyc.connect("localhost", 12345, config = rpyc.core.protocol.DEFAULT_CONFIG)

	def get_job(self, wait=1):
		try:
			j = self.remote.root.getJob(self.interfacename, wait=wait)
			return j
		except rpyc.core.vinegar.GenericException as e:
			# this is horrible, but there seems to be no other way to determine non-new-style
			# exception types correctly.
			if 'queue.Empty' in rpyc.core.vinegar._generic_exceptions_cache:
				if isinstance(e, rpyc.core.vinegar._generic_exceptions_cache['queue.Empty']):
					return None
			if 'KeyError' in rpyc.core.vinegar._generic_exceptions_cache:
				if isinstance(e, rpyc.core.vinegar._generic_exceptions_cache['KeyError']):
					raise KeyError
			else:
				raise e

	def get_job_nowait(self):
		try:
			j = self.remote.root.getJobNoWait(self.interfacename)
			return j
		except rpyc.core.vinegar.GenericException as e:
			# this is horrible, but there seems to be no other way to determine non-new-style
			# exception types correctly.
			if 'queue.Empty' in rpyc.core.vinegar._generic_exceptions_cache:
				if isinstance(e, rpyc.core.vinegar._generic_exceptions_cache['queue.Empty']):
					return None
			if 'KeyError' in rpyc.core.vinegar._generic_exceptions_cache:
				if isinstance(e, rpyc.core.vinegar._generic_exceptions_cache['KeyError']):
					raise KeyError
			else:
				raise e



	def put_job(self, job):
		self.remote.root.putJob(self.interfacename, job)


	def close(self):
		self.remote.close()