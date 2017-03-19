#!/usr/bin/env python3
import msgpack
import settings
import datetime
import queue
from . import AmqpConnector
import logging
import threading
import os.path
import time
import ssl
import uuid
import statsd


class RabbitQueueHandler(object):
	die = False

	def __init__(self, settings_param, mdict):

		self.logPath = 'Main.Feeds.RPC'

		self.log = logging.getLogger(self.logPath)
		self.log.info("RPC Management class instantiated.")
		self.mdict = mdict

		self.dispatch_map = {}

		# Require clientID in settings_param
		assert "RABBIT_LOGIN"       in settings_param
		assert "RABBIT_PASWD"       in settings_param
		assert "RABBIT_SRVER"       in settings_param
		assert "RABBIT_VHOST"       in settings_param

		assert "taskq_task"         in settings_param
		assert "taskq_response"     in settings_param

		assert 'taskq_name' in settings_param
		assert 'respq_name' in settings_param
		self.settings = settings_param

		sslopts = self.getSslOpts()
		self.vhost = settings_param["RABBIT_VHOST"]
		self.connector = AmqpConnector.Connector(userid            = settings_param["RABBIT_LOGIN"],
												password           = settings_param["RABBIT_PASWD"],
												host               = settings_param["RABBIT_SRVER"],
												virtual_host       = settings_param["RABBIT_VHOST"],
												ssl                = sslopts,
												master             = settings_param.get('master', True),
												synchronous        = settings_param.get('synchronous', False),
												flush_queues       = False,
												prefetch           = settings_param.get('prefetch', 25),
												durable            = True,
												heartbeat          = 60,
												task_exchange_type = settings_param.get('queue_mode', 'fanout'),
												poll_rate          = settings_param.get('poll_rate', 1.0/100),
												task_queue         = settings_param["taskq_task"],
												response_queue     = settings_param["taskq_response"],
												)

		self.chunks = {}

		self.log.info("Connected AMQP Interface: %s", self.connector)
		self.log.info("Connection parameters: %s, %s, %s, %s", settings_param["RABBIT_LOGIN"], settings_param["RABBIT_PASWD"], settings_param["RABBIT_SRVER"], settings_param["RABBIT_VHOST"])

		self.log.info("Setting up stats reporter")

		self.mon_con = statsd.StatsClient(
				host = settings.GRAPHITE_DB_IP,
				port = 8125,
				prefix = 'ReadableWebProxy.FetchAgent',
				)

		self.log.info("Setup complete!")


	def getSslOpts(self):
		'''
		Verify the SSL cert exists in the proper place.
		'''
		certpath = './rabbit_pub_cert/'

		caCert = os.path.abspath(os.path.join(certpath, './cacert.pem'))
		cert = os.path.abspath(os.path.join(certpath, './cert1.pem'))
		keyf = os.path.abspath(os.path.join(certpath, './key1.pem'))

		assert os.path.exists(caCert), "No certificates found on path '%s'" % caCert
		assert os.path.exists(cert), "No certificates found on path '%s'" % cert
		assert os.path.exists(keyf), "No certificates found on path '%s'" % keyf

		ret = {"cert_reqs" : ssl.CERT_REQUIRED,
				"ca_certs" : caCert,
				"keyfile"  : keyf,
				"certfile"  : cert,
			}
		print("Certificate config: ", ret)

		return ret

	def put_item(self, data):
		# self.log.info("Putting data: %s", data)
		return self.connector.putMessage(data)
		# self.log.info("Outgoing data size: %s bytes.", len(data))


	def get_item(self):
		ret = self.connector.getMessage()
		if ret:
			self.log.info("Received data size: %s bytes.", len(ret))
		return ret

	def process_chunk(self, chunk_message):
		assert 'chunk-type'   in chunk_message
		assert 'chunk-num'    in chunk_message
		assert 'total-chunks' in chunk_message
		assert 'data'         in chunk_message
		assert 'merge-key'    in chunk_message

		merge_key     = chunk_message['merge-key']
		total_chunks  = chunk_message['total-chunks']
		chunk_num     = chunk_message['chunk-num']
		data          = chunk_message['data']
		merge_key     = chunk_message['merge-key']

		if not merge_key in self.chunks:
			self.chunks[merge_key] = {
				'first-seen'  : datetime.datetime.now(),
				'chunk-count' : total_chunks,
				'chunks'      : {}
			}

		# Check our chunk count is sane.
		assert self.chunks[merge_key]['chunk-count'] == total_chunks
		self.chunks[merge_key]['chunks'][chunk_num] = data


		# TODO: clean out partial messages based on their age (see 'first-seen')

		if len(self.chunks[merge_key]['chunks']) == total_chunks:
			components = list(self.chunks[merge_key]['chunks'].items())
			components.sort()
			packed_message = b''.join([part[1] for part in components])
			ret = msgpack.unpackb(packed_message, encoding='utf-8', use_list=False)

			del self.chunks[merge_key]

			self.log.info("Received all chunks for key %s! Decoded size: %0.3fk from %s chunks. Active partial chunked messages: %s.",
				merge_key, len(packed_message) / 1024, len(components), len(self.chunks))

			return ret

		else:
			return None

	def unchunk(self, new_message):
		new = msgpack.unpackb(new_message, encoding='utf-8', use_list=False)

		# If we don't have a chunking type, it's probably an old-style message.
		if not 'chunk-type' in new:
			return new

		# Messages smaller then the chunk_size are not split, and can just be returned.
		if new['chunk-type'] == "complete-message":
			assert 'chunk-type' in new
			assert 'data'       in new
			return new['data']
		elif new['chunk-type'] == "chunked-message":
			return self.process_chunk(new)
		else:
			raise RuntimeError("Unknown message type: %s", new['chunk-type'])

	def get_job(self):
		while True:
			new = self.get_item()
			if new:
				self.log.info("Processing AMQP response item!")
				try:
					tmp = self.unchunk(new)

					# If unchunk returned something, return that.
					# if it didn't return anything, it means that new
					# was a message chunk, but we don't have the
					# whole thing yet, so continue.
					if tmp:
						return tmp
				except Exception:
					self.log.error("Failure unpacking message!")
					msgstr = str(new)
					if len(new) < 5000:
						self.log.error("Message content: %s", msgstr)
					else:
						self.log.error("Message length: '%s'", len(msgstr))
			else:
				return None

	def put_job(self, new_job):
		assert 'module'       in new_job
		assert 'call'         in new_job
		assert 'dispatch_key' in new_job
		assert 'jobid'        in new_job
		assert new_job['jobid'] != None

		assert 'jobmeta'     in new_job

		# Make sure we have a returned data list for the added job.

		packed_job = msgpack.packb(new_job, use_bin_type=True)
		self.put_item(packed_job)

	def __del__(self):
		self.close()

	def close(self):
		self.log.info("Closing connector wrapper: %s -> %s", self.logPath, self.vhost)
		self.connector.stop()




	def dispatch_outgoing(self):

		for qname, q in self.mdict[self.settings['taskq_name']].items():
			while not q.empty():
				try:
					job = q.get_nowait()
					jkey = uuid.uuid1().hex
					job['jobmeta'] = {'sort_key' : jkey}
					self.mon_con.incr("Fetch.Get.{}".format(qname), 1)
					self.dispatch_map[jkey] = (qname, time.time())
					self.put_job(job)
				except queue.Empty:
					break

	def process_retreived(self):
		while True:
			new = self.get_job()
			if not new:
				# print("No job item?", new)
				return

			if not 'jobmeta' in new:
				self.log.error("No metadata in job! Wat?")
				self.log.error("Job contents: '%s'", new)
				continue
			if not 'sort_key' in new['jobmeta']:
				self.log.error("No sort key in job! Wat?")
				self.log.error("Job contents: '%s'", new)
				continue

			jkey = new['jobmeta']['sort_key']
			if not jkey in self.dispatch_map:
				self.log.error("Job sort key not in known table! Does the job predate the current execution session?")
				self.log.error("Job key: '%s'", jkey)
				self.log.error("Job contents: '%s'", new)
				continue

			qname, started_at = self.dispatch_map[jkey]
			if not qname in self.mdict[self.settings['respq_name']]:
				self.log.error("Job response queue missing?")
				self.log.error("Queue name: '%s'", qname)
				continue

			self.mdict[self.settings['respq_name']][qname].put(new)

			fetchtime = (time.time() - started_at) * 1000

			self.mon_con.incr("Fetch.Resp.{}".format(qname), 1)
			self.mon_con.timing("Fetch.Duration.{}".format(qname), fetchtime)

			self.log.info("Demultiplexed job for '%s'. Time to response: %s", qname, fetchtime)


	def runner(self):
		self.mdict['amqp_runstate'] = True

		while self.mdict['amqp_runstate']:
			time.sleep(1)
			self.dispatch_outgoing()
			self.process_retreived()

		self.log.info("Saw exit flag. Closing interface")
		self.close()


