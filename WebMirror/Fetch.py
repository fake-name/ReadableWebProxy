

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import WebMirror.rules
import WebMirror.LogBase as LogBase

import datetime


import WebMirror.processor.HtmlProcessor
import WebMirror.processor.GDriveDirProcessor
import WebMirror.processor.GDocProcessor
import WebMirror.processor.MarkdownProcessor

import WebMirror.util.urlFuncs as url_util
import urllib.parse
import traceback
import WebMirror.util.webFunctions as webFunctions
import bs4

import WebMirror.processor.ProcessorBase



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


PLUGINS = [
	WebMirror.processor.HtmlProcessor.HtmlPageProcessor,
	WebMirror.processor.GDriveDirProcessor.GDriveDirProcessor,
	WebMirror.processor.GDocProcessor.GdocPageProcessor,
	WebMirror.processor.MarkdownProcessor.MarkdownProcessor,
]

class ItemFetcher(LogBase.LoggerMixin):


	loggerPath = "Main.SiteArchiver"



	# Fetch items up to 1,000,000 (1 million) links away from the root source
	# This (functionally) equates to no limit.
	# The db defaults to  (e.g. max signed integer value) anyways
	FETCH_DISTANCE = 1000 * 1000

	def __init__(self, rules, job):
		# print("Fetcher init()")
		super().__init__()

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

		baseRules = [ruleset for ruleset in rules if ruleset['netlocs'] == None].pop(0)

		rules = [ruleset for ruleset in rules if ruleset['netlocs'] != None]
		rules.sort(key=lambda x:x['netlocs'])

		self.ruleset = rules

		self.relinkable = set()
		for item in self.ruleset:
			[self.relinkable.add(url) for url in item['fileDomains']]         #pylint: disable=W0106
			[self.relinkable.add(url) for url in item['netlocs']]             #pylint: disable=W0106


		netloc = urllib.parse.urlsplit(job.url).netloc

		self.rules = None
		for ruleset in self.ruleset:
			if netloc in ruleset['netlocs']:
				self.log.info("Found specific ruleset!")
				self.rules = ruleset

		if not self.rules:
			self.log.warn("Using base ruleset!")
			self.rules = baseRules


		assert self.rules

		self.job = job

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
		return {'plainLinks' : [], 'rsrcLinks' : []}


	def processHtmlPage(self, url, content):
		scraper = WebMirror.processor.HtmlProcessor.HtmlPageProcessor(
									pageUrl         = url,
									pgContent       = content,
									baseUrls        = self.job.starturl,
									loggerPath      = self.loggerPath,
									badwords        = self.rules['badwords'],
									decompose       = self.rules['decompose'],
									decomposeBefore = self.rules['decomposeBefore'],
									fileDomains     = self.rules['fileDomains'],
									allImages       = self.rules['allImages'],
									ignoreBadLinks  = self.rules['IGNORE_MALFORMED_URLS'],
									stripTitle      = self.rules['stripTitle'],
									relinkable      = self.relinkable
								)
		extracted = scraper.extractContent()
		# print(extracted)
		return extracted


# 	def processReturnedFileResources(self, resources):

# 		# fMap = {}


# 		for fName, mimeType, content, fHash in resources:
# 			# m = hashlib.md5()
# 			# m.update(content)
# 			# fHash = m.hexdigest()

# 			hashName = self.tableKey+fHash

# 			# fMap[fName] = fHash

# 			fName = os.path.split(fName)[-1]

# 			self.log.info("Resource = '%s', '%s', '%s'", fName, mimeType, hashName)
# 			if mimeType in ["image/gif", "image/jpeg", "image/pjpeg", "image/png", "image/svg+xml", "image/vnd.djvu"]:
# 				self.log.info("Processing resource '%s' as an image file. (mimetype: %s)", fName, mimeType)
# 				self.upsert(hashName, istext=False)
# 				self.saveFile(hashName, mimeType, fName, content)
# 			elif mimeType in ["application/octet-stream"]:
# 				self.log.info("Processing '%s' as an binary file.", fName)
# 				self.upsert(hashName, istext=False)
# 				self.saveFile(hashName, mimeType, fName, content)
# 			else:
# 				self.log.warn("Unknown MIME Type? '%s', FileName: '%s'", mimeType, fName)

