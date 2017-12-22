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

from settings import settings as settings_file
from . import InterfaceConsumer
from . import MessageSettings



WORKER_CONFS = {
	'RPC_AMQP_SETTINGS'         : MessageSettings.RPC_AMQP_SETTINGS,
	'LOWRATE_RPC_AMQP_SETTINGS' : MessageSettings.LOWRATE_RPC_AMQP_SETTINGS,
	'FEED_AMQP_SETTINGS'        : MessageSettings.FEED_AMQP_SETTINGS,
}


class MessageProcessor(object):
	def __init__(self, interface_dict):
		self.log = logging.getLogger('Main.Feeds.RPC')

		self.worker_pools   = {}
		self.interface_dict = interface_dict

		self.mon_con = statsd.StatsClient(
				host = settings_file['GRAPHITE_DB_IP'],
				port = 8125,
				prefix = 'ReadableWebProxy.FetchAgent',
				)


	def __init_pool(self, pool_name):
		self.worker_pools[pool_name] = {
			'outgoing_q'   : queue.Queue(),
			'incoming_q'   : queue.Queue(),
			'workers'      : [],
			'dispatch_map' : {},

			# The chunk structure is slightly annoying, so just limit to 10 partial message keys.
			'chunk_cache'  : cachetools.LRUCache(maxsize=5),
			'chunk_lock'   : threading.Lock(),
		}

	def __check_pool(self, worker_name, worker_settings):
		dead_workers = [tmp for tmp in self.worker_pools[worker_name]['workers'] if not tmp.worker_alive()]
		for dead_worker in dead_workers:
			self.log.warning("Dead worker thread in pool for '%s'! Removing", worker_name)
			self.worker_pools[worker_name]['workers'].remove(dead_worker)
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
			for queue_name, outq in self.interface_dict[outq_n].items():
				try:
					while True:
						new_job = outq.get_nowait()

						# Attach tracking data to the job
						jkey = uuid.uuid1().hex
						new_job['jobmeta'] = {
							'sort_key' : jkey,
							'qname'    : queue_name,
							}
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

				del self.worker_pools[worker_name]['chunk_cache'][merge_key]

				self.log.info("Received all chunks for key %s! Decoded size: %0.3fk from %s chunks. Active partial chunked messages: %s.",
					merge_key, len(packed_message) / 1024, len(components), len(self.worker_pools[worker_name]['chunk_cache']))

				return ret

			else:
				self.log.info("Have %s/%s items for chunk, %s different partial messages in queue.",
					len(self.worker_pools[worker_name]['chunk_cache'][merge_key]['chunks']),
					total_chunks,
					len(self.worker_pools[worker_name]['chunk_cache']))
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
			qname, started_at = self.worker_pools[worker_name]['dispatch_map'][job_data['jobmeta']['sort_key']]
		elif 'qname' in job_data['jobmeta']:
			qname = job_data['jobmeta']['qname']
			started_at = None

		elif 'sort_key' in job_data['jobmeta'] and not job_data['jobmeta']['sort_key'] in self.worker_pools[worker_name]['dispatch_map']:
			self.log.error("Job sort key not in known table! Does the job predate the current execution session?")
			self.log.error("Job key: '%s'", job_data['jobmeta']['sort_key'])
			self.log.error("Job contents: '%s'", job_data)
			return
		else:
			self.log.error("No sort key or queue name in response!")
			self.log.error("Response meta: %s", job_data['jobmeta'])
			return

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


	def run(self):
		self.__check_workers()
		self.__forward_outgoing()
		self.__process_incoming()
