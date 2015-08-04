
import urllib.parse

import bs4
import copy
import readability.readability
import lxml.etree
import traceback

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


	wanted_mimetypes = ['text/html']
	want_priority    = 50

	loggerPath = "Main.Text.HtmlProc"

	def __init__(self, baseUrls, pageUrl, pgContent, loggerPath, relinkable, **kwargs):
		self.loggerPath = loggerPath+".HtmlExtract"

		self._tld           = set()
		self._fileDomains   = set()

		self.content = pgContent
		self.pageUrl = pageUrl

		# kwargs.setdefault("badwords",           [])
		# kwargs.setdefault("decompose",          [])
		# kwargs.setdefault("decomposeBefore",    [])
		# kwargs.setdefault("fileDomains",        [])
		# kwargs.setdefault("allImages",          True)
		# kwargs.setdefault("followGLinks",       True)
		# kwargs.setdefault("ignoreBadLinks",     False)
		# kwargs.setdefault("tld",                set())
		# kwargs.setdefault("stripTitle",         '')
		# kwargs.setdefault("ignoreMissingTitle", False)
		# kwargs.setdefault("destyle",            [])

		self._badwords        = set()
		# `_decompose` and `_decomposeBefore` are the actual arrays of items to decompose, that are loaded with the contents of
		# `decompose` and `decomposeBefore` on plugin initialization
		self._decompose       = copy.copy(GLOBAL_DECOMPOSE_AFTER)
		self._decomposeBefore = copy.copy(GLOBAL_DECOMPOSE_BEFORE)
		self.stripTitle       = copy.copy(kwargs['stripTitle'])
		self.destyle          = copy.copy(kwargs['destyle'])


		appends = [
			(kwargs["decompose"],       self._decompose),
			(kwargs["decomposeBefore"], self._decomposeBefore),
		]
		adds = [
			(kwargs["badwords"],        self._badwords),

		]

		# Move the plugin-defined decompose calls into the control lists
		for src, dst in appends:
			for item in src:
				dst.append(item)


		for src, dst in adds:
			for item in src:
				dst.add(item)






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

		# # Filter by domain
		# if not self.allImages and not any([base in url for base in self._fileDomains]):
		# 	return

		# # and by blocked words
		# hadbad = False
		# for badword in self._badwords:
		# 	if badword.lower() in url.lower():
		# 		hadbad = True
		# if hadbad:
		# 	return


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


	def destyleItems(self, soup, destyle):
		'''
		using the set of search 2-tuples in `destyle`,
		walk the parse tree and decompose the attributes of any matching
		element.
		'''
		for tagtype, attrs in destyle:
			for found in soup.find_all(tagtype, attrs=attrs):
				for key in list(found.attrs):
					del found.attrs[key]

		return soup

	def decomposeItems(self, soup, toDecompose):
		# print("Decomposing", toDecompose)
		# Decompose all the parts we don't want
		for key in toDecompose:
			try:
				if not soup:
					print("Soup is false? Wat?")
				have = soup.find_all(True, attrs=key)

				for instance in have:
					# print("Need to decompose for ", key)
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

		# And all remote scripts
		for item in soup.find_all("script"):
			item.decompose()

		# Link tags
		for item in soup.find_all("link"):
			item.decompose()

		# Meta tags
		for item in soup.find_all("meta"):
			item.decompose()

		# Comments
		for item in soup.findAll(text=lambda text:isinstance(text, bs4.Comment)):
			item.extract()

		return soup

	def cleanHtmlPage(self, soup, url=None):

		soup = self.relink(soup)

		title = self.extractTitle(soup, url)


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



	def removeClasses(self, soup):
		cnt = 0

		validattrs = [
			'href',
			'src',
			'style',

		]

		for item in [item for item in soup.find_all(True) if item]:
			for attr in list(item.attrs.keys()):
				if attr not in validattrs:
					del item[attr]

		return soup

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
		soup = self.destyleItems(soup, self.destyle)

		# Allow child-class hooking
		soup = self.postprocessBody(soup)

		soup = self.removeClasses(soup)

		# Process page with readability, extract title.
		pgTitle, pgBody = self.cleanHtmlPage(soup, url=self.pageUrl)

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

