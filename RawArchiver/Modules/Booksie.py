
import urllib.parse
import RawArchiver.ModuleBase

class BooksieRawModule(RawArchiver.ModuleBase.RawScraperModuleBase):

	module_name = "BooksieRawModule"

	target_urls = [
		'http://www.booksie.com/',
	]

	target_tlds = [urllib.parse.urlparse(tmp).netloc for tmp in target_urls]

	badwords = [
			"/poetry",
			"/poetry/",
			"/users/",
			"/rss/",
			"/writers",
			"/pdf/",

			'/bookshelf-recommended/',
			'/member/connect?',
			'_USER_PROFILE__',
			'_MEDIA_IMAGE__120x120.',
			# Booksie tags can apparently nest arbitrarily, so
			# they basically take over the scraper if left unchecked.
			"/tags/",

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
