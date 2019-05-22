
import bs4
import copy
import re
import time
import urllib.parse
import os.path
import os


import tqdm

from fontTools.ttLib import TTFont
import fontTools.ttLib.tables._g_l_y_f as g_l_y_f

import common.util.urlFuncs as urlFuncs
from . import HtmlProcessor
import WebMirror.API
import common.database as db
import tinycss2
import bs4

import itertools
import code
import io

from .fonts import FontTables

PRELOADED_FONTS = {}

def get_codepoint_name_map(f):

	# Now we have to extract the map of
	# unicode codepoints to the internal font symbol names.
	unicode_plat = None
	for table in f['cmap'].tables:
		# Platform ID 0 is "Unicode", whatever that means.
		# there's also a 'platEncID' parameter, but I haven't been able
		# to figure out what it refers to at all.
		if table.platformID == 0:
			unicode_plat = table

	if not unicode_plat:
		return None

	# Since the map is codepoint->name, we flip it.
	inverse_map = {value:key for key, value in unicode_plat.cmap.items()}

	return inverse_map

def load_fonts():
	fonts = []

	fontdir = os.path.join(os.path.dirname(__file__), "fonts")
	for font_name in tqdm.tqdm(os.listdir(fontdir)):
		if font_name.endswith(".woff"):
			with open(os.path.join(fontdir, font_name), "rb") as fp:
				font = TTFont(fp)
				fonts.append((font, font_name))

	return fonts


def check_init_font_cache():

	if PRELOADED_FONTS:
		return PRELOADED_FONTS

	fonts = load_fonts()


	for font, font_name in tqdm.tqdm(fonts):
		inverse_map = get_codepoint_name_map(font)

		if not inverse_map:
			print("Error - No unicode table in %s" % font_name)
			continue

		gs = font.getGlyphSet()

		keys = list(gs.keys())
		keys.sort()

		for key in keys:
			# For each glyph, pull out a flattened, sorted representation of the glyph's component(s)
			gly = gs[key]
			raw_glyph = gly._glyph
			coords = flatten_coords(raw_glyph)

			# Using that base representation of the glyph, stick it into
			# a list
			PRELOADED_FONTS.setdefault(tuple(coords), []).append((inverse_map.get(key, None), gly))

	print("Pre-initialized with %s glyphs from %s files" % (len(PRELOADED_FONTS), len(fonts)))
	return PRELOADED_FONTS


def flatten_coords(in_coords):
	if isinstance(in_coords, g_l_y_f.GlyphComponent):
		return in_coords.getComponentInfo()
	elif hasattr(in_coords, "coordinates"):
		ret = list(in_coords.coordinates)
		ret.sort()
		return tuple(ret)
	elif hasattr(in_coords, "components"):
		ret = [flatten_coords(tmp) for tmp in in_coords.components]
		ret.sort()
		return tuple(ret)
	elif isinstance(in_coords, list):
		ret = [flatten_coords(subitem for subitem in in_coords)]
		ret.sort()
		return tuple(ret)
	elif hasattr(in_coords, "numberOfContours") and in_coords.numberOfContours == 0:
		return tuple()
	else:
		# print("Wat: ", type(in_coords), in_coords)
		return tuple()


def defont(font, url):

	# print("Processing font file from url %s" % url)

	f = TTFont(font)

	gs = f.getGlyphSet()
	keys = list(gs.keys())
	keys.sort()

	coorset = {k : [(ord(v['char']), None)] for k, v in FontTables.PREDEFINED_FONT_MAPS.items()}


	inverse_map = get_codepoint_name_map(f)


	# print(inverse_map)

	for key in keys:
		# For each glyph, pull out a flattened, sorted representation of the glyph's component(s)
		gly = gs[key]
		raw_glyph = gly._glyph
		coords = flatten_coords(raw_glyph)

		# print(key, inverse_map.get(key, None), coords)

		# Using that base representation of the glyph, stick it into
		# a list
		coorset.setdefault(tuple(coords), []).append((inverse_map.get(key, None), gly))



	# Filter the codepoint lists.
	# Note that I'm not sure how to handle duplicate items that
	# have no entry in the mapping table. I'm just ignoring items for which
	# that is true at the moment.
	# It seems to work.
	items = []
	for key, value in coorset.items():
		# print("Key, value:", key, value)
		if len(value) > 1:


			cps  = [item[0] for item in value if item[0]]
			syms = [item[1] for item in value]

			# Ignore invalid mappings.
			if len(cps) <= 1:
				continue

			# We have to sort the codepoints, because we want to convert down to the simpler entries.
			# A-Za-z is within the ascii table, so we are converting from high codepoints (> 1000) to
			# the ascii entries. Going the other way is how you /add/ the replacement cipher.
			cps.sort()

			# print("Key:", key)
			# print("Dupe:", cps, syms, value)

			# Identity mappings are useless
			if all([cps[0] == c for c in cps]):
				continue

			items.append((cps, syms))

	items.sort()

	convmap = {}
	for codepoints, symbols in items:
		convs = " <- ".join([chr(cp) for cp in codepoints])
		# print("Conversion: %s" % convs)
		for cp in codepoints[1:]:
			if chr(cp) != chr(codepoints[0]):
				convmap[chr(cp)] = chr(codepoints[0])



	return convmap

