
import abc

class RawScraperModuleBase(metaclass=abc.ABCMeta):
	'''
	The interface contract for a scraper module is very simple.

	Basically, it just involves three parameters. The module name, as a class
	attribute, and two static methods.

	`cares_about_url()` takes a url parameter, and returns a boolean containing
	whether the module thinks it wants that URL. This is used to screen new URLs
	as to whether they should be scraped.

	`get_start_urls()` should return a list of URLs to pre-populate the "should crawl"
	page list.

	------

	Additional functionality can be added via two additional classmethods, that are
	optional.

	`check_prefetch()` is called before each fetch for `url`, using webget instance
	`wg`. This is intended to allow things like validating login state in the web
	get instance, and other such functionality.
	A return of `True` means everything is OK, a return of `False` means the prefetch
	check cannot get the WebGet instance into the required state, for whatever reason.


	`check_postfetch()` is called once content has been fetched, with the associated
	data and metadata for the fetch (`url, wg, fname, fcontent, fmimetype`). This is
	intended to allow the module to modify the content or metadata before it is
	fed through the link extraction system/saved-to-disk. It can also allow more
	banal operations such as clarifying filenames.
	Return value is a 3-tuple `(fname, fcontent, fmimetype)`

	'''

	rewalk_interval = 90

	@abc.abstractproperty
	def module_name(self):
		pass

	@classmethod
	@abc.abstractmethod
	def cares_about_url(cls, url):
		pass

	@classmethod
	@abc.abstractmethod
	def get_start_urls(cls):
		pass

	@classmethod
	def check_prefetch(cls, url, wg):
		return True

	@classmethod
	def single_thread_fetch(cls, url):
		return False

	@classmethod
	def check_postfetch(cls, url, wg, fname, fcontent, fmimetype):
		return fname, fcontent, fmimetype