# 		if len(resources) == 0:
# 			self.log.info("File had no resource content!")




	# def extractGoogleDriveFolder(self, url):
	# 	scraper = self.gdriveClass(
	# 								pageUrl         = url,
	# 								loggerPath      = self.loggerPath,
	# 								relinkable      = self.relinkable
	# 							)
	# 	extracted = scraper.extractContent()
	# 	return extracted


# 	def retreiveGoogleDoc(self, url):
# 		# pageUrl, loggerPath, tableKey, scannedDomains=None, tlds=None

# 		try:
# 			scraper = self.gDocClass(
# 										pageUrl         = url,
# 										loggerPath      = self.loggerPath,
# 										tableKey        = self.tableKey,
# 										scannedDomains  = self.baseUrl,
# 										tlds            = self.tld,
# 										relinkable      = self.relinkable
# 									)
# 			extracted, resources = scraper.extractContent()
# 			self.processReturnedFileResources(resources)
# 		except TextScrape.gDocParse.CannotAccessGDocException:
# 			self.log.warning("Cannot access google doc content. Attempting to access as a plain HTML resource via /pub interface")
# 			url = url + "/pub"
# 			extracted = self.retreivePlainResource(url)
# 			if "This document is not published." in extracted['contents']:
# 				raise ValueError("Could not extract google document!")

# 		return extracted

# 	def processAsMarkdown(self, url, content):
# 		pbLut = getattr(self, 'pasteBinLut', {})

# 		scraper = self.markdownClass(
# 									pageUrl         = url,
# 									loggerPath      = self.loggerPath,
# 									content         = content,
# 									pbLut           = pbLut
# 								)
# 		extracted = scraper.extractContent()

# 		return extracted

# 	def retreiveGoogleFile(self, url):


# 		self.log.info("Should fetch google file at '%s'", url)
# 		doc = gdp.GFileExtractor(url)

# 		attempts = 0

# 		while 1:
# 			attempts += 1
# 			try:
# 				content, fName, mType = doc.extract()
# 			except TypeError:
# 				self.log.critical('Extracting item failed!')
# 				for line in traceback.format_exc().strip().split("\n"):
# 					self.log.critical(line.strip())
# 				return self.getEmptyRet()
# 			if content:
# 				break
# 			if attempts > 3:
# 				raise DownloadException


# 			self.log.error("No content? Retrying!")

# 		scraper = self.htmlProcClass(
# 									baseUrls        = self.baseUrl,
# 									pageUrl         = url,
# 									pgContent       = content,
# 									loggerPath      = self.loggerPath,
# 									badwords        = self.badwords,
# 									decompose       = self.decompose,
# 									decomposeBefore = self.decomposeBefore,
# 									fileDomains     = self.fileDomains,
# 									allImages       = self.allImages,
# 									followGLinks    = self.FOLLOW_GOOGLE_LINKS,
# 									ignoreBadLinks  = self.IGNORE_MALFORMED_URLS,
# 									tld             = self.tld,
# 									stripTitle      = self.stripTitle
# 								)
# 		extracted = scraper.extractContent()

# 		return extracted


