from app import app
import config
import datetime
import os.path
import contextlib

import common.database
import WebMirror.Engine
# import WebMirror.runtime_engines
from common.Exceptions import DownloadException, getErrorDiv
from flask import g


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

def replace_links(content):
	rsc_key = "RESOURCE:{}".format(config.relink_secret).lower()
	ctnt_key = "CONTENT:{}".format(config.relink_secret).lower()

	content = content.replace(ctnt_key, "/view?url=")
	content = content.replace(rsc_key, "/render_rsc?url=")
	return content


class RemoteContentObject(object):
	def __init__(self, url, db_session = None):
		self.url     = url
		self.fetched = False
		self.job     = None

		if db_session:
			self.db_sess = db_session
		else:
			self.db_sess = g.session

		# print("RemoteContentObject instantiated. Available fetchers: %s" % WebMirror.runtime_engines.fetchers.qsize())
		# self.archiver = WebMirror.runtime_engines.fetchers.get()
		self.archiver = WebMirror.Engine.SiteArchiver(cookie_lock=False, run_filters=False, new_job_queue=None, db_interface=self.db_sess)


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
		if content:
			content = replace_links(content)
		return content

	def getResource(self):
		"""
		At this point, we have the page content, but we need to
		replace the url/resource keys with the proper paths
		so that the page will render properly
		"""
		assert self.fetched
		assert self.job.file

		itempath = os.path.join(app.config['RESOURCE_DIR'], self.job.file_item.fspath)
		fname = self.job.file_item.filename
		with open(itempath, "rb") as fp:
			contents = fp.read()
		return self.job.mimetype, fname, contents

	def getCacheState(self):
		assert self.fetched
		fetched = self.job.fetchtime
		ago = datetime.datetime.now() - fetched
		return td_format(ago)


	def processRaw(self, content, mimetype='text/html', starturl='http://www.example.org'):

		# Abuse the fact that functions (including lambda) are fully formed objects
		job = lambda:None

		job.url       = self.url
		job.starturl  = "http://www.example.org"
		job.distance  = common.database.MAX_DISTANCE-2
		fetcher       = self.archiver.fetcher(self.archiver.ruleset, target_url=job.url, start_url=job.starturl, db_sess=self.archiver.db_sess, job=job, cookie_lock=False)
		print(fetcher)
		ret          = fetcher.dispatchContent(content, "None", "text/html")
		content = ret['contents']
		content = replace_links(content)
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

	return title, content, cachestate


@contextlib.contextmanager
def getPageRow(url):
	page = RemoteContentObject(url)

	try:
		page.fetch(ignore_cache=False)

		yield page
	except DownloadException:
		yield None
	finally:
		page.close()




def getResource(url, ignore_cache=False):
	'''
	Get a url that (probably) contains resource content synchronously.
	Return is a 4-tuple consisting of (mimetype, filename, filecontent, cache-state)
	'''
	page = RemoteContentObject(url)
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
