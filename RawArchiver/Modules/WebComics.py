
import urllib.parse
import RawArchiver.Modules.ModuleBase

class WebComicsRawModule(RawArchiver.Modules.ModuleBase.RawScraperModuleBase):

	module_name = "WebComicsRawModule"

	target_urls = [
		'http://somethingpositive.net',
		'http://www.girlgeniusonline.com',
	]

	target_tlds = [urllib.parse.urlparse(tmp).netloc for tmp in target_urls]

	@staticmethod
	def cares_about_url(cls, url):
		return urllib.parse.urlparse(url).netloc in cls.target_tlds

	@staticmethod
	def get_start_urls(cls):
		return [tmp for tmp in cls.target_urls]