class PlainRabbitQueueHandler(object):
	die = False

	def __init__(self, settings_param, mdict):

		self.logPath = 'Main.Feeds.RPC'

		self.log = logging.getLogger(self.logPath)
		self.log.info("RPC Management class instantiated.")
		self.mdict = mdict

		self.dispatch_map = {}

		# Require clientID in settings_param
		assert "RABBIT_LOGIN"       in settings_param
		assert "RABBIT_PASWD"       in settings_param
		assert "RABBIT_SRVER"       in settings_param
		assert "RABBIT_VHOST"       in settings_param

		assert "taskq_task"         in settings_param
		assert "taskq_response"     in settings_param

		assert 'taskq_name' in settings_param
		assert 'respq_name' in settings_param
		self.settings = settings_param

		sslopts = self.getSslOpts()
		self.vhost = settings_param["RABBIT_VHOST"]
		self.connector = AmqpConnector.Connector(userid            = settings_param["RABBIT_LOGIN"],
												password           = settings_param["RABBIT_PASWD"],
												host               = settings_param["RABBIT_SRVER"],
												virtual_host       = settings_param["RABBIT_VHOST"],
												ssl                = sslopts,
												master             = settings_param.get('master', True),
												synchronous        = settings_param.get('synchronous', False),
												flush_queues       = False,
												prefetch           = settings_param.get('prefetch', 25),
												durable            = True,
												heartbeat          = 60,
												task_exchange_type = settings_param.get('queue_mode', 'fanout'),
												poll_rate          = settings_param.get('poll_rate', 1.0/100),
												task_queue         = settings_param["taskq_task"],
												response_queue     = settings_param["taskq_response"],
												)


		self.log.info("Connected AMQP Interface: %s", self.connector)
		self.log.info("Connection parameters: %s, %s, %s, %s", settings_param["RABBIT_LOGIN"], settings_param["RABBIT_PASWD"], settings_param["RABBIT_SRVER"], settings_param["RABBIT_VHOST"])


		self.log.info("Setting up stats reporter")

		self.mon_con = statsd.StatsClient(
				host = settings.GRAPHITE_DB_IP,
				port = 8125,
				prefix = 'ReadableWebProxy.FetchAgent',
				)

		self.log.info("Setup complete!")

	def getSslOpts(self):
		'''
		Verify the SSL cert exists in the proper place.
		'''
		certpath = './rabbit_pub_cert/'

		caCert = os.path.abspath(os.path.join(certpath, './cacert.pem'))
		cert = os.path.abspath(os.path.join(certpath, './cert1.pem'))
		keyf = os.path.abspath(os.path.join(certpath, './key1.pem'))

		assert os.path.exists(caCert), "No certificates found on path '%s'" % caCert
		assert os.path.exists(cert), "No certificates found on path '%s'" % cert
		assert os.path.exists(keyf), "No certificates found on path '%s'" % keyf

		ret = {"cert_reqs" : ssl.CERT_REQUIRED,
				"ca_certs" : caCert,
				"keyfile"  : keyf,
				"certfile"  : cert,
			}
		print("Certificate config: ", ret)

		return ret


	def get_item(self):
		ret = self.connector.getMessage()
		if ret:
			self.log.info("Received data size: %s bytes.", len(ret))
		return ret


	def put_job(self, new_job):

		# packed_job = msgpack.packb(new_job, use_bin_type=True)
		self.connector.putMessage(new_job, synchronous=1000)

	def __del__(self):
		self.close()

	def close(self):
		self.log.info("Closing connector wrapper: %s -> %s", self.logPath, self.vhost)
		self.connector.stop()


	def dispatch_outgoing(self):
		while not self.mdict[self.settings['taskq_name']].empty():
			try:
				job = self.mdict[self.settings['taskq_name']].get_nowait()
				self.put_job(job)
				self.mon_con.incr("Feed.Put.{}".format(qname), 1)
			except queue.Empty:
				break

	def process_retreived(self):
		while True:
			new = self.get_item()

			if not new:
				# print("No job item?", new)
				return

			self.mdict[self.settings['respq_name']].put(new)

			self.mon_con.incr("Feed.Recv.{}".format(qname), 1)



	def runner(self):
		self.mdict['amqp_runstate'] = True

		while self.mdict['amqp_runstate']:
			time.sleep(1)
			self.dispatch_outgoing()
			self.process_retreived()

		self.log.info("Saw exit flag. Closing interface")
		self.close()