def isplit(iterable, conditional):
	return [list(g) for k,g in itertools.groupby(iterable, conditional) if not k]


def apply_correction_map(soup, tag, cor_map):
	for item in list(tag.descendants):
		if isinstance(item, bs4.NavigableString):
			origstr = str(item)
			itemstr = origstr
			for fontset in cor_map:
				for badc, goodc in fontset.items():
					if badc in itemstr:
						itemstr = itemstr.replace(badc, goodc)
			if origstr != itemstr:
				news = soup.new_string(itemstr)
				item.replace_with(news)



class BaseFontRemapProcessor(HtmlProcessor.HtmlPageProcessor):


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


	def _getFontUrl(self, soup):
		ss = soup.find_all('link', rel='stylesheet')
		for item in ss:
			if hasattr(item, "href"):
				if "/useanyfont/" in item['href'] and 'css' in item['href']:
					if "http://" in item['href'] or "https://" in item['href']:
						return item['href']
					else:
						return urllib.parse.urljoin(self.pageUrl, item['href'])

		return None

	def _extractCss(self, css):
		# Parsing CSS is always a clusterfuck

		ss, coding = tinycss2.parse_stylesheet_bytes(css)
		ssf = [tmp.content for tmp in ss if tmp.type == "at-rule"]

		ssf = [isplit(tmp, lambda x:x.type=="literal" and x.value.strip() == ";") for tmp in ssf]
		fonts = {}
		for fontdef in ssf:
			name = None
			urls = []
			for subsection in [tmp for tmp in fontdef if len(tmp) and tmp[0].type == "ident"]:
				if subsection[0].value == "font-family":
					name = subsection[2].value
				if subsection[0].value == 'src':
					for tmp in subsection:
						# We want the woffs
						if tmp.type == "url" and tmp.value.lower().endswith("woff"):
							value = tmp.value
							if "http://" in value or "https://" in value:
								urls.append(value)
							else:
								urls.append(urllib.parse.urljoin(self.pageUrl, value))

							self.log.info("Found font-family tag: '%s' -> '%s'", name, value)

			if name and urls:
				fonts.setdefault(name, [])
				fonts[name].append(list(set(urls))[0])
		self.log.info("Found %s font-family tags!", len(fonts))
		return fonts

	def _getFontLuts(self, fonturls):

		ret = {}

		for key, fonturl_list in fonturls.items():
			ret[key] = []
			for fonturl in fonturl_list:
				self.log.info("Building font remap LUT for font at %s", fonturl)
				with db.session_context() as sess:
					with WebMirror.API.getPageRow(fonturl, ignore_cache=False, session=sess) as page:
						try:
							page.fetch(ignore_cache=False)
							_, _, content = page.getResource()
						except AssertionError:
							page.fetch(ignore_cache=True)
							_, _, content = page.getResource()

						cmap = defont(io.BytesIO(content), fonturl)
						if cmap:
							# self.log.info("Font remap contains %s remapped code-points", len(cmap))
							ret[key].append(cmap)


		# I'm unclear why just this one char is being missed.
		if 'arial-kcds' in ret:
			ret['arial-kcds']["걣"] = "A"

		self.log.info("Found %s remapped fonts", len(ret))

		return ret


	def getMapTable(self, soup):

		cssUrl = self._getFontUrl(soup)
		if not cssUrl:
			return []
		with db.session_context() as sess:
			with WebMirror.API.getPageRow(cssUrl, ignore_cache=False, session=sess) as page:
				assert page
				mimetype, fname, content = page.getResource()

		assert mimetype.lower() == "text/css"

		fonturls = self._extractCss(content)
		fontluts = self._getFontLuts(fonturls)
		return fontluts

	def preprocessBody(self, soup):
		mt = self.getMapTable(soup)

		for key, maptable in mt.items():
			to_fix = soup.find_all(True, style=re.compile(key, re.IGNORECASE))
			for item in to_fix:
				apply_correction_map(soup, item, maptable)
			to_fix = soup.find_all(True, class_=re.compile(key, re.IGNORECASE))
			for item in to_fix:
				apply_correction_map(soup, item, maptable)



		apply_correction_map(soup, soup.body, maptable)

		return soup


