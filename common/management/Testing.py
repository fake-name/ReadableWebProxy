

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import time
import queue
import pprint
import common.get_rpyc
import WebMirror.JobDispatcher

def dump_response(resp):
	pprint.pprint(resp)
	if 'traceback' in resp:
		print()
		print("Exception!")
		for line in resp['traceback']:
			print(line)

def exposed_test_chromium_fetch():
	'''
	Run a test-fetch with the chromium remote
	rendering system

	'''
	print("Chromium Test")

	rpc_interface = common.get_rpyc.RemoteJobInterface("TestInterface")
	rpc_interface.check_ok()
	print("RPC:", rpc_interface)

	print("Dispatching job engine")

	raw_job_1 = WebMirror.JobDispatcher.buildjob(
		module         = 'NUWebRequest',
		call           = 'getHeadTitlePhantomJS',
		dispatchKey    = "lolwattttt",
		jobid          = "lolwat",
		args           = ['http://www.google.com', 'http://www.goat.com'],
		kwargs         = {},
		additionalData = {'herp' : 'derp'},
		postDelay      = 0
	)
	raw_job_2 = WebMirror.JobDispatcher.buildjob(
		module         = 'WebRequest',
		call           = 'getHeadTitleChromium',
		dispatchKey    = "lolwattttt",
		jobid          = "lolwat",
		args           = [],
		kwargs         = {'url' : 'http://www.google.com', 'referrer' : 'http://www.goat.com'},
		additionalData = {'herp' : 'derp'},
		postDelay      = 0
	)

	rpc_interface.put_job(raw_job_1)
	rpc_interface.put_job(raw_job_2)

	for _ in range(60 * 15):

		try:
			tmp = rpc_interface.get_job()
			if tmp:
				print("response!")
				dump_response(tmp)
			else:
				print("No tmp:", tmp)
				time.sleep(1)
		except queue.Empty:
			time.sleep(1)


