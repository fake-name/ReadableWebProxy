
import runStatus
import threading
import traceback
import queue
import sys
import time
import common.LogBase as LogBase

# import rpyc
# rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
# import rpyc.core.vinegar


# class RemoteJobInterface(LogBase.LoggerMixin):

# 	loggerPath = "Main.RemoteJobInterface"

# 	def __init__(self, interfacename):
# 		self.interfacename = interfacename
# 		self.remote = rpyc.connect("localhost", 12345, config = rpyc.core.protocol.DEFAULT_CONFIG)

# 	def get_job(self, wait=1):
# 		try:
# 			j = self.remote.root.getJob(self.interfacename, wait=wait)
# 			return j
# 		except rpyc.core.vinegar.GenericException as e:
# 			# this is horrible, but there seems to be no other way to determine non-new-style
# 			# exception types correctly.
# 			if 'queue.Empty' in rpyc.core.vinegar._generic_exceptions_cache:
# 				if isinstance(e, rpyc.core.vinegar._generic_exceptions_cache['queue.Empty']):
# 					return None
# 			if 'KeyError' in rpyc.core.vinegar._generic_exceptions_cache:
# 				if isinstance(e, rpyc.core.vinegar._generic_exceptions_cache['KeyError']):
# 					raise KeyError
# 			else:
# 				raise e

# 	def get_job_nowait(self):
# 		try:
# 			j = self.remote.root.getJobNoWait(self.interfacename)
# 			return j
# 		except rpyc.core.vinegar.GenericException as e:
# 			# this is horrible, but there seems to be no other way to determine non-new-style
# 			# exception types correctly.
# 			if 'queue.Empty' in rpyc.core.vinegar._generic_exceptions_cache:
# 				if isinstance(e, rpyc.core.vinegar._generic_exceptions_cache['queue.Empty']):
# 					return None
# 			if 'KeyError' in rpyc.core.vinegar._generic_exceptions_cache:
# 				if isinstance(e, rpyc.core.vinegar._generic_exceptions_cache['KeyError']):
# 					raise KeyError
# 			else:
# 				raise e



# 	def put_job(self, job):
# 		self.remote.root.putJob(self.interfacename, job)


# 	def close(self):
# 		self.remote.close()


import zerorpc

class RemoteJobInterface(LogBase.LoggerMixin):

	loggerPath = "Main.RemoteJobInterface"

	def __init__(self, interfacename):
		self.interfacename = interfacename

		self.remote = zerorpc.Client()
		self.remote.connect("tcp://127.0.0.1:4242")

	def get_job(self):
		try:
			j = self.remote.getJob(self.interfacename)
			return j
		except zerorpc.RemoteError as e:
			if e.name == "Empty":
				raise queue.Empty
		except Exception as e:
			raise e

	def get_job_nowait(self):
		try:
			j = self.remote.getJobNoWait(self.interfacename)
			return j

		except zerorpc.RemoteError as e:
			if e.name == "Empty":
				raise queue.Empty
		except Exception as e:
			raise e



	def put_job(self, job):
		self.remote.putJob(self.interfacename, job)


	def close(self):
		self.remote.close()



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
	# print(rint.put_job(raw_job))
	print(rint)
	while 1:
		try:
			j = rint.get_job()
			print("Got job!")
		except queue.Empty:
			time.sleep(1)
			print("No message")
		# except Exception as e:
		except zerorpc.RemoteError as e:
			print("type", type(e))
			print("instance", issubclass(type(e), queue.Empty))

			import inspect
			print(inspect.getmro(type(e)))
			print("name: ", e.name)
			print("name: ", e.name == "Empty")
			print("human_msg: ", e.msg )
			print("traceback : ", e.traceback )

			raise e

	remote.close()
if __name__ == '__main__':
	main()

