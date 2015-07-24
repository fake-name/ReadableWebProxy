

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import WebMirror.rules
import LogBase
import runStatus
import time

import multiprocessing
from sqlalchemy import desc


import WebMirror.processor.HtmlProcessor
import WebMirror.processor.GDriveDirProcessor
import WebMirror.processor.GDocProcessor

import WebMirror.util.urlFuncs
import urllib.parse
import traceback
import webFunctions
import bs4

MAX_DISTANCE = 1000 * 1000

# import sql.operators as sqlo

# import TextScrape.urlFuncs
# import inspect
# import collections
# import queue
# import bs4
# from concurrent.futures import ThreadPoolExecutor


# import os.path
# import os

import TextScrape.gDocParse as gdp

class DownloadException(Exception):
	pass

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

	threads = 2

	# Fetch items up to 1,000,000 (1 million) links away from the root source
	# This (functionally) equates to no limit.
	# The db defaults to  (e.g. max signed integer value) anyways
	FETCH_DISTANCE = 1000 * 1000

	def __init__(self, rules, job):
		super().__init__()

		self.wg = webFunctions.WebGetRobust()

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
				self.rules = ruleset
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
									baseUrls        = self.job.starturl,
									pageUrl         = url,
									pgContent       = content,
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




	def extractGoogleDriveFolder(self, url):
		scraper = self.gdriveClass(
									pageUrl         = url,
									loggerPath      = self.loggerPath,
									relinkable      = self.relinkable
								)
		extracted = scraper.extractContent()
		return extracted


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



	def dispatchContent(self, url, content, fName, mimeType):
		self.log.info("Dispatching file '%s' with mime-type '%s'", fName, mimeType)

		# *sigh*. So minus.com is fucking up their http headers, and apparently urlencoding the
		# mime type, because apparently they're shit at things.
		# Anyways, fix that.
		if '%2F' in  mimeType:
			mimeType = mimeType.replace('%2F', '/')

		if mimeType in ['text/xml', 'text/atom+xml', 'application/atom+xml', 'application/xml', 'text/css', 'application/x-javascript', 'application/javascript']:

			if mimeType in ['text/xml', 'text/atom+xml', 'application/atom+xml', 'application/xml']:
				self.log.info("XML File?")
				self.log.info("URL: '%s'", url)

			elif mimeType in ['text/css']:
				self.log.info("CSS!")
				self.log.info("URL: '%s'", url)

			elif mimeType in ['application/x-javascript', 'application/javascript']:
				self.log.info("Javascript Resource!")
				self.log.info("URL: '%s'", url)

			assert self.job.url == url
			self.job.title    = ''
			self.job.contents = content
			self.job.mimetype = mimeType
			self.job.state    = 'complete'
			self.job.is_text  = True
			return self.getEmptyRet()




		elif mimeType in ["image/gif", "image/jpeg", "image/pjpeg", "image/png", "image/svg+xml", "image/vnd.djvu",
			"application/octet-stream", "application/x-mobipocket-ebook", "application/pdf", "application/zip"]:
			if mimeType in ["image/gif", "image/jpeg", "image/pjpeg", "image/png", "image/svg+xml", "image/vnd.djvu"]:
				self.log.info("Processing '%s' as an image file.", url)
			elif mimeType in ["application/octet-stream", "application/x-mobipocket-ebook", "application/pdf", "application/zip"]:
				self.log.info("Processing '%s' as an binary file.", url)

			self.saveFile(url, mimeType, fName, content)
			return self.getEmptyRet()


		elif mimeType in ['text/html']:
			ret = self.processHtmlPage(url, content)

		elif mimeType in ['text/plain']:
			ret = self.processAsMarkdown(url, content)

		else:
			self.log.error("Unknown MIME Type: '%s', Url: '%s'", mimeType, url)
			self.log.error("Not saving file!")
			return self.getEmptyRet()


		return ret




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


		self.log.info("Retreived file of type '%s', name of '%s' with a size of %0.3f K", mType, fileN, len(content)/1000.0)
		return content, fileN, mType


	def retreivePlainResource(self, job):
		self.log.info("Fetching Simple Resource: '%s'", job.url)
		try:
			content, fName, mimeType = self.getItem(self.job.url)
		except ValueError:

			for line in traceback.format_exc().split("\n"):
				self.log.critical(line)
			job.state = "error"
			job.errno = -1

			return self.getEmptyRet()

		return self.dispatchContent(job.url, content, fName, mimeType)








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
		self.job.url = WebMirror.util.urlFuncs.urlClean(self.job.url)

		# print('Dispatch URL', url)

		netloc = urllib.parse.urlsplit(self.job.url.lower()).netloc

		isGdoc,  realUrl = gdp.isGdocUrl(self.job.url)
		isGfile, fileUrl = gdp.isGFileUrl(self.job.url)

		# print('Fetching: ', self.job.url, 'distance', self.job.distance)
		# print(isGdoc, isGfile)
		if 'drive.google.com' in netloc:
			self.log.info("Google Drive content!")
			response = self.extractGoogleDriveFolder(self.job)
		elif isGdoc:
			self.log.info("Google Docs content!")
			response = self.retreiveGoogleDoc(self.job, realUrl)
		elif isGfile:
			self.log.info("Google File content!")
			response = self.retreiveGoogleFile(self.job, realUrl)

		else:
			response = self.retreivePlainResource(self.job)

		if 'title' in response and 'contents' in response:
			self.job.title    = response['title']
			self.job.content  = response['contents']
			self.job.mimetype = 'text/html'
			self.job.is_text  = True
			self.job.state    = 'complete'


		return response
		# self.upsertResponseLinks(job, response)
