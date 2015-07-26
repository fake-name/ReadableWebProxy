
import urllib.parse

import bs4
import copy
import readability.readability
import lxml.etree

import WebMirror.util.urlFuncs as urlFuncs
from . import ProcessorBase

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




GLOBAL_BAD = [
			'gprofiles.js',
			'netvibes.com',
			'accounts.google.com',
			'edit.yahoo.com',
			'add.my.yahoo.com',
			'public-api.wordpress.com',
			'r-login.wordpress.com',
			'twitter.com',
			'facebook.com',
			'public-api.wordpress.com',
			'wretch.cc',
			'ws-na.amazon-adsystem.com',
			'delicious.com',
			'paypal.com',
			'digg.com',
			'topwebfiction.com',
			'/page/page/',
			'addtoany.com',
			'stumbleupon.com',
			'delicious.com',
			'reddit.com',
			'newsgator.com',
			'technorati.com',
			'pixel.wp.com',
			'a.wikia-beacon.com',
			'b.scorecardresearch.com',
			'//mail.google.com',
	]

GLOBAL_DECOMPOSE_BEFORE = [
			{'name'     : 'likes-master'},  # Bullshit sharing widgets
			{'id'       : 'jp-post-flair'},
			{'class'    : 'post-share-buttons'},
			{'class'    : 'commentlist'},  # Scrub out the comments so we don't try to fetch links from them
			{'class'    : 'comments'},
			{'id'       : 'comments'},
		]

GLOBAL_DECOMPOSE_AFTER = []

