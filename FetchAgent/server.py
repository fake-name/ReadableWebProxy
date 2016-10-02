
import rpyc
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True

import logging
import logSetup
import multiprocessing
import threading
import pickle
import sys
import queue
import FetchAgent.AmqpInterface

from rpyc.utils.server import ThreadPoolServer







class FetchInterfaceServer(rpyc.Service):
	threadLocal = threading.local()

	def on_connect(self):
		self.threadLocal.log = logging.getLogger("Main.RPC-Interface")

		import FetchAgent.manager
		self.mdict = FetchAgent.manager.manager
		self.threadLocal.log.info("Connection")

	def on_disconnect(self):
		self.threadLocal.log.info("Disconnect!")

	def exposed_putJob(self, queuename, job):

		if not queuename in self.mdict['outq']:
			print(self.mdict)
			with self.mdict['qlock']:
				self.mdict['outq'][queuename] = multiprocessing.Queue()
				self.mdict['inq'][queuename] = multiprocessing.Queue()

		print("Putting item in queue!", queuename, job)
		self.mdict['outq'][queuename].put(job)

	def exposed_getJob(self, queuename, wait=1):
		print("Get job call for '%s' -> %s" % (queuename, self.mdict['inq'][queuename].qsize()))
		return self.mdict['inq'][queuename].get(timeout=wait)

	def exposed_getJobNoWait(self, queuename):
		print("Get job call for '%s' -> %s" % (queuename, self.mdict['inq'][queuename].qsize()))
		return self.mdict['inq'][queuename].get_nowait()




def run_server():
	print("Started.")
	serverLog = logging.getLogger("Main.RPyCServer")
	server = ThreadPoolServer(
		service=FetchInterfaceServer,
		port = 12345,
		hostname='localhost',
		logger=serverLog,
		nbThreads=6,
		protocol_config = rpyc.core.protocol.DEFAULT_CONFIG)
	server.start()



def before_exit():
	print("Caught exit! Exiting")



def initialize_manager():
	import FetchAgent.manager
	# mgr = multiprocessing.Manager()
	FetchAgent.manager.manager = {}


	# FetchAgent.manager.manager.qlock = pickle.dumps(mgr.Lock())
	FetchAgent.manager.manager['qlock'] = multiprocessing.Lock()

	print("Manager lock: ", FetchAgent.manager.manager['qlock'])
	FetchAgent.manager.manager['outq'] = {}
	FetchAgent.manager.manager['inq'] = {}

	return FetchAgent.manager.manager

def run():
	logSetup.initLogging()


	mtmp = initialize_manager()
	FetchAgent.AmqpInterface.startup_interface(mtmp)

	run_server()

	FetchAgent.AmqpInterface.shutdown_interface(mtmp)

def main():
	print("Preloading cache directories")

	# print("Testing reload")
	# server.tree.tree.reloadTree()
	# print("Starting RPC server")

	import server_reloader

	server_reloader.main(
		run
	)

if __name__ == '__main__':
	main()
