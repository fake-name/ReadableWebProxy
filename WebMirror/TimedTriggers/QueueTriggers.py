

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




	def get_create_job(self, sess, url):

		have = sess.query(self.db.WebPages).filter(self.db.WebPages.url == url).scalar()
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
			sess.add(new)
			sess.commit()
			return new

	def enqueue_url(self, sess, url):

		print("Enqueueing ")
		job = self.get_create_job(sess, url)
		job.state = 'fetching'
		sess.commit()

		raw_job = WebMirror.JobUtils.buildjob(
			module         = 'SmartWebRequest',
			call           = 'smartGetItem',
			dispatchKey    = "fetcher",
			jobid          = job.id,
			args           = [job.url],
			kwargs         = {},
			additionalData = {'mode' : 'fetch'},
			postDelay      = 0
		)

		self.rpc_interface.put_job(raw_job)

	def go(self):

		with self.db.session_context() as sess:
			for url in self.get_urls():
				self.enqueue_url(sess, url)


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



