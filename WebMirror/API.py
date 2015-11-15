from app import app
import config
import datetime
import os.path
from config import relink_secret
import queue

from WebMirror.Engine import SiteArchiver
from WebMirror.Exceptions import DownloadException, getErrorDiv

# TODO: Pool of engines

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


fetchers = queue.Queue()

for x in range(3):
	fetchers.put(SiteArchiver(cookie_lock=False, run_filters=False))



class RemoteContentObject(object):
	def __init__(self, url):
		self.url     = url
		self.fetched = False
		self.job     = None
		print("RemoteContentObject instantiated. Available fetchers: %s" % fetchers.qsize())
		self.archiver = fetchers.get()


	def fetch(self, ignore_cache=False):
		self.fetched = True
		self.job     = self.archiver.synchronousJobRequest(self.url, ignore_cache)

		# print(self.job)

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


	def processRaw(self, content):

		# Abuse the fact that functions (including lambda) are fully formed objects
		job = lambda:None

		job.url      = "http://www.example.org"
		job.starturl = "http://www.example.org"
		fetcher      = self.archiver.fetcher(self.archiver.ruleset, job.url, job.starturl, cookie_lock=False)
		ret          = fetcher.dispatchContent(content, "None", "text/html")
		content = ret['contents']
		content = replace_links(content)
		return content

	def close(self):
		fetchers.put(self.archiver)
		self.archiver = None

	def __del__(self):
		if self.archiver != None:
			print("ERROR! Archiver not released!")



def processRaw(content):
	page = RemoteContentObject("http://www.example.org")
	try:
		ret = page.processRaw(content)
	finally:
		page.close()

	return ret



def getPage(url, ignore_cache=False):
	page = RemoteContentObject(url)

	try:
		page.fetch(ignore_cache)

		title      = page.getTitle()
		content    = page.getContent("/view?url=")
		cachestate = page.getCacheState()
	except DownloadException:
		title, content, cachestate = getErrorDiv()
	finally:
		page.close()

	return title, content, cachestate


def getResource(url, ignore_cache=False):
	page = RemoteContentObject(url)
	try:
		page.fetch(ignore_cache)

		mimetype, fname, content = page.getResource()
		cachestate               = page.getCacheState()
	finally:
		page.close()
	return mimetype, fname, content, cachestate