STATE = {}

def monitor(manager):
	while manager['amqp_runstate']:
		STATE['rpc_instance'].connector.checkLaunchThread()
		STATE['feed_instance'].connector.checkLaunchThread()
		time.sleep(1)
		print("Monitor looping!")


def startup_interface(manager):
	rpc_amqp_settings = {
		'RABBIT_LOGIN'    : settings.RPC_RABBIT_LOGIN,
		'RABBIT_PASWD'    : settings.RPC_RABBIT_PASWD,
		'RABBIT_SRVER'    : settings.RPC_RABBIT_SRVER,
		'RABBIT_VHOST'    : settings.RPC_RABBIT_VHOST,
		'master'          : True,
		'prefetch'        : 250,
		# 'prefetch'        : 50,
		# 'prefetch'        : 5,
		'queue_mode'      : 'direct',
		'taskq_task'      : 'task.q',
		'taskq_response'  : 'response.q',

		"poll_rate"       : 1/100,

		'taskq_name' : 'outq',
		'respq_name' : 'inq',

	}

	feed_amqp_settings = {
		'RABBIT_LOGIN'    : settings.RABBIT_LOGIN,
		'RABBIT_PASWD'    : settings.RABBIT_PASWD,
		'RABBIT_SRVER'    : settings.RABBIT_SRVER,
		'RABBIT_VHOST'    : settings.RABBIT_VHOST,
		'master'          : True,
		'prefetch'        : 25,
		# 'prefetch'        : 50,
		# 'prefetch'        : 5,
		'queue_mode'              : 'fanout',
		'taskq_task'              : 'task.q',
		'taskq_response'          : 'response.q',

		'task_exchange_type'      : 'fanout',
		'response_exchange_type'  : 'direct',


		"poll_rate"               : 1/100,

		'taskq_name'              : 'feed_outq',
		'respq_name'              : 'feed_inq',
	}

	STATE['rpc_instance'] = RabbitQueueHandler(rpc_amqp_settings, manager)
	STATE['rpc_thread'] = threading.Thread(target=STATE['rpc_instance'].runner)
	STATE['rpc_thread'].start()

	STATE['feed_instance'] = PlainRabbitQueueHandler(feed_amqp_settings, manager)
	STATE['feed_thread'] = threading.Thread(target=STATE['feed_instance'].runner)
	STATE['feed_thread'].start()

	STATE['monitor_thread'] = threading.Thread(target=monitor, args=[manager])
	STATE['monitor_thread'].start()


def shutdown_interface(manager):
	print("Halting AMQP interface")
	manager['amqp_runstate'] = False
	STATE['rpc_thread'].join()
	STATE['feed_thread'].join()
	STATE['monitor_thread'].join()

