
import WebMirror.database
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

	def getTitle(self):
		assert self.fetched
		return "haaaaai"

	def getContent(self, relink_key, relink_replace):
		assert self.fetched
		return "wat"

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