# 		raise NotImplementedError("TODO: FIX ME!")



		# with self.transaction() as cur:
		# 	cur.execute("SELECT fspath  FROM {tableName} WHERE fhash=%s;".format(tableName=self.tableName), (fHash, ))
		# 	row = cur.fetchone()
		# 	if row:
		# 		self.log.info("Already downloaded file. Not creating duplicates.")
		# 		hadFile = True
		# 		fqPath = row[0]

		# with self.transaction() as cur:

		# 	cur.execute("SELECT dbid, fspath, contents, mimetype  FROM {tableName} WHERE url=%s;".format(tableName=self.tableName), (url, ))
		# 	row = cur.fetchone()
		# 	if not row:
		# 		self.log.critical("Failure when saving file for URL '%s'", url)
		# 		self.log.critical("File name: '%s'", fileName)
		# 		return

		# 	dbid, dummy_havePath, dummy_haveCtnt, dummy_haveMime = row
		# 	# self.log.info('havePath, haveCtnt, haveMime - %s, %s, %s', havePath, haveCtnt, haveMime)

		# 	if not hadFile:
		# 		fqPath = self.getFilenameFromIdName(dbid, fileName)

		# 	newRowDict = {  "dlstate" : 2,
		# 					"series"  : None,
		# 					"contents": len(content),
		# 					"istext"  : False,
		# 					"mimetype": mimetype,
		# 					"fspath"  : fqPath,
		# 					"fhash"   : fHash}


		# self.updateDbEntry(url=url, commit=False, **newRowDict)


		# if not hadFile:
		# 	try:
		# 		with open(fqPath, "wb") as fp:
		# 			fp.write(content)
		# 	except OSError:
		# 		self.log.error("Error when attempting to save file. ")
		# 		with self.transaction() as cur:
		# 			newRowDict = {"dlstate" : -1}
		# 			self.updateDbEntry(url=url, commit=False, **newRowDict)



