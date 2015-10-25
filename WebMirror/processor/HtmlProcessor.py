
import bs4
import copy
import re
import webcolors

import WebMirror.util.urlFuncs as urlFuncs
from . import ProcessorBase




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




class HtmlPageProcessor(ProcessorBase.PageProcessor):


	wanted_mimetypes = ['text/html']
	want_priority    = 50

	loggerPath = "Main.Text.HtmlProc"

	def __init__(self, baseUrls, pageUrl, pgContent, loggerPath, relinkable, **kwargs):

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

		# `_decompose` and `_decomposeBefore` are the actual arrays of items to decompose, that are loaded with the contents of
		# `decompose` and `decomposeBefore` on plugin initialization


		self._decompose       = copy.copy(ProcessorBase.GLOBAL_DECOMPOSE_AFTER)
		self._decomposeBefore = copy.copy(ProcessorBase.GLOBAL_DECOMPOSE_BEFORE)
		self.stripTitle       = copy.copy(kwargs['stripTitle'])
		self.destyle          = copy.copy(kwargs['destyle'])
		self.preserveAttrs    = copy.copy(kwargs['preserveAttrs'])


		appends = [
			(kwargs["decompose"],       self._decompose),
			(kwargs["decomposeBefore"], self._decomposeBefore),
		]

		# Move the plugin-defined decompose calls into the control lists
		for src, dst in appends:
			for item in src:
				dst.append(item)





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


	def destyleItems(self, soup):
		'''
		using the set of search 2-tuples in `destyle`,
		walk the parse tree and decompose the attributes of any matching
		element.
		'''
		for tagtype, attrs in self.destyle:
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
		for instance in soup.find_all('style', attrs={"type" : "text/css"}):
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


	def fixCss(self, soup):
		'''
		So, because the color scheme of our interface can vary from the original, we need to fix any cases
		of white text. However, I want to preserve *most* of the color information.
		Therefore, we look at all the inline CSS, and just patch where needed.
		'''

		hascss = soup.find_all(True, attrs={"style" : True})


		# parser = tinycss.make_parser('page3')

		hexr = re.compile('(#(?:[a-fA-F0-9]{6})|#(?:[a-fA-F0-9]{3}))')

		for item in hascss:
			if item['style']:
				ststr = item['style']

				# Prevent inline fonts.
				if 'font' in ststr.lower():
					item['style'] = ''

				# Disable all explicit width settings.
				if 'width' in ststr.lower():
					item['style'] = ''
				if 'max-width' in ststr.lower():
					item['style'] = ''


				old = hexr.findall(ststr)
				for match in old:
					color = webcolors.hex_to_rgb(match)
					mean = sum(color)/len(color)

					if mean > 200:
						above = mean - 200
						color = tuple((max(255-cval, 0) for cval in color))
						new = webcolors.rgb_to_hex(color)
						item['style'] = item['style'].replace(match, new)
						#item['style'] = ''



				# I really /want/ to use a real CSS parser, but I can't find any
				# that properly let me /generate/ CSS. TinyCSS /parses/, but I can't
				# then convert the parse tree back to css (as far as I can tell, anyways)


				# attr, errors = parser.parse_style_attr(item['style'])

				# new = []
				# for decl in attr:
				# 	if decl.name == "color" and decl.value[0].type == "HASH":
				# 		print(decl)
				# 		print(decl.name)
				# 		print(decl.value)

				# 	print(decl.as_css())

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
			tmp_valid = validattrs[:]
			clean = True
			for name, attr in self.preserveAttrs:
				if item.name == name:
					if attr:
						tmp_valid.append(attr)
					else:
						# Preserve all attributes
						clean = False
			if clean and item.attrs:

				for attr, value in list(item.attrs.items()):
					if "float:left" in value or "float:right" in value:
						del item[attr]
					elif attr not in tmp_valid:
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

		# pull out the page content and enqueue it. Filtering is
		# done in the parent.
		plainLinks = self.extractLinks(soup, self.pageUrl)
		imageLinks = self.extractImages(soup, self.pageUrl)

		# Do the later cleanup to prep the content for local rendering.
		soup = self.decomposeItems(soup, self._decompose)

		soup = self.decomposeAdditional(soup)
		soup = self.destyleItems(soup)

		# Allow child-class hooking
		soup = self.postprocessBody(soup)

		soup = self.removeClasses(soup)

		soup = self.fixCss(soup)

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