class KobatoChanDaiSukiPageProcessor(BaseFontRemapProcessor):

	wanted_mimetypes = ['text/html']
	want_priority    = 80

	loggerPath = "Main.Text.KobatoChanDaiSuki"

	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https?://(?:www\.)?kobatochan\.com", url):
			print("KobatoChanDaiSukiProcessor Wants url: '%s'" % url)
			return True
		return False

class NepustationPageProcessor(BaseFontRemapProcessor):

	wanted_mimetypes = ['text/html']
	want_priority    = 80

	loggerPath = "Main.Text.Nepustation"

	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https?://(?:www\.)?nepustation\.com", url):
			print("Nepustation Wants url: '%s'" % url)
			return True
		return False

	def preprocessBody(self, soup):

		# The nepustation guy is a first-class douchecanoe
		for item in soup.find_all("span", style=re.compile("color: transparent", re.IGNORECASE)):
			item.decompose()

		soup = super().preprocessBody(soup)

		return soup

class EccentricTranslationsFontRemapProcessor(BaseFontRemapProcessor):

	wanted_mimetypes = ['text/html']
	want_priority    = 80

	loggerPath = "Main.Text.EccentricTranslations"

	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https?://(?:www\.)?eccentrictranslations\.com", url):
			print("EccentricTranslationsProcessor Wants url: '%s'" % url)
			return True
		return False

	def _getCssUrls(self, soup):
		ret = []
		css = soup.find_all('link', rel='stylesheet')
		for tag in css:
			if tag.get("href", None):
				url = tag.get("href")
				ret.append(urllib.parse.urljoin(self.pageUrl, url))

		self.log.info("Found %s CSS Links", len(ret))

		return ret


	def getMapTable(self, soup):

		cssUrls = self._getCssUrls(soup)
		if not cssUrls:
			return []

		for cssUrl in cssUrls:
			with db.session_context() as sess:
				with WebMirror.API.getPageRow(cssUrl, ignore_cache=False, session=sess) as page:
					assert page
					mimetype, fname, content = page.getResource()

			assert mimetype.lower() == "text/css"

			fonturls = self._extractCss(content)

			fontluts = self._getFontLuts(fonturls)
		return fontluts



	def preprocessBody(self, soup):
		if soup.find('div', id='copyfight_content'):
			self.log.info("Found copyfight garbage div. Fixing.")
			soup = super().preprocessBody(soup)

		return soup

	def test(self):
		import pprint

		fontluts = self._getFontLuts({'copyfight' : [
				# 'http://eccentrictranslations.com/wp-content/plugins/copyfight/cache/opensans/OpenSans-Regular.woff',
				'http://eccentrictranslations.com/wp-content/plugins/copyfight/cache/4/42a38ad215ab716a45257eec057d15748f829ec44d6e17d0c8b41aa1fb42a4f4.woff',
			]})


		# print("Font luts:")
		# pprint.pprint(fontluts)


def test():

	# fonts = check_init_font_cache()
	# print(fonts)

	wat = EccentricTranslationsFontRemapProcessor(
									pageUrl         = 'wat',
									pgContent       = 'wat',
									mimeType        = 'wat',
									db_sess         = 'wat',
									baseUrls        = 'wat',
									loggerPath      = 'wat',
									badwords        = 'wat',
									decompose       = 'wat',
									decomposeBefore = 'wat',
									fileDomains     = 'wat',
									allImages       = 'wat',
									decompose_svg   = 'wat',
									ignoreBadLinks  = 'wat',
									stripTitle      = 'wat',
									relinkable      = 'wat',
									destyle         = 'wat',
									preserveAttrs   = 'wat',
									type            = 'wat',
									message_q       = 'wat',
									job             = 'wat',
									wg_proxy        = 'wat',
		)

	print(wat)

	wat.test()



if __name__ == '__main__':
	import logSetup
	logSetup.initLogging(1)
	test()

