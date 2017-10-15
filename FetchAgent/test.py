
import logging
import queue
import pickle
import logSetup
import multiprocessing
import sys

import rpyc
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
rpyc.core.protocol.DEFAULT_CONFIG['import_custom_exceptions'] = True
rpyc.core.protocol.DEFAULT_CONFIG['instantiate_oldstyle_exceptions'] = True
import rpyc.core.vinegar

import time

from WebMirror.JobDispatcher import buildjob



def main():
	logSetup.initLogging()

	remote = rpyc.connect("localhost", 12345, config = rpyc.core.protocol.DEFAULT_CONFIG)


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

	print(remote)
	print(remote.root.putJob('wat', raw_job))

	while 1:
		try:
			j = remote.root.getJob("wat")
			print("Got job!")
		except queue.Empty:
			time.sleep(1)
			print("No message")
		except rpyc.core.vinegar.GenericException as e:
			# this is horrible
			if 'queue.Empty' in rpyc.core.vinegar._generic_exceptions_cache:
				if isinstance(e, rpyc.core.vinegar._generic_exceptions_cache['queue.Empty']):
					print("Empty exception")
					continue

			print("type", type(e))
			print("instance", issubclass(type(e), queue.Empty))

			import inspect
			print(inspect.getmro(type(e)))
			# extp = rpyc.core.vinegar._get_exception_class(queue.Empty)
			# print(extp)
			# print("instance", isinstance(e, extp))
			# print("instance", isinstance(type(e), extp))
			# print("type", type(extp()))
			fakemodule = {"__module__" : "%s/%s" % ("rpyc.core.vinegar", "queue")}
			extp = type("queue.Empty", (rpyc.core.vinegar.GenericException,), fakemodule)
			print(extp)
			print(isinstance(e, extp))
			print(isinstance(e, rpyc.core.vinegar.GenericException))


			print(rpyc.core.vinegar._generic_exceptions_cache )
			raise e

	remote.close()
if __name__ == '__main__':
	main()
