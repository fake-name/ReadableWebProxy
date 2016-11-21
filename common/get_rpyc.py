
import runStatus
import threading
import traceback
import queue
import sys
import time
import common.LogBase as LogBase

# import zerorpc


import socket
from bsonrpc import BatchBuilder, BSONRpc
from bsonrpc import request, notification, service_class

from common.fixed_bsonrpc import Fixed_BSONRpc


class RemoteJobInterface(LogBase.LoggerMixin):

	loggerPath = "Main.RemoteJobInterface"

	def __init__(self, interfacename):
		self.interfacename = interfacename


		# Cut-the-corners TCP Client:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(('localhost', 6000))

		self.rpc = Fixed_BSONRpc(s)
		self.rpc_client = self.rpc.get_peer_proxy(timeout=10)
		# Execute in self.rpc_client:

		self.check_ok()

	def __del__(self):
		self.rpc.close() # Closes the socket 's' also

	def get_job(self):
		try:
			j = self.rpc_client.getJob(self.interfacename)
			return j
		except Exception as e:
			raise e

	def get_job_nowait(self):
		try:
			j = self.rpc_client.getJobNoWait(self.interfacename)
			return j
		except Exception as e:
			raise e

	def put_feed_job(self, message):
		assert isinstance(message, (str, bytes, bytearray))
		self.rpc_client.putRss(message)

	def put_many_feed_job(self, messages):
		assert isinstance(messages, (list, set))
		self.rpc_client.putManyRss(messages)

	def put_job(self, job):
		self.rpc_client.putJob(self.interfacename, job)


	def check_ok(self):
		ret, bstr = self.rpc_client.checkOk()
		assert ret is True

	def close(self):
		self.rpc_client.close()



def main():
	import logSetup
	from WebMirror.NewJobQueue import buildjob
	logSetup.initLogging()

	raw_job = buildjob(
		module         = 'WebRequest',
		call           = 'getItem',
		dispatchKey    = "fetcher",
		jobid          = -1,
		args           = ['http://www.google.com'],
		kwargs         = {},
		additionalData = {'mode' : 'fetch'},
		postDelay      = 0
	)

	rint = RemoteJobInterface("wat")
	print(rint.put_job(raw_job))
	print(rint)
	while 1:
		try:
			j = rint.get_job()
			if j:
				print("Got job!", j)
		except queue.Empty:
			time.sleep(1)
			print("No message")
		except Exception as e:
		# except pyjsonrpc.JsonRpcError as err:
			print("type", type(e))
			print("instance", issubclass(type(e), queue.Empty))

			import inspect
			print(inspect.getmro(type(e)))

			raise e

	remote.close()
if __name__ == '__main__':
	main()

