

import logging
import threading
import queue
import threading
import pickle
import sys
import queue
import os
import signal
from gevent.server import StreamServer
import FetchAgent2.MessageProcessor
import traceback
import logSetup
import mprpc
import gevent.monkey
import gevent

# from graphitesend import graphitesend
import statsd

import settings
import time

# import rpyc
# rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
# from rpyc.utils.server import ThreadPoolServer





INTERRUPTS = 0

TO_EXIT = []


def build_mprpc_handler(server):
	global TO_EXIT
	TO_EXIT.append(server)

	def handler(signum=-1, frame=None):
		global INTERRUPTS
		INTERRUPTS += 1
		print('Signal handler called with signal %s for the %s time' % (signum, INTERRUPTS))
		if INTERRUPTS > 2:
			print("Raising due to repeat interrupts")
			raise KeyboardInterrupt
		for server in TO_EXIT:
			server.close()
	return handler

def base_abort():
	print("Low level keyboard interrupt")
	for server in TO_EXIT:
		server.close()


class FetchInterfaceClass(mprpc.RPCServer):


	def __init__(self, interface_dict, rpc_prefix):

		mp_conf = {"use_bin_type":True}
		super().__init__(pack_params=mp_conf)

		self.log = logging.getLogger("Main.{}-Interface".format(rpc_prefix))
		self.mdict = interface_dict
		self.log.info("Connection")



	def __check_have_queue(self, queuename):
		if not queuename in self.mdict['outq']:
			with self.mdict['qlock']:
				self.mdict['outq'][queuename] = queue.Queue()
				self.mdict['inq'][queuename] = queue.Queue()

	def __check_rss_queue(self, queuename):
		if not queuename in self.mdict['feed_outq']:
			with self.mdict['qlock']:
				self.mdict['feed_outq'][queuename] = queue.Queue()
				self.mdict['feed_inq'][queuename] = queue.Queue()

	def putJob(self, queuename, job):
		self.__check_have_queue(queuename)
		self.log.info("Putting item in queue %s with size: %s (Queue size: %s)!", queuename, len(job), self.mdict['outq'][queuename].qsize())
		self.mdict['outq'][queuename].put(job)

	def getJob(self, queuename):
		self.__check_have_queue(queuename)
		self.log.info("Get job call for '%s' -> %s", queuename, self.mdict['inq'][queuename].qsize())
		try:
			tmp = self.mdict['inq'][queuename].get_nowait()
			return tmp
		except queue.Empty:
			return None

	def getJobNoWait(self, queuename):
		self.__check_have_queue(queuename)
		self.log.info("Get job call for '%s' -> %s", queuename, self.mdict['inq'][queuename].qsize())
		try:
			return self.mdict['inq'][queuename].get_nowait()
		except queue.Empty:
			return None

	def putRss(self, message):
		feed_q_name = 'rss_queue'
		self.__check_rss_queue(feed_q_name)
		self.log.info("Putting rss item with size: %s (qsize: %s)!", len(message), self.mdict['feed_outq'][feed_q_name].qsize())
		self.mdict['feed_outq'][feed_q_name].put(message)

	def putManyRss(self, messages):
		feed_q_name = 'rss_queue'
		self.__check_rss_queue(feed_q_name)
		for message in messages:
			self.log.info("Putting rss item with size: %s!", len(message))
			self.mdict['feed_outq'][feed_q_name].put(message)

	def getRss(self):
		feed_q_name = 'rss_queue'
		self.__check_rss_queue(feed_q_name)
		self.log.info("Get job call for rss queue -> %s", self.mdict['feed_inq'][feed_q_name].qsize())
		try:
			ret = self.mdict['feed_inq'][feed_q_name].get_nowait()
			return ret
		except queue.Empty:
			return None

	def checkOk(self):
		return (True, b'wattt\0')


sock_path = '/tmp/rwp-fetchagent-sock'




def run_mprpc(interface_dict):
	print("MpRPC server Started.")
	server_instance = FetchInterfaceClass(interface_dict, "MpRPC")
	mprpc_server = StreamServer(('0.0.0.0', 4315), server_instance)

	gevent.signal(signal.SIGINT, build_mprpc_handler(mprpc_server))
	mprpc_server.serve_forever()


def initialize_manager(interface_dict):

	# interface_dict.qlock = pickle.dumps(mgr.Lock())
	interface_dict['qlock'] = threading.Lock()

	print("Manager lock: ", interface_dict['qlock'])
	interface_dict['outq'] = {}
	interface_dict['inq'] = {}

	interface_dict['feed_outq'] = {}
	interface_dict['feed_inq'] = {}


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
	amqp_interface = FetchAgent2.MessageProcessor.MessageProcessor(interface_dict)

	print("AMQP Interfaces have started. Launching RPC threads.")

	t2 = threading.Thread(target=run_mprpc, args=(interface_dict, ))

	t2.start()

	try:
		while INTERRUPTS == 0:
			amqp_interface.run()
			time.sleep(0.1)
	except AssertionError:
		print("Main worker encountered assertion failure!")
		traceback.print_exc()
		base_abort()
	except KeyboardInterrupt:
		print("Main worker abort")
		base_abort()

	except Exception:
		print("Wat?")
		traceback.print_exc()
		with open("Manager error %s.txt" % time.time(), "w") as fp:
			fp.write("Manager crashed?\n")
			fp.write(traceback.format_exc())


	print("Joining on worker threads")

	t2.join()

	print("Terminating AMQP interface.")
	amqp_interface.terminate()


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
