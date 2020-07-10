
import urllib.parse
import RawArchiver.ModuleBase

class ElscioneRawModule(RawArchiver.ModuleBase.RawScraperModuleBase):

	module_name = "MiscRawModule"

	target_urls = [
		'https://server.elscione.com/',
	]

	target_tlds = [urllib.parse.urlparse(tmp).netloc for tmp in target_urls]

	badwords = [
		'server.elscione.com/Music/',
		'server.elscione.com/Anime/',


	]

	@classmethod
	def cares_about_url(cls, url):
		if any([badword in url for badword in cls.badwords]):
			return False

		if RawArchiver.ModuleBase.duplicate_path_fragments(url):
			return False
		return urllib.parse.urlparse(url).netloc in cls.target_tlds

	@classmethod
	def get_start_urls(cls):
		return [tmp for tmp in cls.target_urls]


	@staticmethod
	def get_max_active_jobs():
		return 5
