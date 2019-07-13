

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import time
import queue
import pprint
import common.get_rpyc
import WebMirror.JobDispatcher
from WebMirror.JobUtils import buildjob

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

	raw_job_2 = buildjob(
		module         = 'WebRequest',
		call           = 'getHeadTitleChromium',
		dispatchKey    = "lolwattttt",
		jobid          = "lolwat",
		args           = [],
		kwargs         = {'url' : 'http://www.google.com', 'referrer' : 'http://www.goat.com'},
		additionalData = {'herp' : 'derp'},
		postDelay      = 0
	)

	raw_job_3 = buildjob(
		module         = 'WebRequest',
		call           = 'getItemChromium',
		dispatchKey    = "lolwattttt",
		jobid          = "lolwat",
		args           = [],
		kwargs         = {'itemUrl' : 'http://www.google.com'},
		additionalData = {'herp' : 'derp'},
		postDelay      = 0
	)

	raw_job_4 = buildjob(
		module         = 'WebRequest',
		call           = 'getItem',
		dispatchKey    = "lolwattttt",
		jobid          = "lolwat",
		args           = [],
		kwargs         = {'itemUrl' : 'http://imgsv.imaging.nikon.com/lineup/dslr/d600/img/sample01/img_01_l.jpg'},
		additionalData = {'herp' : 'derp'},
		postDelay      = 0
	)

	# rpc_interface.put_job(raw_job_1)
	rpc_interface.put_job(raw_job_2)
	rpc_interface.put_job(raw_job_3)
	rpc_interface.put_job(raw_job_4)

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


def exposed_test_local_rpc_fetch():
	'''
	Run a test-fetch with the chromium remote
	rendering system

	'''
	print("Chromium Test")

	rpc_interface = common.get_rpyc.RemoteFetchInterface()
	rpc_interface.check_ok()

	print("RPC:", rpc_interface)

	print("Dispatching job engine")

	# raw_job1 = buildjob(
	# 	module                 = 'WebRequest',
	# 	call                   = 'getItem',
	# 	dispatchKey            = "fetcher",
	# 	jobid                  = -1,
	# 	args                   = ['http://raptorjes.us/'],
	# 	kwargs                 = {},
	# 	additionalData         = {'mode' : 'fetch'},
	# 	postDelay              = 0,
	# )

	# ret1 = rpc_interface.dispatch_request(raw_job1)

	# print("Return 1: ")
	# pprint.pprint(ret1)


	# rpc_interface.check_ok()
	# raw_job2 = buildjob(
	# 	module                 = 'WebRequest',
	# 	call                   = 'getItem',
	# 	dispatchKey            = "fetcher",
	# 	jobid                  = -1,
	# 	args                   = ['http://www.asdasdasdasdasdgoogle.com'],
	# 	kwargs                 = {},
	# 	additionalData         = {'mode' : 'fetch'},
	# 	postDelay              = 0,
	# )

	# ret2 = rpc_interface.dispatch_request(raw_job2)

	# print("Return 2: ")
	# pprint.pprint(ret2)


	rpc_interface.check_ok()
	raw_job3 = WebMirror.JobUtils.buildjob(
		module                 = 'WebRequest',
		call                   = 'chromiumGetRenderedItem',
		dispatchKey            = "fetcher",
		jobid                  = -1,
		args                   = ["http://raptorjes.us/"],
		kwargs                 = {},
		additionalData         = {'mode' : 'fetch'},
		postDelay              = 0,
	)
	ret3 = rpc_interface.dispatch_request(raw_job3)


	print("Return 3: ")
	pprint.pprint(ret3)

	rpc_interface.check_ok()
	raw_job4 = WebMirror.JobUtils.buildjob(
		module                 = 'WebRequest',
		call                   = 'chromiumGetRenderedItem',
		dispatchKey            = "fetcher",
		jobid                  = -1,
		args                   = ["http://raptorjes.us//raptorjesus.jpg"],
		kwargs                 = {},
		additionalData         = {'mode' : 'fetch'},
		postDelay              = 0,
	)
	ret4 = rpc_interface.dispatch_request(raw_job4)


	print("Return 4: ")
	pprint.pprint(ret4)

	rpc_interface.close()
