
import datetime
import os.path
import contextlib
import logging
import random
import urllib.parse
import common.database
import Misc.txt_to_img
import WebMirror.Engine
# import WebMirror.runtime_engines
from common.Exceptions import DownloadException, getErrorDiv
from flask import g
from app import app
from app import utilities

import common.global_constants


import WebRequest
import WebRequest.UA_Constants as wr_constants
import common.util.DbCookieJar as dbCj
import common.database as db

def td_format(td_object):
		seconds = int(td_object.total_seconds())
		periods = [
				('y',        60*60*24*365),
				('d',         60*60*24),
				('h',        60*60),
				('m',      60),
				('s',      1)
				]

		if seconds < 1:
			return "just fetched"

		retstr=[]
		for period_name, period_seconds in periods:
			if seconds > period_seconds:
				period_value, seconds = divmod(seconds,period_seconds)
				retstr.append("%s%s" % (period_value, period_name))

		return ", ".join(retstr)

WG_POOL = [WebRequest.WebGetRobust(
			alt_cookiejar = dbCj.DatabaseCookieJar(db=db, session=db.get_db_session(postfix="_cookie_interface"))
			) for x in range(2)]

class RemoteContentObject(object):
	def __init__(self, url, db_session = None):
		self.log = logging.getLogger("Main.RemoteContentObject")
		self.url     = url
		self.fetched = False
		self.job     = None



		if db_session:
			self.db_sess = db_session
		else:
			self.db_sess = g.session

		# print("RemoteContentObject instantiated. Available fetchers: %s" % WebMirror.runtime_engines.fetchers.qsize())
		# self.archiver = WebMirror.runtime_engines.fetchers.get()
		self.archiver = WebMirror.Engine.SiteArchiver(cookie_lock=False,
			new_job_queue=None,
			db_interface=self.db_sess,
			wg_override=random.choice(WG_POOL)
			)


	def fetch(self, ignore_cache=False, version=None):
		self.fetched = True

		assert not (ignore_cache and version)

		self.job     = self.archiver.synchronousJobRequest(self.url, ignore_cache)

		# Override the job instance if we're fetching a old version
		if version != None:
			self.job = self.job.versions[version]


	def getTitle(self):
		assert self.fetched
		assert self.job
		return self.job.title

	def getContent(self, relink_replace):
		"""
		At this point, we have the page content, but we need to
		replace the url/resource keys with the proper paths
		so that the page will render properly
		"""
		assert self.fetched


		content = self.job.content
		if content and relink_replace:
			content = utilities.replace_links(content)
		return content

	def getMime(self):
		assert self.fetched
		assert self.job

		return self.job.mimetype

	def getResource(self):
		"""
		At this point, we have the page content, but we need to
		replace the url/resource keys with the proper paths
		so that the page will render properly
		"""

		assert self.fetched
		if self.job.state != "complete":
			self.log.error("Job resource retreival attempted when job has not been completed!")
			self.log.error("Target URL %s", self.job.url)

			msg  = "Job failed or not fetched!\n"
			msg += "Current job state: %s\n" % self.job.state
			msg += "URL: %s\n" % self.job.url
			img_dat = Misc.txt_to_img.text_to_png(msg)
			return "image/png", "genimg.%s.png", img_dat
			# job failed
		if not self.job.file:
			try:
				self.fetch(ignore_cache=True)

			except DownloadException:
				self.log.error("Failure during refetch-attempt for item!")
				self.log.error("Refetch attempt for %s", self.job.url)

				msg  = "Job complete, but no file present?!\n"
				msg += "Current job state: %s\n" % self.job.state
				msg += "URL: %s\n" % self.job.url
				msg += "Returned MIME: %s\n" % self.job.mimetype
				msg += "Content size: %s\n" % len(self.job.content)
				# msg += "Body: %s\n" % self.job.content
				img_dat = Misc.txt_to_img.text_to_png(msg)
				return "image/png", "genimg.%s.png", img_dat

			if not self.job.file:

				self.log.error("Refetch for resource did not return content!")
				self.log.error("Target URL %s", self.job.url)

				msg  = "Job complete, no file present, and refetch failed!\n"
				msg += "Current job state: %s\n" % self.job.state
				msg += "URL: %s\n" % self.job.url
				msg += "Returned MIME: %s\n" % self.job.mimetype
				msg += "Content size: %s\n" % len(self.job.content)
				# msg += "Body: %s\n" % self.job.content
				img_dat = Misc.txt_to_img.text_to_png(msg)
				return "image/png", "genimg.%s.png", img_dat

		assert self.fetched
		assert self.job.file

		itempath = os.path.join(app.config['RESOURCE_DIR'], self.job.file_item.fspath)
		fname = self.job.file_item.filename

		with open(itempath, "rb") as fp:
			contents = fp.read()

		self.db_sess.commit()

		return self.job.mimetype, fname, contents

	def getCacheState(self):
		assert self.fetched
		fetched = self.job.fetchtime
		if fetched is None:
			fetched = datetime.datetime.now()
		ago = datetime.datetime.now() - fetched
		return td_format(ago)


	def processRaw(self, content, mimetype='text/html', starturl='http://www.example.org'):

		# Abuse the fact that functions (including lambda) are fully formed objects
		job = lambda:None

		job.url       = self.url
		job.priority  = 9
		job.starturl  = "http://www.example.org"
		job.distance  = common.database.MAX_DISTANCE-2
		job.netloc    = urllib.parse.urlsplit(self.url).netloc
		fetcher       = self.archiver.fetcher(self.archiver.ruleset, target_url=job.url, start_url=job.starturl, db_sess=self.archiver.db_sess, job=job, cookie_lock=False)
		print(fetcher)
		ret          = fetcher.dispatchContent(content, "None", "text/html")
		content = ret['contents']
		content = utilities.replace_links(content)
		return content

	def dispatchRetreived(self, parentjob, content, mimetype):
		print("Dispatching prefetched content!")
		assert bool(content) == True
		self.archiver.synchronousDispatchPrefetched(self.url, parentjob, content, mimetype)


	def close(self):
		# WebMirror.runtime_engines.fetchers.put(self.archiver)
		self.archiver = None

	# def __del__(self):
	# 	if self.archiver != None:
	# 		print("ERROR! Archiver not released!")