class HtmlPageProcessor(ProcessorBase.PageProcessor):

	loggerPath = "Main.Text.HtmlProc"

	def __init__(self, baseUrls, pageUrl, pgContent, loggerPath, relinkable, **kwargs):
		self.loggerPath = loggerPath+".HtmlExtract"

		self._tld           = set()
		self._fileDomains   = set()

		self.content = pgContent
		self.pageUrl = pageUrl

		kwargs.setdefault("badwords",           [])
		kwargs.setdefault("decompose",          [])
		kwargs.setdefault("decomposeBefore",    [])
		kwargs.setdefault("fileDomains",        [])
		kwargs.setdefault("allImages",          True)
		kwargs.setdefault("followGLinks",       True)
		kwargs.setdefault("ignoreBadLinks",     False)
		kwargs.setdefault("tld",                set())
		kwargs.setdefault("stripTitle",         '')
		kwargs.setdefault("ignoreMissingTitle", False)

		self.ignoreMissingTitle = kwargs["ignoreMissingTitle"]
		self.allImages          = kwargs["allImages"]
		self.stripTitle         = kwargs["stripTitle"]
		self.ignoreBadLinks     = kwargs['ignoreBadLinks']


		self._badwords       = set(GLOBAL_BAD)
		# `_decompose` and `_decomposeBefore` are the actual arrays of items to decompose, that are loaded with the contents of
		# `decompose` and `decomposeBefore` on plugin initialization
		self._decompose       = copy.copy(GLOBAL_DECOMPOSE_AFTER)
		self._decomposeBefore = copy.copy(GLOBAL_DECOMPOSE_BEFORE)

		self._relinkDomains = set()

		for url in relinkable:
			self._relinkDomains.add(url)

		# A lot of this could probably be a lot more elegant.
		# It's kind of crude and does a lot of unnecessary copying atm.
		# Basically, it works, but it's evolved to it's current state, not
		# been designed to it.
		self.scannedDomains = set()
		if isinstance(baseUrls, (set, list)):
			for url in baseUrls:
				self.scannedDomains.add(url)
				self._fileDomains.add(urllib.parse.urlsplit(url.lower()).netloc)
		else:
			self.scannedDomains.add(baseUrls)
			self._fileDomains.add(urllib.parse.urlsplit(baseUrls.lower()).netloc)

		self._scannedDomains = set()

		if kwargs['followGLinks']:
			# Tell the path filtering mechanism that we can fetch google doc files
			self._scannedDomains.add('https://docs.google.com/document/')
			self._scannedDomains.add('https://docs.google.com/spreadsheets/')
			self._scannedDomains.add('https://drive.google.com/folderview')
			self._scannedDomains.add('https://drive.google.com/open')

			# and relink the google docs as well.
			self._relinkDomains.add('https://docs.google.com/document/')
			self._relinkDomains.add('https://docs.google.com/spreadsheets/')
			self._relinkDomains.add('https://drive.google.com/folderview')
			self._relinkDomains.add('https://drive.google.com/open')



		appends = [
			(kwargs["decompose"],       self._decompose),
			(kwargs["decomposeBefore"], self._decomposeBefore),
		]
		adds = [
			(kwargs["badwords"],        self._badwords),
			(kwargs["fileDomains"],     self._fileDomains),


			# You need to install the TLDs before the baseUrls, because the baseUrls
			# are permuted driven by the TLDs, to some extent.
			(kwargs["tld"],             self._tld),
		]

		# Move the plugin-defined decompose calls into the control lists
		for src, dst in appends:
			for item in src:
				dst.append(item)


		for src, dst in adds:
			for item in src:
				dst.add(item)

		# Lower case all the domains, since they're not case sensitive, and it case mismatches can break matching.
		# We also extract /just/ the netloc, so http/https differences don't cause a problem.
		if isinstance(self.scannedDomains, (set, list)):
			for url in self.scannedDomains:
				self.installBaseUrl(url)
		else:
			self.installBaseUrl(self.scannedDomains)



		tmp = list(self._scannedDomains)
		tmp.sort()
		# for url in tmp:
		# 	self.log.info("Scanned domain:		%s", url)


	def installBaseUrl(self, url):
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

				self._fileDomains.add('bp.blogspot.{tld}'.format(tld=tld))


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
	#	 ######   ######  ########     ###    ########  #### ##    ##  ######      ######## ##     ## ##    ##  ######  ######## ####  #######  ##    ##  ######
	#	##    ## ##    ## ##     ##   ## ##   ##     ##  ##  ###   ## ##    ##     ##       ##     ## ###   ## ##    ##    ##     ##  ##     ## ###   ## ##    ##
	#	##       ##       ##     ##  ##   ##  ##     ##  ##  ####  ## ##           ##       ##     ## ####  ## ##          ##     ##  ##     ## ####  ## ##
	#	 ######  ##       ########  ##     ## ########   ##  ## ## ## ##   ####    ######   ##     ## ## ## ## ##          ##     ##  ##     ## ## ## ##  ######
	#	      ## ##       ##   ##   ######### ##         ##  ##  #### ##    ##     ##       ##     ## ##  #### ##          ##     ##  ##     ## ##  ####       ##
	#	##    ## ##    ## ##    ##  ##     ## ##         ##  ##   ### ##    ##     ##       ##     ## ##   ### ##    ##    ##     ##  ##     ## ##   ### ##    ##
	#	 ######   ######  ##     ## ##     ## ##        #### ##    ##  ######      ##        #######  ##    ##  ######     ##    ####  #######  ##    ##  ######
	#
	########################################################################################################################




	def processImageLink(self, url, baseUrl):

		# Skip tags with `img src=""`.
		# No idea why they're there, but they are
		if not url:
			return

		# Filter by domain
		if not self.allImages and not any([base in url for base in self._fileDomains]):
			return

		# and by blocked words
		hadbad = False
		for badword in self._badwords:
			if badword.lower() in url.lower():
				hadbad = True
		if hadbad:
			return


		url = urlFuncs.urlClean(url)

		return self.processNewUrl(url, baseUrl=baseUrl, istext=False)





	def extractImages(self, soup, baseUrl):
		ret = []
		for imtag in soup.find_all("img"):
						# Skip empty anchor tags
			try:
				url = imtag["src"]
			except KeyError:
				continue

			item = self.processImageLink(url, baseUrl)
			if item:
				ret.append(item)
		return ret


	def decomposeItems(self, soup, toDecompose):
		# Decompose all the parts we don't want
		for key in toDecompose:
			try:
				for instance in soup.find_all(True, attrs=key):

					# So.... yeah. At least one blogspot site has EVERY class used in the
					# <body> tag, for no coherent reason. Therefore, *never* decompose the <body>
					# tag, even if it has a bad class in it.
					if instance.name == 'body':
						continue

					instance.decompose() # This call permutes the tree!
			except AttributeError:
				pass

		return soup

	def decomposeAdditional(self, soup):

		# Clear out all the iframes
		for instance in soup.find_all('iframe'):
			instance.decompose()

		# Clean out any local stylesheets
		for instance in soup.find_all('style'):
			instance.decompose()

		return soup

	def cleanHtmlPage(self, srcSoup, url=None):

		# since readability strips tag attributes, we preparse with BS4,
		# parse with readability, and then do reformatting *again* with BS4
		# Yes, this is ridiculous.

		ctnt = srcSoup.prettify()
		doc = readability.readability.Document(ctnt)
		try:
			doc.parse()
			content = doc.content()
		except lxml.etree.ParserError:
			content = "Page failed to load!"

		soup = bs4.BeautifulSoup(content, "lxml")
		soup = self.relink(soup)
		contents = ''




		title = self.extractTitle(soup, doc, url)


		if isinstance(self.stripTitle, (list, set)):
			for stripTitle in self.stripTitle:
				title = title.replace(stripTitle, "")
		else:
			title = title.replace(self.stripTitle, "")

		title = title.strip()

		# Since the content we're extracting will be embedded into another page, we want to
		# strip out the <body> and <html> tags. `unwrap()`  replaces the soup with the contents of the
		# tag it's called on. We end up with just the contents of the <body> tag.
		soup.body.unwrap()
		contents = soup.prettify()

		return title, contents


	# Process a plain HTML page.
	# This call does a set of operations to permute and clean a HTML page.
	#
	# First, it decomposes all tags with attributes dictated in the `_decomposeBefore` class variable
	# it then canonizes all the URLs on the page, extracts all the URLs from the page,
	# then decomposes all the tags in the `decompose` class variable, feeds the content through
	# readability, and finally saves the processed HTML into the database
	def extractContent(self):
		self.log.info("Processing '%s' as HTML.", self.pageUrl)
		soup = bs4.BeautifulSoup(self.content, "lxml")


		# Allow child-class hooking
		soup = self.preprocessBody(soup)

		# Clear out any particularly obnoxious content before doing any parsing.
		soup = self.decomposeItems(soup, self._decomposeBefore)

		# Make all the page URLs fully qualified, so they're unambiguous
		soup = urlFuncs.canonizeUrls(soup, self.pageUrl)

		# Conditionally pull out the page content and enqueue it.
		if self.checkDomain(self.pageUrl):
			plainLinks = self.extractLinks(soup, self.pageUrl)
			imageLinks = self.extractImages(soup, self.pageUrl)
		else:
			self.log.warn("Not extracting images or links for url '%s'", self.pageUrl)
			plainLinks = []
			imageLinks = []

		# Do the later cleanup to prep the content for local rendering.
		soup = self.decomposeItems(soup, self._decompose)

		soup = self.decomposeAdditional(soup)

		# Allow child-class hooking
		soup = self.postprocessBody(soup)

		# Process page with readability, extract title.
		pgTitle, pgBody = self.cleanHtmlPage(soup, url=self.pageUrl)
		if not self.ignoreMissingTitle:
			if 'has no title!' in pgTitle:
				self.log.warn("Page has no title: '%s' (len %s)", pgTitle, len(pgBody))
			else:
				self.log.info("Page with title '%s' retreived.", pgTitle)

		ret = {}

		# If an item has both a plain-link and an image link, prefer the
		# image link, and delete it from the plain link list
		for link in imageLinks:
			if link in plainLinks:
				plainLinks.remove(link)

		ret['plainLinks'] = plainLinks
		ret['rsrcLinks']  = imageLinks
		ret['title']      = pgTitle
		ret['contents']   = pgBody


		return ret

		# self.updateDbEntry(url=url, title=pgTitle, contents=pgBody, mimetype=mimeType, dlstate=2)



def test():
	print("Test mode!")
	import webFunctions
	import logSetup
	logSetup.initLogging()

	import TextScrape.RelinkLookup

	relinkable = TextScrape.RelinkLookup.getRelinkable()

	wg = webFunctions.WebGetRobust()

	tests = [
		('http://jawztranslations.blogspot.com/2015/03/LMS-V22-C07.html', 'http://jawztranslations.blogspot.com/'),
		('http://skythewood.blogspot.sg/2015/03/G26.html', 'http://skythewood.blogspot.sg/'),
	]

	for testurl, context in tests:
		content = wg.getpage(testurl)
		scraper = HtmlPageProcessor([context], testurl, content, 'Main.Test', tld=['com', 'net', 'sg'], relinkable=relinkable)
		extr = scraper.extractContent()
		# print(scraper)

	print()
	print()
	print()
	print(extr)
	# print(extr['fLinks'])


if __name__ == "__main__":
	test()

