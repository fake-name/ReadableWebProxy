
import logging
import logSetup
import multiprocessing
import sys

import rpyc
from rpyc.utils.server import ThreadPoolServer







class FetchInterfaceServer(rpyc.Service):
	def on_connect(self):
		import FetchAgent.manager
		self.mgr = FetchAgent.manager.manager


	def exposed_putJob(self, queuename, job):
		if not queuename in self.mgr.outq:
			with self.mgr.qlock:
				self.mgr.outq[queuename] = multiprocessing.Queue()

		self.mgr.outq[queuename].put(job)

	def exposed_getJob(self, queuename):
		return self.mgr.outq[queuename].get_nowait()




def run_server():
	print("Started.")
	serverLog = logging.getLogger("Main.RPyCServer")
	server = ThreadPoolServer(service=FetchInterfaceServer, port = 12345, hostname='localhost', logger=serverLog, nbThreads=6)
	server.start()



def before_exit():
	print("Caught exit! Exiting")


def initialize_manager():
	import FetchAgent.manager
	mgr = multiprocessing.Manager()
	FetchAgent.manager.manager = mgr.Namespace()


	FetchAgent.manager.manager.qlock = mgr.Lock()
	FetchAgent.manager.manager.outq = {}
	FetchAgent.manager.manager.inq = {}

# import server_reloader


def main():
	logSetup.initLogging()
	initialize_manager()
	print("Preloading cache directories")

	# print("Testing reload")
	# server.tree.tree.reloadTree()
	# print("Starting RPC server")

	run_server()

	# server_reloader.main(
	# 	run_server
	# )

if __name__ == '__main__':
	main()
