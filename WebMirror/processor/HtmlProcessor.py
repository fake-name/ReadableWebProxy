
import bs4
import copy
import re
import time
import webcolors
import urllib.parse
import markdown
import tinycss2
import WebRequest
import common.global_constants

import common.util.urlFuncs as urlFuncs
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

	def __init__(self, baseUrls, pageUrl, pgContent, loggerPath, relinkable, extra_msg=None, extra_logger=None, **kwargs):

		self.loggerPath = "Main.Text.HtmlProc%s" % (extra_logger if extra_logger else "")

		msg = ""
		if extra_msg:
			msg = " (%s)" % extra_msg
		self.log.info("HtmlProc processing HTML content%s.", msg)

		self._tld           = set()
		self._fileDomains   = set()

		assert bool(pgContent) == True

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


		self._decompose       = copy.copy(common.global_constants.GLOBAL_DECOMPOSE_AFTER)
		self._decomposeBefore = copy.copy(common.global_constants.GLOBAL_DECOMPOSE_BEFORE)
		self.stripTitle       = copy.copy(kwargs['stripTitle'])
		self.destyle          = copy.copy(kwargs['destyle'])
		self.preserveAttrs    = copy.copy(kwargs['preserveAttrs'])
		self.decompose_svg    = bool(kwargs['decompose_svg'])


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


	def purgeEmptyTags(self, soup):
		for _ in range(5):
			# SVGs are annoying, and nest shit.
			for path_tag in soup.find_all(["polygon", "g", "path", "svg", "div", "span"]):
				if path_tag.contents == [] and path_tag.get_text(strip=True) == "":
					path_tag.decompose()

				if path_tag.name == 'svg':
					for svg_title in path_tag.find_all("title"):
						svg_title.unwrap()

		return soup

	def destyleItems(self, soup):
		'''
		using the set of search 2-tuples in `destyle`,
		walk the parse tree and decompose the attributes of any matching
		element.
		'''

		# Use a custom function so we only walk the tree once.
		def destyleSearchFunc(tag):
			if tag.name in self.destyle:
				filter_attr = self.destyle[tag.name]

				if not filter_attr:
					return True

				for key, value in filter_attr.items():
					if tag.get(key, "NO_VAL_WAT") == value:
						return True

			return False

		for found in soup.find_all(destyleSearchFunc):
			for key in list(found.attrs):
				del found.attrs[key]

		return soup

	def decomposeItems(self, soup, toDecompose):
		if not soup:
			print("Soup is false? Wat?")

		# print("Decomposing", toDecompose)
		# Decompose all the parts we don't want

		# Use a custom function so we only walk the tree once.
		def searchFunc(tag):
			for candidate in toDecompose:
				for key, value in candidate.items():
					haskey = tag.get(key)
					if haskey:
						vallist = tag.get(key)
						if isinstance(vallist, str):
							vallist = [vallist, ]

						hasval = any([sattr.lower() == value.lower() for sattr in vallist if sattr])
						if hasval:
							return True
			return False


		have = soup.find_all(searchFunc)

		for instance in have:
			# print("Need to decompose for ", key)
			# So.... yeah. At least one blogspot site has EVERY class used in the
			# <body> tag, for no coherent reason. Therefore, *never* decompose the <body>
			# tag, even if it has a bad class in it.
			if instance.name == 'body':
				continue

			instance.decompose()

		return soup

	def decomposeAdditional(self, soup):

		# Clean out any local stylesheets
		for instance in soup.find_all('style', attrs={"type" : "text/css"}):
			instance.decompose()

		decompose = [
			# Clear out all the iframes
			'iframe',
			# Even if not explicitly tagged as css
			'style',
			# And all remote scripts
			"script",
			# Link tags
			"link",
			# Meta tags
			"meta",

			# Stylesheets (needs further checking)
			"style",
		]

		if self.decompose_svg:
			decompose.append("svg")

		for instance in soup.find_all(decompose):

			# If it's a style tag, make sure the type is text/css before removing
			if instance.name == 'style':
				if instance.get("type", None) == "text/css":
					instance.decompose()
			else:
				instance.decompose()

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


		# Match the CSS ASCII color classes
		hexr = re.compile('((?:[a-fA-F0-9]{6})|(?:[a-fA-F0-9]{3}))')

		def clamp_hash_token(intok, high):
			old = hexr.findall(intok.value)
			for match in old:
				color = webcolors.hex_to_rgb("#"+match)
				mean = sum(color)/len(color)

				if high:
					if mean > 150:
						color = tuple((max(255-cval, 0) for cval in color))
						new = webcolors.rgb_to_hex(color)
						intok.value = intok.value.replace(match, new)
				else:
					if mean < 100:
						color = tuple((min(cval, 100) for cval in color))
						new = webcolors.rgb_to_hex(color).replace("#", "")
						intok.value = intok.value.replace(match, new)
			return intok

		def clamp_css_color(toks, high=True):
			toks = [tok for tok in toks if tok.type != 'whitespace']

			for tok in toks:
				if tok.type == 'hash':
					clamp_hash_token(tok, high)
				if tok.type == 'string':
					tok.value = ""

			return toks

		hascss = soup.find_all(True, attrs={"style" : True})


		initial_keys = [
				'font',
				'font-family'
		]

		empty_keys = [
				'font-size',
				'width',
				'height',
				'display',
				'max-width',
				'max-height',
				'background-image',
				'margin-bottom',
				'line-height',
				'vertical-align',
				'white-space',
				'font-size',
				'box-sizing',
				'cursor',
				'display',
				'height',
				'left',
				'margin-bottom',
				'margin-right',
				'margin',
				'object-fit',
				'overflow',
				'position',
				'right',
				'text-align',
				'top',
				'visibility',
				'width',
				'z-index',

		]

		foreground_color_keys = [
			'color',
		]
		background_color_keys = [
			'background',
			'background-color',
		]

		for item in hascss:
			if 'tony-yon-ka.blogspot.com' in self.pageUrl:
					item['style'] = ""

			elif item['style']:

				try:
					parsed_style = tinycss2.parse_declaration_list(item['style'])

					for style_chunk in parsed_style:
						if style_chunk.type == 'declaration':

							if any([dec_str == style_chunk.name for dec_str in initial_keys]):
								style_chunk.value = [tinycss2.ast.IdentToken(1, 1, "Sans-Serif")]
							if any([dec_str == style_chunk.name for dec_str in empty_keys]):
								style_chunk.value = []

							if any([dec_str == style_chunk.name for dec_str in foreground_color_keys]):
								style_chunk.value = clamp_css_color(style_chunk.value)
							if any([dec_str == style_chunk.name for dec_str in background_color_keys]):
								style_chunk.value = clamp_css_color(style_chunk.value, high=False)

							# Force overflow to be visible
							if style_chunk.name == "overflow":
								style_chunk.value = [tinycss2.ast.IdentToken(1, 1, "visible")]

					parsed_style = [chunk for chunk in parsed_style if chunk.value]

					item['style'] = tinycss2.serialize(parsed_style)

				except AttributeError:
					# If the parser encountered an error, it'll produce 'ParseError' tokens without
					# the 'value' attribute. This produces attribute errors.
					# If the style is fucked, just clobber it.
					item['style'] = ""

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

		if soup.head:
			soup.head.decompose()

		# Since the content we're extracting will be embedded into another page, we want to
		# strip out the <body> and <html> tags. `unwrap()`  replaces the soup with the contents of the
		# tag it's called on. We end up with just the contents of the <body> tag.
		while soup.body:
			# print("Unwrapping body tag")
			soup.body.unwrap()

		while soup.html:
			# print("Unwrapping html tag")
			soup.html.unwrap()

		for item in soup.children:
			if isinstance(item, bs4.Doctype):
				# print("decomposing doctype")
				item.extract()

		contents = soup.prettify()

		for item in common.global_constants.GLOBAL_INLINE_BULLSHIT:
			contents = contents.replace(item, "")

		return title, contents



	def removeClasses(self, soup):
		validattrs = [
			'href',
			'src',
			'style',
			'cellspacing',
			'cellpadding',
			'border',
			'colspan',
			'onclick',
			'type',
			'value',
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
					if attr == 'style' and 'float' in value:
						del item[attr]
					elif attr not in tmp_valid:
						del item[attr]

			# Set the class of tables set to have no borders to the no-border css class for later rendering.
			if item.name == "table" and item.has_attr("border") and item['border'] == "0":
				if not item.has_attr("class"):
					item['class'] = ""
				item['class'] += " noborder"


		return soup


	# Miscellaneous spot-fixes for specific sites.
	def prePatch(self, url, soup):
		return soup


	# Miscellaneous spot-fixes for specific sites.
	def spotPatch(self, soup):

		# Replace <pre> tags on wattpad.
		# wp_div = soup.find_all('div', class_="panel-reading")
		# for item in wp_div:
		# Fukkit, just nuke them in general
		for pre in soup.find_all("pre"):
			pre.name = "div"
			contentstr = pre.encode_contents().decode("utf-8")

			# Don't markdown huge documents.
			if len(contentstr) > 1024 * 500:
				continue

			formatted = markdown.markdown(contentstr, extensions=["linkify"])
			formatted = WebRequest.as_soup(formatted)
			if formatted.find("html"):
				formatted.html.unwrap()
				formatted.body.unwrap()
				pre.replace_with(formatted)
			# print(pre)
		return soup




	def preprocessBody(self, soup):
		for link in soup.find_all("a"):
			if link.has_attr("href"):
				if "javascript:if(confirm(" in link['href']:
					qs = urllib.parse.urlsplit(link['href']).query
					link['href'] = "/viewstory.php?{}".format(qs)

		return soup

	# Process a plain HTML page.
	# This call does a set of operations to permute and clean a HTML page.
	#
	# First, it decomposes all tags with attributes dictated in the `_decomposeBefore` class variable
	# it then canonizes all the URLs on the page, extracts all the URLs from the page,
	# then decomposes all the tags in the `decompose` class variable, feeds the content through
	# readability, and finally saves the processed HTML into the database
	def extractContent(self):
		self.log.info("Processing '%s' as HTML (size: %s).", self.pageUrl, len(self.content))
		assert self.content
		# print(type(self.content))

		badxmlprefix = '<?xml version="1.0"?>'
		if self.content.strip().lower().startswith(badxmlprefix):
			self.content = self.content[len(badxmlprefix):]


		soup = WebRequest.as_soup(self.content)
		# try:
		# 	soup = WebRequest.as_soup(self.content)
		# except AttributeError as e:
		# 	with open("badpage %s.html" % time.time(), "w") as fp:
		# 		fp.write(self.content)
		# 		raise e


		soup = self.prePatch(self.pageUrl, soup)

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
		soup = self.spotPatch(soup)
		soup = self.destyleItems(soup)

		# Allow child-class hooking
		soup = self.postprocessBody(soup)

		soup = self.removeClasses(soup)

		soup = self.purgeEmptyTags(soup)

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