def processRaw(content):
	page = RemoteContentObject("http://www.example.org")
	try:
		ret = page.processRaw(content)
	finally:
		page.close()

	return ret



def getPage(url, ignore_cache=False, version=None):

	assert not (version and ignore_cache)

	page = RemoteContentObject(url)

	if version:
		assert isinstance(version, int)

	try:
		page.fetch(ignore_cache, version)

		title      = page.getTitle()
		content    = page.getContent("/view?url=")
		cachestate = page.getCacheState()
	except DownloadException:
		title, content, cachestate = getErrorDiv()
	finally:
		page.close()


	if any([tmp.lower() in url.lower() for tmp in common.global_constants.GLOBAL_BAD_URLS]):

		bad_segs = [tmp for tmp in common.global_constants.GLOBAL_BAD_URLS if tmp.lower() in url.lower()]

		return (
				'Filtered',
				'Url %s is filtered by GLOBAL_BAD_URLS (%s)' % (url, bad_segs),
				'filtered',
			)

	return title, content, cachestate


@contextlib.contextmanager
def getPageRow(url, ignore_cache=False, session=None):
	page = RemoteContentObject(url, db_session=session)
	print("Page object: ", page)
	try:
		print("doing fetch: ")
		page.fetch(ignore_cache=ignore_cache)
		print("Fetched. Yielding")
		yield page

	except DownloadException:
		yield None
	finally:
		page.close()




def getResource(url, ignore_cache=False, session=None):
	'''
	Get a url that (probably) contains resource content synchronously.
	Return is a 4-tuple consisting of (mimetype, filename, filecontent, cache-state)
	'''


	if any([tmp.lower() in url.lower() for tmp in common.global_constants.GLOBAL_BAD_URLS]):

		bad_segs = [tmp for tmp in common.global_constants.GLOBAL_BAD_URLS if tmp.lower() in url.lower()]

		return (
				'text/ascii',
				'Url %s is filtered by GLOBAL_BAD_URLS (%s)' % (url, bad_segs),
				'Url %s is filtered by GLOBAL_BAD_URLS (%s)' % (url, bad_segs),
				'filtered',
			)

	page = RemoteContentObject(url, db_session=session)
	try:
		page.fetch(ignore_cache)

		mimetype, fname, content = page.getResource()
		cachestate               = page.getCacheState()
	finally:
		page.close()
	return mimetype, fname, content, cachestate

def processFetchedContent(url, content, mimetype, parentjob, db_session=None):

	page = RemoteContentObject(url, db_session=db_session)
	try:
		ret = page.dispatchRetreived(parentjob, content, mimetype)
	finally:
		page.close()

	return ret
