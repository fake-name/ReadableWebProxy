

import WebMirror.rules
import abc
import WebMirror.TimedTriggers.TriggerBase

import urllib.parse
import datetime
import sqlalchemy.exc
import WebMirror.JobDispatcher



class QueueTrigger(WebMirror.TimedTriggers.TriggerBase.TriggerBaseClass, WebMirror.JobDispatcher.RpcMixin):


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.instance = WebMirror.JobDispatcher.RpcJobDispatcherInternal(None, None)
		self.check_open_rpc_interface()

		self.sess = self.db.get_db_session()


	def get_create_job(self, url):

		have = self.sess.query(self.db.WebPages).filter(self.db.WebPages.url == url).scalar()
		if have:
			return have
		else:

			parsed = urllib.parse.urlparse(url)
			root = urllib.parse.urlunparse((parsed[0], parsed[1], "", "", "", ""))

			new = self.db.WebPages(
				url       = url,
				starturl  = root,
				netloc    = parsed.netloc,
				distance  = 50000,
				is_text   = True,
				priority  = 500000,
				type      = 'unknown',
				fetchtime = datetime.datetime.now(),
				)
			self.sess.add(new)
			self.sess.commit()
			return new

	def enqueue_url(self, url):

		print("Enqueueing ")
		job = self.get_create_job(url)
		job.state = 'fetching'
		self.sess.commit()

		raw_job = WebMirror.JobUtils.buildjob(
			module         = 'WebRequest',
			call           = 'getItem',
			dispatchKey    = "fetcher",
			jobid          = job.id,
			args           = [job.url],
			kwargs         = {},
			additionalData = {'mode' : 'fetch'},
			postDelay      = 0
		)

		self.rpc_interface.put_job(raw_job)

	def go(self):
		for url in self.get_urls():
			self.enqueue_url(url)


	@abc.abstractmethod
	def get_urls(self):
		pass


class NuQueueTrigger(QueueTrigger):

	loggerPath = 'NuQueueTrigger'
	pluginName = 'NuQueueTrigger'

	def get_urls(self):
		return [

			# Fetch the new NovelUpdates stuff.
			'http://www.novelupdates.com/',
		]



