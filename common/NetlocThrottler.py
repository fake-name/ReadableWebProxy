
import logging
import queue
import cachetools

import common.LogBase

class NetlockThrottler(common.LogBase.LoggerMixin):

	loggerPath = "Main.RateLimiter"

	def __init__(self):
		super().__init__()

		self.accumulator_min = -100
		self.accumulator_max =  250
		self.url_throttler = {}

		self.jobl = []

	def __check_init_nl(self, netloc):

		if not netloc in self.url_throttler:
			self.url_throttler[netloc] = {
				'active_fetches'     : 0,
				'status_accumulator' : 5,
				'job_queue'          : queue.Queue(),
			}

	def put_job(self, row_id, job_url, job_netloc):
		self.__check_init_nl(job_netloc)
		self.log.info("Putting limited job for netloc %s", job_netloc)

		self.url_throttler[job_netloc]['job_queue'].put((row_id, job_url, job_netloc))

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


	def get_available_jobs(self):
		ret = []
		for item in self.url_throttler.values():
			try:
				while item['active_fetches'] <= item['status_accumulator']:
					ret.append(item['job_queue'].get(block=False))
					item['active_fetches'] += 1
			except queue.Empty:
				pass

		self.log.info("Extracted %s jobs from rate-limiting queues.", len(ret))

		return ret