# 	########################################################################################################################
# 	#
# 	#	##     ## #### ##     ## ########         ######## ##    ## ########  ########
# 	#	###   ###  ##  ###   ### ##                  ##     ##  ##  ##     ## ##
# 	#	#### ####  ##  #### #### ##                  ##      ####   ##     ## ##
# 	#	## ### ##  ##  ## ### ## ######   #######    ##       ##    ########  ######
# 	#	##     ##  ##  ##     ## ##                  ##       ##    ##        ##
# 	#	##     ##  ##  ##     ## ##                  ##       ##    ##        ##
# 	#	##     ## #### ##     ## ########            ##       ##    ##        ########
# 	#
# 	#	########  ####  ######  ########     ###    ########  ######  ##     ## ######## ########
# 	#	##     ##  ##  ##    ## ##     ##   ## ##      ##    ##    ## ##     ## ##       ##     ##
# 	#	##     ##  ##  ##       ##     ##  ##   ##     ##    ##       ##     ## ##       ##     ##
# 	#	##     ##  ##   ######  ########  ##     ##    ##    ##       ######### ######   ########
# 	#	##     ##  ##        ## ##        #########    ##    ##       ##     ## ##       ##   ##
# 	#	##     ##  ##  ##    ## ##        ##     ##    ##    ##    ## ##     ## ##       ##    ##
# 	#	########  ####  ######  ##        ##     ##    ##     ######  ##     ## ######## ##     ##
# 	#
# 	########################################################################################################################



	def plugin_dispatch(self, plugin, url, content, fName, mimeType):
		self.log.info("Dispatching file '%s' with mime-type '%s'", fName, mimeType)



		params = {
									'pageUrl'         : url,
									'pgContent'       : content,
									'mimeType'        : mimeType,
									'baseUrls'        : self.job.starturl,
									'loggerPath'      : self.loggerPath,
									'badwords'        : self.rules['badwords'],
									'decompose'       : self.rules['decompose'],
									'decomposeBefore' : self.rules['decomposeBefore'],
									'fileDomains'     : self.rules['fileDomains'],
									'allImages'       : self.rules['allImages'],
									'ignoreBadLinks'  : self.rules['IGNORE_MALFORMED_URLS'],
									'stripTitle'      : self.rules['stripTitle'],
									'relinkable'      : self.relinkable
		}

		ret = plugin.process(params)
		return ret

		# if mimeType in ['text/html']:
		# 	ret = self.processHtmlPage(url, content)

		# elif mimeType in ['text/plain']:
		# 	ret = self.processAsMarkdown(url, content)

		# elif mimeType in ['text/xml', 'text/atom+xml', 'application/atom+xml', 'application/xml', 'text/css', 'application/x-javascript', 'application/javascript']:

		# 	if mimeType in ['text/xml', 'text/atom+xml', 'application/atom+xml', 'application/xml']:
		# 		self.log.info("XML File?")
		# 		self.log.info("URL: '%s'", url)

		# 	elif mimeType in ['text/css']:
		# 		self.log.info("CSS!")
		# 		self.log.info("URL: '%s'", url)

		# 	elif mimeType in ['application/x-javascript', 'application/javascript']:
		# 		self.log.info("Javascript Resource!")
		# 		self.log.info("URL: '%s'", url)

		# 	assert self.job.url == url
		# 	self.job.title    = ''
		# 	self.job.contents = content
		# 	self.job.mimetype = mimeType
		# 	self.job.state    = 'complete'
		# 	self.job.is_text  = True
		# 	return self.getEmptyRet()




		# elif mimeType in ["image/gif", "image/jpeg", "image/pjpeg", "image/png", "image/svg+xml", "image/vnd.djvu",
		# 	"application/octet-stream", "application/x-mobipocket-ebook", "application/pdf", "application/zip"]:
		# 	if mimeType in ["image/gif", "image/jpeg", "image/pjpeg", "image/png", "image/svg+xml", "image/vnd.djvu"]:
		# 		self.log.info("Processing '%s' as an image file.", url)
		# 	elif mimeType in ["application/octet-stream", "application/x-mobipocket-ebook", "application/pdf", "application/zip"]:
		# 		self.log.info("Processing '%s' as an binary file.", url)

		# 	# self.saveFile(url, mimeType, fName, content)
		# 	ret = {"file" : True, "url" : url, "mimeType" : mimeType, "fName" : fName, "content" : content}
		# 	return ret


		# else:
		# 	self.log.error("Unknown MIME Type: '%s', Url: '%s'", mimeType, url)
		# 	self.log.error("Not saving file!")
		# 	return self.getEmptyRet()






	# def retreivePlainResource(self, job):
	# 	self.log.info("Fetching Simple Resource: '%s'", job.url)
	# 	try:
	# 		content, fName, mimeType = self.getItem(self.job.url)
	# 	except ValueError:

	# 		for line in traceback.format_exc().split("\n"):
	# 			self.log.critical(line)
	# 		job.state = "error"
	# 		job.errno = -1

	# 		return self.getEmptyRet()

	# 	return self.dispatchContent(job.url, content, fName, mimeType)




	def getItem(self, itemUrl):

		try:
			content, handle = self.wg.getpage(itemUrl, returnMultiple=True)
		except:
			if self.rules['cloudflare']:
				if not self.wg.stepThroughCloudFlare(itemUrl, titleNotContains='Just a moment...'):
					raise ValueError("Could not step through cloudflare!")
				# Cloudflare cookie set, retrieve again
				content, handle = self.wg.getpage(itemUrl, returnMultiple=True)
			else:
				raise



		if not content or not handle:
			raise ValueError("Failed to retreive file from page '%s'!" % itemUrl)

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
		self.job.url = url_util.urlClean(self.job.url)

		print('Dispatch URL', self.job.url)
		keys = list(self.plugin_modules.keys())
		keys.sort(reverse=True)
		print(keys)

		content, fName, mimeType = self.getItem(self.job.url)


		for key in keys:
			for plugin in self.plugin_modules[key]:
				if mimeType.lower() in plugin.wanted_mimetypes and plugin.wantsUrl(self.job.url):
					print("plugin", plugin, "wants", self.job.url)
					return self.plugin_dispatch(plugin, self.job.url, content, fName, mimeType)


		self.log.error("Did not know how to dispatch request for url: '%s', mimetype: '%s'!", self.job.url, mimeType)
		return self.getEmptyRet()

		# self.upsertResponseLinks(job, response)
