#!/usr/bin/env python3
import msgpack
import datetime
import traceback
import queue
import logging
import threading
import os.path
import time
import ssl
import uuid
import statsd
import cachetools
import fdict

import settings as settings_file
from . import InterfaceConsumer
from . import MessageSettings



WORKER_CONFS = {
	'RPC_AMQP_SETTINGS'         : MessageSettings.RPC_AMQP_SETTINGS,
	'LOWRATE_RPC_AMQP_SETTINGS' : MessageSettings.LOWRATE_RPC_AMQP_SETTINGS,
	'FEED_AMQP_SETTINGS'        : MessageSettings.FEED_AMQP_SETTINGS,
}


def hours(num):
	return 60*60*num

class MessageProcessor(object):
	def __init__(self, interface_dict):
		self.log = logging.getLogger('Main.Feeds.RPC')

		self.worker_pools   = {}
		self.interface_dict = interface_dict

		self.mon_con = statsd.StatsClient(
				host = settings_file.GRAPHITE_DB_IP,
				port = 8125,
				prefix = 'ReadableWebProxy.FetchAgent',
				)

		self.debug_interval = 10
		self.chunk_flush_interval = 10
		self.last_debug = time.time() - self.debug_interval
		self.last_chunk_flush = time.time() - self.chunk_flush_interval

		os.makedirs(settings_file.CHUNK_CACHE_DIR, exist_ok=True)

	def __init_pool(self, pool_name):
		self.worker_pools[pool_name] = {
			'outgoing_q'   : queue.Queue(),
			'incoming_q'   : queue.Queue(),
			'workers'      : [],

			'dispatch_map' : cachetools.TTLCache(maxsize=10000, ttl=hours(24)),

			# The chunk structure is slightly annoying, so just limit to 50 partial message keys, and
			# a TTL of 3 hours.
			# 'chunk_cache'  : fdict.sfdict(filename=os.path.join(settings_file.CHUNK_CACHE_DIR, "chunk_cache_{}.db".format(pool_name.lower()))),
			'chunk_cache'   : cachetools.TTLCache(maxsize=50, ttl=hours(3)),
			'chunk_lock'   : threading.Lock(),
		}

	def __check_pool(self, worker_name, worker_settings):
		dead_workers = [tmp for tmp in self.worker_pools[worker_name]['workers'] if not tmp.worker_alive()]
		for dead_worker in dead_workers:
			self.log.warning("Dead worker thread in pool for '%s'! Removing", worker_name)
			try:
				dead_worker.join()
				self.worker_pools[worker_name]['workers'].remove(dead_worker)
			except Exception:
				with open("Error in message processor %s.txt" % time.time(), "w") as fp:
					exc = traceback.format_exc()
					fp.write("Message processor had error!\n")
					fp.write(exc)
					print("Message processor had error!\n")
					print(exc)

		while len(self.worker_pools[worker_name]['workers']) < worker_settings['worker_threads']:
			self.log.warning("Need to create worker thread in pool for '%s'", worker_name)
			new_worker = InterfaceConsumer.SingleAmqpConnection(
					config         = worker_settings,
					task_queue     = self.worker_pools[worker_name]['outgoing_q'],
					response_queue = self.worker_pools[worker_name]['incoming_q'],
				)
			self.worker_pools[worker_name]['workers'].append(new_worker)


	def __check_workers(self):
		for worker_name, worker_settings in WORKER_CONFS.items():
			if not worker_name in self.worker_pools:
				self.__init_pool(worker_name)
			self.__check_pool(worker_name, worker_settings)

	def __forward_outgoing(self):
		'''
		For each worker pool, consume from all the queues in it's interface queue-set,
		and forward the items into the pool queue
		'''
		for worker_name, worker_settings in WORKER_CONFS.items():
			outq_n = worker_settings['taskq_name']
			if not outq_n in self.interface_dict:
				raise RuntimeError("Setting outbound queue '%s' doesn't exist!" % outq_n)

			assert isinstance(self.interface_dict[outq_n], dict), "Interface dict member '%s' is not also a dict. Actual type: %s" % (
					outq_n, type(self.interface_dict[outq_n]))

			for queue_name, outq in self.interface_dict[outq_n].items():
				qsz = outq.qsize()
				if qsz:
					self.log.info("Polling interface dict queue: '%s' -> '%s' (%s items)", outq_n, queue_name, qsz)
				try:
					while True:
						new_job = outq.get_nowait()
						if isinstance(new_job, str):
							self.log.info("Sending string job!")
							self.worker_pools[worker_name]['outgoing_q'].put(new_job)
						elif isinstance(new_job, bytes):
							self.log.info("Sending bytes job!")
							self.worker_pools[worker_name]['outgoing_q'].put(new_job)
						elif isinstance(new_job, dict):
							assert isinstance(new_job, dict), "Jobs must be of type dict, passed type '%s'" % type(new_job)

							# Attach tracking data to the job
							jkey = str(uuid.uuid1().hex)
							meta = {
								'sort_key'   : jkey,
								'qname'      : queue_name,
								'started_at' : time.time(),
								}
							new_job['jobmeta'] = meta
							self.worker_pools[worker_name]['dispatch_map'][jkey] = (queue_name, time.time())

							assert 'module'       in new_job
							assert 'call'         in new_job
							assert 'dispatch_key' in new_job
							assert 'jobid'        in new_job
							assert new_job['jobid'] != None
							assert 'jobmeta'     in new_job

							# Make sure we have a returned data list for the added job.

							packed_job = msgpack.packb(new_job, use_bin_type=True)
							self.worker_pools[worker_name]['outgoing_q'].put(packed_job)
						else:
							raise AssertionError("Unknown outbound job type: '%s'" % type(new_job))

						self.mon_con.incr("Fetch.Resp.{}".format(queue_name), 1)

				except queue.Empty:
					pass

	def __check_have_interface_queue(self, worker_name, queuename):

		if not queuename in self.interface_dict[WORKER_CONFS[worker_name]['taskq_name']]:
			self.log.warning("Need to create queues for client name: %s", queuename)
			with self.interface_dict['qlock']:
				self.interface_dict[WORKER_CONFS[worker_name]['taskq_name']][queuename] = queue.Queue()
				self.interface_dict[WORKER_CONFS[worker_name]['respq_name']][queuename] = queue.Queue()



	def __process_chunk(self, chunk_message, worker_name):
		assert 'chunk-type'   in chunk_message
		assert 'chunk-num'    in chunk_message
		assert 'total-chunks' in chunk_message
		assert 'data'         in chunk_message
		assert 'merge-key'    in chunk_message

		total_chunks  = chunk_message['total-chunks']
		chunk_num     = chunk_message['chunk-num']
		data          = chunk_message['data']
		merge_key     = chunk_message['merge-key']

		with self.worker_pools[worker_name]['chunk_lock']:
			if not merge_key in self.worker_pools[worker_name]['chunk_cache']:
				self.worker_pools[worker_name]['chunk_cache'][merge_key] = {
					'first-seen'  : datetime.datetime.now(),
					'chunk-count' : total_chunks,
					'chunks'      : {}
				}

			# Check our chunk count is sane.
			assert self.worker_pools[worker_name]['chunk_cache'][merge_key]['chunk-count'] == total_chunks
			self.worker_pools[worker_name]['chunk_cache'][merge_key]['chunks'][chunk_num] = data

			if len(self.worker_pools[worker_name]['chunk_cache'][merge_key]['chunks']) == total_chunks:
				components = list(self.worker_pools[worker_name]['chunk_cache'][merge_key]['chunks'].items())
				components.sort()
				packed_message = b''.join([part[1] for part in components])
				ret = msgpack.unpackb(packed_message, encoding='utf-8', use_list=False)

				self.worker_pools[worker_name]['chunk_cache'][merge_key] = None
				del self.worker_pools[worker_name]['chunk_cache'][merge_key]

				# self.worker_pools[worker_name]['chunk_cache'].sync()

				self.log.info("Received all chunks for key %s! Decoded size: %0.3fk from %s chunks. Active partial chunked messages: %s.",
					merge_key, len(packed_message) / 1024, len(components), len(self.worker_pools[worker_name]['chunk_cache']))

				return ret

			else:
				self.log.info("Have %s/%s items for chunk, %s different partial messages in queue.",
					len(self.worker_pools[worker_name]['chunk_cache'][merge_key]['chunks']),
					total_chunks,
					len(self.worker_pools[worker_name]['chunk_cache']))

				# if time.time() > self.last_chunk_flush + self.chunk_flush_interval:
				# 	self.last_chunk_flush += self.chunk_flush_interval
				# 	self.worker_pools[worker_name]['chunk_cache'].sync()

				return None

	def __unchunk(self, new_message, worker_name):
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
			return self.__process_chunk(new, worker_name)
		else:
			raise RuntimeError("Unknown message type: %s", new['chunk-type'])

	def __dispatch_response(self, job_data, worker_name):

		if not 'jobmeta' in job_data:
			self.log.error("No metadata in job! Wat?")
			self.log.error("Job contents: '%s'", job_data)
			return

		if not any(['sort_key' in job_data['jobmeta'], 'qname' in job_data['jobmeta']]):
			self.log.error("No sort key in job! Wat?")
			self.log.error("Job contents: '%s'", job_data)
			return

		if 'sort_key' in job_data['jobmeta'] and job_data['jobmeta']['sort_key'] in self.worker_pools[worker_name]['dispatch_map']:
			qname, started_at = self.worker_pools[worker_name]['dispatch_map'].pop(job_data['jobmeta']['sort_key'])
			self.worker_pools[worker_name]['dispatch_map'][job_data['jobmeta']['sort_key']] = None
			del self.worker_pools[worker_name]['dispatch_map'][job_data['jobmeta']['sort_key']]

		elif 'qname' in job_data['jobmeta']:
			qname = job_data['jobmeta']['qname']
			started_at = None
			self.log.warning("Missing sort key in jobmeta. Have queue override: %s!", qname)

		elif 'sort_key' in job_data['jobmeta'] and not job_data['jobmeta']['sort_key'] in self.worker_pools[worker_name]['dispatch_map']:
			self.log.error("Job sort key not in known table! Does the job predate the current execution session?")
			self.log.error("Job key: '%s'", job_data['jobmeta']['sort_key'])
			self.log.error("Job contents: '%s'", job_data)
			return
		else:
			self.log.error("No sort key or queue name in response!")
			self.log.error("Response meta: %s", job_data['jobmeta'])
			return

		# Why bother caching here?
		if not started_at and 'started_at' in job_data['jobmeta']:
			started_at = job_data['jobmeta']['started_at']

		self.__check_have_interface_queue(worker_name, qname)

		self.interface_dict[WORKER_CONFS[worker_name]['respq_name']][qname].put(job_data)

		if started_at:
			fetchtime = (time.time() - started_at) * 1000
			self.mon_con.timing("Fetch.Duration.{}".format(qname), fetchtime)
			self.log.info("Demultiplexed job for '%s'. Time to response: %s", qname, fetchtime)
		else:
			self.log.info("Demultiplexed job for '%s'. Original fetchtime missing!", qname)


		self.mon_con.incr("Fetch.Resp.{}".format(qname), 1)

	def __process_incoming(self):
		'''
		Consume from the worker pools, and dispatch into the relevant
		RPC interfaces.

		This is slightly more complex, because it needs to handle chunked
		responses.
		'''
		for worker_name, worker_settings in WORKER_CONFS.items():
			try:
				while 1:
					resp_dat = self.worker_pools[worker_name]['incoming_q'].get_nowait()
					resp = self.__unchunk(resp_dat, worker_name)
					if resp:
						self.__dispatch_response(resp, worker_name)
			except queue.Empty:
				pass
			except MemoryError:
				# shit has asploded. Drop the chunk cache on the floor to avoid dying completely.
				for pool in self.worker_pools.values():
					pool['chunk_cache'] = cachetools.LRUCache(maxsize=50)
					# pool['chunk_cache'] = fdict.sfdict(filename=os.path.join(settings_file.CHUNK_CACHE_DIR, "chunk_cache_{}.db".format(pool_name.lower()))),

				with open("Manager Memory Error %s.txt" % time.time(), "w") as fp:
					fp.write("Manager ran out of memory!\n")
					fp.write(traceback.format_exc())

	def __status_debug(self):
		if time.time() < self.last_debug + self.debug_interval:
			return

		self.last_debug += self.debug_interval

		self.log.info("Debugging RPC State")
		for worker_name, worker_conf in self.worker_pools.items():
			self.log.info("	Queue for {qname} -> {q_outgoing}/{q_incoming}, pool: {dispatch_map_sz}, chunk_cache: {chunks} {state_per_chunk}".format(
						qname           = worker_name.ljust(30),
						q_outgoing      = worker_conf['outgoing_q'].qsize(),
						q_incoming      = worker_conf['incoming_q'].qsize(),
						dispatch_map_sz = len(worker_conf['dispatch_map']),
						chunks          = len(worker_conf['chunk_cache']),
						state_per_chunk = [(len(tmp['chunks']), tmp['chunk-count']) for tmp in worker_conf['chunk_cache'].values() if tmp and 'chunks' in tmp and 'chunk-count' in tmp]
					)
				)

		for interface_group, queue_dict in self.interface_dict.items():
			if isinstance(queue_dict, dict):
				for queue_name, queue_item in queue_dict.items():
					self.log.info("	Queue: %s->%s: %s", queue_name.ljust(20), interface_group.ljust(4), queue_item.qsize())
			else:
				self.log.info("	Item: %s -> %s", interface_group, queue_dict)


	def run(self):
		self.__check_workers()
		self.__forward_outgoing()
		self.__process_incoming()
		self.__status_debug()

	def __terminate_pool(self, worker_name, worker_settings):
		self.log.info("Joining on workers for pool %s", worker_name)
		for worker in self.worker_pools[worker_name]['workers']:
			worker.signal_stop()
		for worker in self.worker_pools[worker_name]['workers']:
			worker.join()

	def terminate(self):
		for worker_name, worker_settings in WORKER_CONFS.items():
			if not worker_name in self.worker_pools:
				self.__init_pool(worker_name)
			self.__terminate_pool(worker_name, worker_settings)

