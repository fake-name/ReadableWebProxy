
import logging
import queue
import cachetools
import os
import os.path
import msgpack

import common.LogBase
import common.redis

from common.db_constants import DB_IDLE_PRIORITY
from common.db_constants import DB_MAX_PRIORITY


class NetlockThrottler(common.LogBase.LoggerMixin):

	loggerPath = "Main.RateLimiter"

	def __init__(self, key_prefix, fifo_limit=None, netloc_max=None):
		super().__init__()

		self.fifo_limit      = fifo_limit
		self.accumulator_min = 10
		self.accumulator_max = 100
		self.url_throttler   = {}

		self.total_queued    = 0

		self.jobl = []
		self.key_prefix = key_prefix

		if netloc_max is None:
			netloc_max = {}

		assert isinstance(netloc_max, dict)
		self.netloc_max = netloc_max

		# There should only be a few of these, so we can just
		# keep connections forever in each.
		self.redis = common.redis.get_redis_queue_conn()

	def __netloc_to_key(self, netloc, priority):
		return "{}_{}_{}".format(self.key_prefix, netloc, priority)


	def __check_init_nl(self, netloc):

		if not netloc in self.url_throttler:
			self.url_throttler[netloc] = {
				'active_fetches'     : 0,
				'status_accumulator' : 10,
				'active_priorities'  : set(),
			}

	def put_job(self, row_id, job_url, job_netloc, job_priority):

		self.__check_init_nl(job_netloc)

		self.url_throttler[job_netloc]['active_priorities'].add(job_priority)

		self.log.info("Putting limited job for netloc %s (%s items, score: %s, active: %s)",
			job_netloc,
			self.redis.llen(self.__netloc_to_key(job_netloc, job_priority)),
			self.url_throttler[job_netloc]['status_accumulator'],
			self.url_throttler[job_netloc]['active_fetches'])

		# if self.fifo_limit is None or self.url_throttler[job_netloc]['job_queue'].qsize() < self.fifo_limit:
		# 	self.url_throttler[job_netloc]['job_queue'].put((row_id, job_url, job_netloc))

		item_b = msgpack.packb((row_id, job_url, job_netloc), use_bin_type=True)
		self.redis.rpush(self.__netloc_to_key(job_netloc, job_priority), item_b)
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
		accumulator_max = self.netloc_max.get(netloc, self.accumulator_max)
		print("MAx for netloc: %s -> %s" % (netloc, accumulator_max))
		self.url_throttler[netloc]['status_accumulator'] = min(
			self.url_throttler[netloc]['status_accumulator'], accumulator_max)

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


	def _extract_for_netloc(self, job_netloc, key_dict):
		ret = []
		for priority in [x for x in range(DB_MAX_PRIORITY, DB_IDLE_PRIORITY+1) if x in self.url_throttler[job_netloc]['active_priorities']]:
			while True:

				# Allow unlimited fetching if the site isn't erroring at all
				if key_dict['active_fetches'] > key_dict['status_accumulator']:
					return ret

				# ret.append(item['job_queue'].get(block=False))
				item_b = self.redis.lpop(self.__netloc_to_key(job_netloc, priority))
				if not item_b:  # Nothing in queue
					break

				item = msgpack.unpackb(item_b, use_list=False, raw=False)
				ret.append(item)
				key_dict['active_fetches'] += 1
				self.total_queued -= 1

		return ret


	def get_available_jobs(self):

		ret = []

		for job_netloc, key_dict in self.url_throttler.items():
			ret += self._extract_for_netloc(job_netloc, key_dict)

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

