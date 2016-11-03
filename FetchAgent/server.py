

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



import zerorpc
import gevent.monkey
import gevent

class FetchInterfaceServer(object):


	def __init__(self):
		self.log = logging.getLogger("Main.RPC-Interface")

		import FetchAgent.manager
		self.mdict = FetchAgent.manager.manager
		self.log.info("Connection")


	def _check_have_queue(self, queuename):
		if not queuename in self.mdict['outq']:
			# self.log.info(self.mdict)
			with self.mdict['qlock']:
				self.mdict['outq'][queuename] = multiprocessing.Queue()
				self.mdict['inq'][queuename] = multiprocessing.Queue()

	def putJob(self, queuename, job):
		self._check_have_queue(queuename)
		self.log.info("Putting item in queue %s with size: %s!", queuename, len(job))
		self.mdict['outq'][queuename].put(job)

	def getJob(self, queuename):
		self._check_have_queue(queuename)
		self.log.info("Get job call for '%s' -> %s", queuename, self.mdict['inq'][queuename].qsize())
		try:
			return self.mdict['inq'][queuename].get_nowait()
		except queue.Empty:
			return None

	def getJobNoWait(self, queuename):
		self._check_have_queue(queuename)
		self.log.info("Get job call for '%s' -> %s", queuename, self.mdict['inq'][queuename].qsize())
		try:
			return self.mdict['inq'][queuename].get_nowait()
		except queue.Empty:
			return None




def run_server():
	print("Started.")
	serverLog = logging.getLogger("Main.RPyCServer")
	server = zerorpc.Server(FetchInterfaceServer())
	server.bind("tcp://127.0.0.1:4242")

	gevent.signal(signal.SIGINT, build_handler(server))

	server.run()




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
