from app import app
import config
import os.path
from config import relink_secret

from WebMirror.Engine import SiteArchiver

def replace_links(content):
	rsc_key = "RESOURCE:{}".format(config.relink_secret).lower()
	ctnt_key = "CONTENT:{}".format(config.relink_secret).lower()

	content = content.replace(ctnt_key, "/view?url=")
	content = content.replace(rsc_key, "/render_rsc?url=")
	return content

class RemoteContentObject(object):
	def __init__(self, url):
		self.url = url
		self.fetched = False

		self.archiver = SiteArchiver(cookie_lock=False, run_filters=False)


	def fetch(self, ignore_cache=False):
		self.fetched = True
		self.job = self.archiver.synchronousJobRequest(self.url, ignore_cache)

		# print(self.job)

	def getTitle(self):
		assert self.fetched
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
		return "hurp durp"


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


def processRaw(content):
	page = RemoteContentObject("http://www.example.org")
	return page.processRaw(content)



def getPage(url, ignore_cache=False):
	page = RemoteContentObject(url)

	page.fetch(ignore_cache)

	title      = page.getTitle()
	content    = page.getContent("/view?url=")
	cachestate = page.getCacheState()

	return title, content, cachestate


def getResource(url, ignore_cache=False):
	page = RemoteContentObject(url)

	page.fetch(ignore_cache)

	mimetype, fname, content = page.getResource()
	cachestate        = page.getCacheState()

	return mimetype, fname, content, cachestate
