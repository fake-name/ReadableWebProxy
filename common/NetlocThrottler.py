
import logging
import queue
import cachetools
import os
import os.path
import msgpack

import common.LogBase
import common.redis



class NetlockThrottler(common.LogBase.LoggerMixin):

	loggerPath = "Main.RateLimiter"

	def __init__(self, fifo_limit=None):
		super().__init__()

		self.fifo_limit      = fifo_limit
		self.accumulator_min = 10
		self.accumulator_max = 500
		self.url_throttler   = {}

		self.total_queued    = 0

		self.jobl = []

		# There should only be a few of these, so we can just
		# keep connections forever in each.
		self.redis = common.redis.get_redis_queue_conn()


	def __check_init_nl(self, netloc):

		if not netloc in self.url_throttler:
			self.url_throttler[netloc] = {
				'active_fetches'     : 0,
				'status_accumulator' : 10,
			}

	def put_job(self, row_id, job_url, job_netloc):
		self.__check_init_nl(job_netloc)
		self.log.info("Putting limited job for netloc %s (%s items, score: %s, active: %s)",
			job_netloc,
			self.redis.llen(job_netloc),
			self.url_throttler[job_netloc]['status_accumulator'],
			self.url_throttler[job_netloc]['active_fetches'])

		# if self.fifo_limit is None or self.url_throttler[job_netloc]['job_queue'].qsize() < self.fifo_limit:
		# 	self.url_throttler[job_netloc]['job_queue'].put((row_id, job_url, job_netloc))

		item_b = msgpack.packb((row_id, job_url, job_netloc), use_bin_type=True)
		self.redis.rpush(job_netloc, item_b)
		# self.url_throttler[job_netloc]['job_queue'].put((row_id, job_url, job_netloc))

		self.total_queued += 1

	def netloc_error(self, netloc):
		self.__check_init_nl(netloc)

		self.url_throttler[netloc]['status_accumulator'] -= 1
		self.url_throttler[netloc]['status_accumulator'] = max(
			self.url_throttler[netloc]['status_accumulator'], self.accumulator_min)

		self.log.warning("Err: Limiter status for netloc %s: %s (active %s)", netloc,
			self.url_throttler[netloc]['status_accumulator'], self.url_throttler[netloc]['active_fetches'])

		self.url_throttler[netloc]['active_fetches'] -= 1
		self.url_throttler[netloc]['active_fetches'] = max(
			self.url_throttler[netloc]['active_fetches'], 0)

	def netloc_ok(self, netloc):
		self.__check_init_nl(netloc)

		self.url_throttler[netloc]['status_accumulator'] += 1
		self.url_throttler[netloc]['status_accumulator'] = min(
			self.url_throttler[netloc]['status_accumulator'], self.accumulator_max)

		self.log.info("Ok: Limiter status for netloc %s: %s (active %s)", netloc,
			self.url_throttler[netloc]['status_accumulator'], self.url_throttler[netloc]['active_fetches'])

		self.url_throttler[netloc]['active_fetches'] -= 1
		self.url_throttler[netloc]['active_fetches'] = max(
			self.url_throttler[netloc]['active_fetches'], 0)

	def clear_active_counts(self, override_status=False):
		for value in self.url_throttler.values():
			value['active_fetches'] = 0
			if override_status:
				value['status_accumulator'] = override_status


	def get_in_queues(self):
		return self.total_queued

	def get_available_jobs(self):
		ret = []
		for job_netloc, key_dict in self.url_throttler.items():
			try:
				# Allow unlimited fetching if the site isn't erroring at all
				while key_dict['active_fetches'] <= key_dict['status_accumulator']:
					# ret.append(item['job_queue'].get(block=False))
					item_b = self.redis.lpop(job_netloc)
					if not item_b:  # Nothing in queue
						break
					item = msgpack.unpackb(item_b, use_list=False, raw=False)
					ret.append(item)
					key_dict['active_fetches'] += 1
					self.total_queued -= 1
			except queue.Empty:
				pass
			except persistqueue.Empty:
				pass

		self.log.info("Extracted %s jobs from rate-limiting queues.", len(ret))

		return ret


	def job_reduce(self):
		'''
		We periodically reduce the number of apparent active jobs,
		as well as the number of errors, so timeouts don't persist
		forever.
		'''
		for item in self.url_throttler.values():
			if item['status_accumulator'] < 5:
				item['status_accumulator'] += 1
			elif item['status_accumulator'] > 5:
				item['status_accumulator'] -= 1

