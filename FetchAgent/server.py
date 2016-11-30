

import logging
import threading
import queue
import threading
import pickle
import sys
import queue
import os
import signal
import FetchAgent.AmqpInterface
import logSetup

# import rpyc
# rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
# from rpyc.utils.server import ThreadPoolServer





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
import socket
from bsonrpc import BSONRpc, ThreadingModel
from bsonrpc import rpc_request, request, service_class
from common.fixed_bsonrpc import Fixed_BSONRpc


@service_class
class FetchInterfaceClass(object):


	def __init__(self, interface_dict):
		self.log = logging.getLogger("Main.RPC-Interface")

		self.mdict = interface_dict
		self.log.info("Connection")


	def __check_have_queue(self, queuename):
		if not queuename in self.mdict['outq']:
			with self.mdict['qlock']:
				self.mdict['outq'][queuename] = queue.Queue()
				self.mdict['inq'][queuename] = queue.Queue()

	@request
	def putJob(self, queuename, job):
		self.__check_have_queue(queuename)
		self.log.info("Putting item in queue %s with size: %s (Queue size: %s)!", queuename, len(job), self.mdict['outq'][queuename].qsize())
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
		self.log.info("Putting rss item with size: %s (qsize: %s)!", len(message), self.mdict['feed_outq'].qsize())
		self.mdict['feed_outq'].put(message)

	@request
	def putManyRss(self, messages):
		for message in messages:
			self.log.info("Putting rss item with size: %s!", len(message))
			self.mdict['feed_outq'].put(message)

	@request
	def getRss(self):
		self.log.info("Get job call for rss queue -> %s", self.mdict['feed_inq'].qsize())
		try:
			return self.mdict['feed_inq'].get_nowait()
		except queue.Empty:
			return None

	@request
	def checkOk(self):
		return (True, b'wattt\0')


sock_path = '/tmp/rwp-fetchagent-sock'

def run_server(interface_dict):
	print("Started.")



	# Quick-and-dirty TCP Server:
	ss = gsocket.socket(gsocket.AF_UNIX, gsocket.SOCK_STREAM)
	# ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ss.bind(sock_path)
	ss.listen(100)

	while True:
		s, addr = ss.accept()
		Fixed_BSONRpc(s,
				FetchInterfaceClass(interface_dict),
				client_info                 = addr,
				threading_model             = ThreadingModel.GEVENT,
				concurrent_request_handling = ThreadingModel.GEVENT)


def before_exit():
	print("Caught exit! Exiting")



def initialize_manager(interface_dict):

	# interface_dict.qlock = pickle.dumps(mgr.Lock())
	interface_dict['qlock'] = threading.Lock()

	print("Manager lock: ", interface_dict['qlock'])
	interface_dict['outq'] = {}
	interface_dict['inq'] = {}

	interface_dict['feed_outq'] = queue.Queue()
	interface_dict['feed_inq'] = queue.Queue()


def run():

	interface_dict = {}

	logSetup.initLogging()

	# Make sure the socket does not already exist
	try:
		os.unlink(sock_path)
	except OSError:
		if os.path.exists(sock_path):
			raise

	initialize_manager(interface_dict)
	FetchAgent.AmqpInterface.startup_interface(interface_dict)
	try:
		run_server(interface_dict)
	except KeyboardInterrupt:
		pass

	FetchAgent.AmqpInterface.shutdown_interface(interface_dict)

	os.unlink(sock_path)

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
