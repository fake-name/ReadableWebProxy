from app import app
import config
import os.path
from config import relink_secret

from WebMirror.Engine import SiteArchiver

class RemoteContentObject(object):
	def __init__(self, url):
		self.url = url
		self.fetched = False

		self.archiver = SiteArchiver()


	def fetch(self):
		self.fetched = True
		self.job = self.archiver.synchronousJobRequest(self.url)
		print(self.job)

	def getTitle(self):
		assert self.fetched
		return self.job.title

	def getContent(self, relink_key, relink_replace):
		"""
		At this point, we have the page content, but we need to
		replace the url/resource keys with the proper paths
		so that the page will render properly
		"""
		assert self.fetched


		content = self.job.content
		if content:
			rsc_key = "RESOURCE:{}".format(config.relink_secret).lower()
			ctnt_key = "CONTENT:{}".format(config.relink_secret).lower()

			content = content.replace(ctnt_key, "/view?url=")
			content = content.replace(rsc_key, "/render_rsc?url=")

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


def getPage(url):
	page = RemoteContentObject(url)

	page.fetch()

	title      = page.getTitle()
	content    = page.getContent(relink_secret, "/view?url=")
	cachestate = page.getCacheState()

	return title, content, cachestate


def getResource(url):
	page = RemoteContentObject(url)

	page.fetch()

	mimetype, fname, content = page.getResource()
	cachestate        = page.getCacheState()

	return mimetype, fname, content, cachestate
