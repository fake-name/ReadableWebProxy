

import logging
import logSetup
import multiprocessing
import threading
import pickle
import sys
import queue
import FetchAgent.AmqpInterface

# import rpyc
# rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
# from rpyc.utils.server import ThreadPoolServer



import signal


INTERRUPTS = 0
def build_handler(server):
	def handler(signum=-1, frame=None):
		global INTERRUPTS
		INTERRUPTS += 1
		print('Signal handler called with signal %s for the %s time' % (signum, INTERRUPTS))
		if INTERRUPTS > 2:
			print("Raising due to repeat interrupts")
			raise KeyboardInterrupt
		server.close()
		# server.stop()
	return handler


import gevent.socket as gsocket
from bsonrpc import BSONRpc, ThreadingModel
from bsonrpc import rpc_request, request, service_class
from common.fixed_bsonrpc import Fixed_BSONRpc


@service_class
class FetchInterfaceClass(object):


	def __init__(self):
		self.log = logging.getLogger("Main.RPC-Interface")

		import FetchAgent.manager
		self.mdict = FetchAgent.manager.manager
		self.log.info("Connection")


	def __check_have_queue(self, queuename):
		if not queuename in self.mdict['outq']:
			# self.log.info(self.mdict)
			with self.mdict['qlock']:
				self.mdict['outq'][queuename] = multiprocessing.Queue()
				self.mdict['inq'][queuename] = multiprocessing.Queue()

	@request
	def putJob(self, queuename, job):
		self.__check_have_queue(queuename)
		self.log.info("Putting item in queue %s with size: %s!", queuename, len(job))
		self.mdict['outq'][queuename].put(job)

	@request
	def getJob(self, queuename):
		self.__check_have_queue(queuename)
		self.log.info("Get job call for '%s' -> %s", queuename, self.mdict['inq'][queuename].qsize())
		try:
			return self.mdict['inq'][queuename].get_nowait()
		except queue.Empty:
			return None


	@request
	def getJobNoWait(self, queuename):
		self.__check_have_queue(queuename)
		self.log.info("Get job call for '%s' -> %s", queuename, self.mdict['inq'][queuename].qsize())
		try:
			return self.mdict['inq'][queuename].get_nowait()
		except queue.Empty:
			return None

	@request
	def putRss(self, message):
		self.log.info("Putting rss item with size: %s!", len(message))
		self.mdict['feed_outq'].put(message)

	@request
	def getRss(self):
		self.log.info("Get job call for rss queue -> %s", self.mdict['feed_inq'].qsize())
		try:
			return self.mdict['inq'].get_nowait()
		except queue.Empty:
			return None

	@request
	def checkOk(self):
		return (True, b'wattt\0')



def run_server():
	print("Started.")



	# Quick-and-dirty TCP Server:
	ss = gsocket.socket(gsocket.AF_INET, gsocket.SOCK_STREAM)
	ss.bind(('localhost', 6000))
	ss.listen(10)

	while True:
		s, addr = ss.accept()
		Fixed_BSONRpc(s,
		        FetchInterfaceClass(),
		        client_info=addr,
		        threading_model=ThreadingModel.GEVENT,
		        concurrent_request_handling=ThreadingModel.GEVENT)

def before_exit():
	print("Caught exit! Exiting")



def initialize_manager():
	import FetchAgent.manager
	FetchAgent.manager.manager = {}


	# FetchAgent.manager.manager.qlock = pickle.dumps(mgr.Lock())
	FetchAgent.manager.manager['qlock'] = multiprocessing.Lock()

	print("Manager lock: ", FetchAgent.manager.manager['qlock'])
	FetchAgent.manager.manager['outq'] = {}
	FetchAgent.manager.manager['inq'] = {}

	FetchAgent.manager.manager['feed_outq'] = multiprocessing.Queue()
	FetchAgent.manager.manager['feed_inq'] = multiprocessing.Queue()

	return FetchAgent.manager.manager

def run():
	logSetup.initLogging()


	mtmp = initialize_manager()
	FetchAgent.AmqpInterface.startup_interface(mtmp)
	try:
		run_server()
	except KeyboardInterrupt:
		pass

	FetchAgent.AmqpInterface.shutdown_interface(mtmp)

def main():
	print("Preloading cache directories")

	# print("Testing reload")
	# server.tree.tree.reloadTree()
	# print("Starting RPC server")

	run()

	# import server_reloader

	# server_reloader.main(
	# 	run
	# )

if __name__ == '__main__':
	main()
