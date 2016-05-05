

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import WebMirror.rules
import WebMirror.LogBase as LogBase


import WebMirror.util.urlFuncs as url_util
import urllib.parse
import WebMirror.util.webFunctions as webFunctions
import bs4

import WebMirror.processor.ProcessorBase

from activePlugins import PREPROCESSORS
from activePlugins import PLUGINS

from WebMirror.Exceptions import DownloadException

########################################################################################################################
#
#	##     ##    ###    #### ##    ##     ######  ##          ###     ######   ######
#	###   ###   ## ##    ##  ###   ##    ##    ## ##         ## ##   ##    ## ##    ##
#	#### ####  ##   ##   ##  ####  ##    ##       ##        ##   ##  ##       ##
#	## ### ## ##     ##  ##  ## ## ##    ##       ##       ##     ##  ######   ######
#	##     ## #########  ##  ##  ####    ##       ##       #########       ##       ##
#	##     ## ##     ##  ##  ##   ###    ##    ## ##       ##     ## ##    ## ##    ##
#	##     ## ##     ## #### ##    ##     ######  ######## ##     ##  ######   ######
#
########################################################################################################################

class ItemFetcher(LogBase.LoggerMixin):


	loggerPath = "Main.SiteArchiver"



	# Fetch items up to 1,000,000 (1 million) links away from the root source
	# This (functionally) equates to no limit.
	# The db defaults to  (e.g. max signed integer value) anyways
	FETCH_DISTANCE = 1000 * 1000

	def __init__(self, rules, target_url, db_sess, start_url, job, cookie_lock=None, wg_handle=None, response_queue=None):
		# print("Fetcher init()")
		super().__init__()

		self.response_queue = response_queue
		self.job            = job
		self.db_sess        = db_sess

		if wg_handle:
			self.wg = wg_handle
		elif cookie_lock:
			self.wg = webFunctions.WebGetRobust(cookie_lock=cookie_lock)
		else:
			self.wg = webFunctions.WebGetRobust()

		# Validate the plugins implement the proper interface
		for item in PLUGINS:
			assert issubclass(item, WebMirror.processor.ProcessorBase.PageProcessor), "Item '%s' does not inherit from '%s'" % (item, WebMirror.processor.ProcessorBase.PageProcessor)


		self.plugin_modules = {}
		for item in PLUGINS:
			key = item.want_priority
			if key in self.plugin_modules:
				self.plugin_modules[key].append(item)
			else:
				self.plugin_modules[key] = [item]



		self.preprocessor_modules = []
		for item in PREPROCESSORS:
			self.preprocessor_modules.append(item)

		baseRules = [ruleset for ruleset in rules if ruleset['netlocs'] == None].pop(0)

		rules = [ruleset for ruleset in rules if ruleset['netlocs'] != None]
		rules.sort(key=lambda x:x['netlocs'])

		self.ruleset = rules

		netloc = urllib.parse.urlsplit(target_url).netloc

		self.rules = None
		for ruleset in self.ruleset:
			if netloc in ruleset['netlocs']:
				# self.log.info("Found specific ruleset!")
				self.rules = ruleset

		if not self.rules:
			self.log.warn("Using base ruleset for URL: '%s'!", target_url)
			self.rules = baseRules


		assert self.rules

		self.target_url = target_url
		self.start_url = start_url

	########################################################################################################################



	########################################################################################################################
	#
	#	########  ####  ######  ########     ###    ########  ######  ##     ##      ##     ## ######## ######## ##     ##  #######  ########   ######
	#	##     ##  ##  ##    ## ##     ##   ## ##      ##    ##    ## ##     ##      ###   ### ##          ##    ##     ## ##     ## ##     ## ##    ##
	#	##     ##  ##  ##       ##     ##  ##   ##     ##    ##       ##     ##      #### #### ##          ##    ##     ## ##     ## ##     ## ##
	#	##     ##  ##   ######  ########  ##     ##    ##    ##       #########      ## ### ## ######      ##    ######### ##     ## ##     ##  ######
	#	##     ##  ##        ## ##        #########    ##    ##       ##     ##      ##     ## ##          ##    ##     ## ##     ## ##     ##       ##
	#	##     ##  ##  ##    ## ##        ##     ##    ##    ##    ## ##     ##      ##     ## ##          ##    ##     ## ##     ## ##     ## ##    ##
	#	########  ####  ######  ##        ##     ##    ##     ######  ##     ##      ##     ## ########    ##    ##     ##  #######  ########   ######
	#
	########################################################################################################################



	def getEmptyRet(self):
		return {
			'plainLinks' : [],
			'rsrcLinks'  : [],

			'title'      : "Error: Unknown dispatch type",
			'contents'   : "Error. Could not dispatch properly",
			'mimeType'   : "text/html",
			}



	def plugin_dispatch(self, plugin, url, content, fName, mimeType, no_ret=False):
		self.log.info("Dispatching file '%s' with mime-type '%s'", fName, mimeType)
		assert isinstance(content, (str, bytes)) , "Content must be a string/bytes. It's currently type: '%s'" % type(content)


		params = {
									'pageUrl'         : url,
									'pgContent'       : content,
									'mimeType'        : mimeType,
									'db_sess'         : self.db_sess,
									'baseUrls'        : self.start_url,
									'fileDomains'     : self.rules['fileDomains'],
									'ignoreBadLinks'  : self.rules['IGNORE_MALFORMED_URLS'],
									'type'            : self.rules['type'],
									'job'             : self.job,
		}

		ret = plugin.process(params)

		if no_ret:
			return

		assert ret != None, "Return from %s was None!" % plugin
		assert "mimeType" in ret or "file" in ret, "Neither mimetype or file in ret for url '%s', plugin '%s'" % (url, plugin)

		return ret





	def getItem(self, itemUrl):

		try:
			content, handle = self.wg.getpage(itemUrl, returnMultiple=True)
		except:
			print("Failure?")
			if self.rules['cloudflare']:
				if not self.wg.stepThroughCloudFlare(itemUrl, titleNotContains='Just a moment...'):
					raise ValueError("Could not step through cloudflare!")
				# Cloudflare cookie set, retrieve again
				content, handle = self.wg.getpage(itemUrl, returnMultiple=True)
			else:
				raise



		if not content or not handle:
			raise DownloadException("Failed to retreive file from page '%s'!" % itemUrl)

		fileN = urllib.parse.unquote(urllib.parse.urlparse(handle.geturl())[2].split("/")[-1])
		fileN = bs4.UnicodeDammit(fileN).unicode_markup
		mType = handle.info()['Content-Type']

		# If there is an encoding in the content-type (or any other info), strip it out.
		# We don't care about the encoding, since WebFunctions will already have handled that,
		# and returned a decoded unicode object.
		if mType and ";" in mType:
			mType = mType.split(";")[0].strip()

		# *sigh*. So minus.com is fucking up their http headers, and apparently urlencoding the
		# mime type, because apparently they're shit at things.
		# Anyways, fix that.
		if '%2F' in  mType:
			mType = mType.replace('%2F', '/')

		self.log.info("Retreived file of type '%s', name of '%s' with a size of %0.3f K", mType, fileN, len(content)/1000.0)
		return content, fileN, mType



	def dispatchContent(self, content, fName, mimeType):
		assert bool(content) == True

		# Do preprocessing:
		preprocess_counts = 0
		for filter_plg in self.preprocessor_modules:
			if filter_plg.wantsUrl(self.target_url):
				content = filter_plg.preprocess(self.target_url, mimeType, content, self.wg)
				preprocess_counts += 1

		if preprocess_counts > 1:
			raise ValueError("Multiple preprocess executions for the same content (%s, %s, %s). Wat?" % (self.target_url, self.fName, self.mimeType))

		# Then actually process it.
		keys = list(self.plugin_modules.keys())
		keys.sort(reverse=True)

		for key in keys:
			for plugin in self.plugin_modules[key]:
				if mimeType.lower() in plugin.wanted_mimetypes and \
						plugin.wantsUrl(self.target_url)       and \
						plugin.wantsFromContent(content):
					# print("plugin", plugin, "wants", self.target_url)
					ret = self.plugin_dispatch(plugin, self.target_url, content, fName, mimeType)
					if not "file" in ret:
						ret['rawcontent'] = content
					return ret

		self.log.error("Did not know how to dispatch request for url: '%s', mimetype: '%s'!", self.target_url, mimeType)
		return self.getEmptyRet()

	########################################################################################################################
	#
	#	########    ###     ######  ##    ##    ########  ####  ######  ########     ###    ########  ######  ##     ## ######## ########
	#	   ##      ## ##   ##    ## ##   ##     ##     ##  ##  ##    ## ##     ##   ## ##      ##    ##    ## ##     ## ##       ##     ##
	#	   ##     ##   ##  ##       ##  ##      ##     ##  ##  ##       ##     ##  ##   ##     ##    ##       ##     ## ##       ##     ##
	#	   ##    ##     ##  ######  #####       ##     ##  ##   ######  ########  ##     ##    ##    ##       ######### ######   ########
	#	   ##    #########       ## ##  ##      ##     ##  ##        ## ##        #########    ##    ##       ##     ## ##       ##   ##
	#	   ##    ##     ## ##    ## ##   ##     ##     ##  ##  ##    ## ##        ##     ##    ##    ##    ## ##     ## ##       ##    ##
	#	   ##    ##     ##  ######  ##    ##    ########  ####  ######  ##        ##     ##    ##     ######  ##     ## ######## ##     ##
	#
	########################################################################################################################

	# This is the main function that's called by the task management system.
	# Retreive remote content at `url`, call the appropriate handler for the
	# transferred content (e.g. is it an image/html page/binary file)
	def fetch(self):
		self.target_url = url_util.urlClean(self.target_url)


		content, fName, mimeType = self.getItem(self.target_url)

		return self.dispatchContent(content, fName, mimeType)


		# self.upsertResponseLinks(job, response)
