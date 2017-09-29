


import runStatus
runStatus.preloadDicts = False

# import Levenshtein as lv

import urllib.parse

import bs4
import copy
import hashlib
import os.path

import traceback
import common.util.WebRequest

from WebMirror.processor.ProcessorBase import PageProcessor
# import TextScrape.SiteArchiver


import common.util.urlFuncs as urlFuncs
import WebMirror.processor.ProcessorUtils.gDocParse as gdp

# import TextScrape.RelinkLookup
# import TextScrape.RELINKABLE as RELINKABLE



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




class GdocPageProcessor(PageProcessor):


	wanted_mimetypes = ['text/html']
	want_priority    = 90

	@staticmethod
	def wantsUrl(url):
		return urlFuncs.isGdocUrl(url)[0]

	loggerPath = "Main.Text.GdocPageProcessor"

	def __init__(self, pageUrl, pgContent, loggerPath, relinkable, scannedDomains=None, tlds=None, **kwargs):
		self.loggerPath = loggerPath+".GDocExtract"
		self.pageUrl    = pageUrl


		self._relinkDomains = set()
		for url in relinkable:
			self._relinkDomains.add(url)


		self._tld            = set()
		self._scannedDomains = set()

		# Tell the path filtering mechanism that we can fetch google doc files
		# Not switchable, since not fetching google docs content from a google docs page
		# wouldn't work too well.
		self._scannedDomains.add('https://docs.google.com/document/')
		self._scannedDomains.add('https://docs.google.com/spreadsheets/')
		self._scannedDomains.add('https://drive.google.com/folderview')
		self._scannedDomains.add('https://drive.google.com/open')

		if not scannedDomains:
			scannedDomains = []
		if not tlds:
			tlds = []

		# Build the filtering structures for checking outgoing links.
		for tld in tlds:
			self._tld.add(tld)


		if isinstance(scannedDomains, (set, list)):
			for url in scannedDomains:
				self.installBaseUrl(url)
		else:
			self.installBaseUrl(scannedDomains)

		# File mapping LUT
		self.fMap = {}

	def installBaseUrl(self, url):
		# print("Inserting ", url)
		netloc = urllib.parse.urlsplit(url.lower()).netloc
		if not netloc:
			raise ValueError("One of the scanned domains collapsed down to an empty string: '%s'!" % url)

		# Generate the possible wordpress netloc values.
		if 'wordpress.com' in netloc:
			subdomain, mainDomain, tld = netloc.rsplit(".")[-3:]

			self._scannedDomains.add("www.{sub}.{main}.{tld}".format(sub=subdomain, main=mainDomain, tld=tld))
			self._scannedDomains.add("{sub}.{main}.{tld}".format(sub=subdomain, main=mainDomain, tld=tld))
			self._scannedDomains.add("www.{sub}.files.{main}.{tld}".format(sub=subdomain, main=mainDomain, tld=tld))
			self._scannedDomains.add("{sub}.files.{main}.{tld}".format(sub=subdomain, main=mainDomain, tld=tld))

		# Blogspot is annoying and sometimes a single site is spread over several tlds. *.com, *.sg, etc...
		if 'blogspot.' in netloc:
			subdomain, mainDomain, tld = netloc.rsplit(".")[-3:]
			self._tld.add(tld)
			for tld in self._tld:
				self._scannedDomains.add("www.{sub}.{main}.{tld}".format(sub=subdomain, main=mainDomain, tld=tld))
				self._scannedDomains.add("{sub}.{main}.{tld}".format(sub=subdomain, main=mainDomain, tld=tld))

		if 'sites.google.com/site/' in url:
			self._scannedDomains.add(url)

		elif 'google.' in netloc:
			self.log.info("Skipping URL: '%s'", url)

		else:

			base, tld = netloc.rsplit(".", 1)
			self._tld.add(tld)
			for tld in self._tld:
				self._scannedDomains.add("{main}.{tld}".format(main=base, tld=tld))
				# print(self._scannedDomains)



	########################################################################################################################
	#
	#	 ######    #######   #######   ######   ##       ########    ########   #######   ######   ######
	#	##    ##  ##     ## ##     ## ##    ##  ##       ##          ##     ## ##     ## ##    ## ##    ##
	#	##        ##     ## ##     ## ##        ##       ##          ##     ## ##     ## ##       ##
	#	##   #### ##     ## ##     ## ##   #### ##       ######      ##     ## ##     ## ##        ######
	#	##    ##  ##     ## ##     ## ##    ##  ##       ##          ##     ## ##     ## ##             ##
	#	##    ##  ##     ## ##     ## ##    ##  ##       ##          ##     ## ##     ## ##    ## ##    ##
	#	 ######    #######   #######   ######   ######## ########    ########   #######   ######   ######
	#
	########################################################################################################################


	def processGdocResources(self, resources):

		# Expected format of tuples in ret:
		# fName, mimeType, content, fHash
		ret = []


		for fName, mimeType, content in resources:
			m = hashlib.md5()
			m.update(content)
			fHash = m.hexdigest()


			pseudoUrl = "gdoc-"+fHash

			self.fMap[fName] = fHash

			fName = os.path.split(fName)[-1]

			self.log.info("Resource = '%s', '%s', '%s'", fName, mimeType, pseudoUrl)
			if mimeType in ["image/gif", "image/jpeg", "image/pjpeg", "image/png", "image/svg+xml", "image/vnd.djvu"]:
				self.log.info("Processing resource '%s' as an image file. (mimetype: %s)", fName, mimeType)
				ret.append((fName, mimeType, content, pseudoUrl))
			elif mimeType in ["application/octet-stream"]:
				self.log.info("Processing '%s' as an binary file.", fName)
				ret.append((fName, mimeType, content, pseudoUrl))
			else:
				self.log.warn("Unknown MIME Type? '%s', FileName: '%s'", mimeType, fName)

		if len(resources) == 0:
			self.log.info("File had no resource content!")

		return ret



	def cleanGdocPage(self, soup, url):
		# doc = readability.readability.Document(str(soup))
		title = self.extractTitle(soup, url)

		for span in soup.find_all("span"):
			span.unwrap()

		for style in soup.find_all('style'):
			style.decompose()

		for tag in soup.find_all(attrs = {'class' : True}):
			del tag['class']

		return title, soup



	# Hook so plugins can modify the internal URLs as part of the relinking process
	def preprocessGdocReaderUrl(self, inUrl):
		if inUrl.lower().endswith("/preview"):
			inUrl = inUrl[:-len("/preview")]

		return inUrl


	def convertToGdocReaderImage(self, srcUrl):

		itemHash = None
		for rscEnd in self.fMap:
			if srcUrl.endswith(rscEnd):
				itemHash = self.fMap[rscEnd]

		# if srcUrl in self.fMap:
		# 	url = self.fMap[srcUrl]
		# elif any([fUrl in url for fUrl in self.fMap]):
		# 	print('wat')
		# 	raise ValueError("Unknown image URL! = '%s'" % url)
		if not itemHash:
			raise ValueError("Unknown image URL! = '%s' (hash '%s')" % (srcUrl, itemHash))

		url = '/books/render?mdsum=%s' % urllib.parse.quote(itemHash)

		return url



	def processGdocPage(self, url, content):
		dummy_fName, content = content
		soup = common.util.WebRequest.as_soup(content)
		urlFuncs.canonizeUrls(soup, url)

		pgTitle, soup = self.cleanGdocPage(soup, url)

		plainLinks = self.extractLinks(soup, url)
		self.log.info("Page title = '%s'", pgTitle)
		soup = self.relink(soup, imRelink=self.convertToGdocReaderImage)

		url = self.preprocessGdocReaderUrl(url)
		url = urlFuncs.trimGDocUrl(url)
		# Since the content we're extracting will be embedded into another page, we want to
		# strip out the <body> and <html> tags. `unwrap()`  replaces the soup with the contents of the
		# tag it's called on. We end up with just the contents of the <body> tag.
		soup.body.unwrap()
		pgBody = soup.prettify()

		# No image links, since they're served as resource files in a google doc
		imageLinks = []
		return plainLinks, imageLinks, pgTitle, pgBody
		# self.updateDbEntry(url=url, title=pgTitle, contents=pgBody, mimetype='text/html', dlstate=2)



	def retreiveGoogleDoc(self, url):


		self.log.info("Should fetch google doc at '%s'", url)
		doc = gdp.GDocExtractor(url)



		attempts = 0


		mainPage = None
		while 1:
			attempts += 1
			try:
				mainPage, resources = doc.extract()
			except TypeError:
				self.log.critical('Extracting item failed!')
				for line in traceback.format_exc().strip().split("\n"):
					self.log.critical(line.strip())


					raise urlFuncs.CannotAccessGDocException("Cannot access google doc! Is it protected?")

			if mainPage:
				break
			if attempts > 3:
				raise TextScrape.SiteArchiver.DownloadException

		resources = self.processGdocResources(resources)

		return self.processGdocPage(url, mainPage) + (resources, )




	# Process a Google-Doc resource page.
	# This call does a set of operations to permute and clean a google doc page.
	def extractContent(self):

		plainLinks, imageLinks, pgTitle, pgBody, resources = self.retreiveGoogleDoc(self.pageUrl)

		ret = {}
		ret['plainLinks'] = plainLinks
		ret['rsrcLinks']  = imageLinks
		ret['title']      = pgTitle
		ret['contents']   = pgBody

		ret['resources'] = resources

		return ret


def test():
	print("Test mode!")
	import WebRequest
	import logSetup
	logSetup.initLogging()

	wg = WebRequest.WebGetRobust()
	# content = wg.getpage('http://www.arstechnica.com')
	scraper = GdocPageProcessor('https://docs.google.com/document/d/1atXMtCutHRpcHwSRS5UyMAC58_gQjMPR2dDVn1LCD3E', 'Main.Test', 'testinating')
	print(scraper)
	extr, rsc = scraper.extractContent()
	print('Plain Links:')
	for link in extr['plainLinks']:
		print(link)
	print()
	print()
	print('Resource files:')
	# for link in extr['rsrcLinks']:
	# 	print(link)

	for fName, mimeType, content, pseudoUrl in rsc:
		print(fName, mimeType, pseudoUrl)
	# print(extr['contents'])



if __name__ == "__main__":
	test()

