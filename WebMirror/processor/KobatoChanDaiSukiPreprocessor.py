
import bs4
import copy
import re
import time
import webcolors
import urllib.parse
import common.util.webFunctions

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
		print("Wat: ", type(in_coords), in_coords)
		return tuple()


def defont(font):
	f = TTFont(font)

	gs = f.getGlyphSet()
	keys = list(gs.keys())
	keys.sort()

	coorset = {}

	for key in keys:
		# For each glyph, pull out a flattened, sorted representation of the glyph's component(s)
		gly = gs[key]
		raw_glyph = gly._glyph
		coords = flatten_coords(raw_glyph)


		# Using that base representation of the glyph, stick it into
		# a list
		coorset.setdefault(tuple(coords), []).append((key, gly))


	# Now we have to extract the map of
	# unicode codepoints to the internal font symbol names.
	unicode_plat = None
	for table in f['cmap'].tables:
		# Platform ID 0 is "Unicode", whatever that means.
		# there's also a 'platEncID' parameter, but I haven't been able
		# to figure out what it refers to at all.
		if table.platformID == 0:
			unicode_plat = table

	# Since the map is codepoint->name, we flip it.
	inverse_map = {value:key for key, value in unicode_plat.cmap.items()}


	# Filter the codepoint lists.
	# Note that I'm not sure how to handle duplicate items that
	# have no entry in the mapping table. I'm just ignoring items for which
	# that is true at the moment.
	# It seems to work.
	items = []
	for key, value in coorset.items():
		if len(value) > 1:

			syms = [item[0] for item in value]
			cps = [inverse_map[key] for key in syms if key in inverse_map]

			# We have to sort the codepoints, because we want to convert down to the simpler entries.
			# A-Za-z is within the ascii table, so we are converting from high codepoints (> 1000) to
			# the ascii entries. Going the other way is how you /add/ the replacement cipher.
			cps.sort()

			# Filtering.
			if len(cps) < 2:
				continue
			items.append((cps, syms))

	items.sort()

	convmap = {}
	for codepoints, symbols in items:
		convs = " <- ".join([chr(cp) for cp in codepoints])
		for cp in codepoints[1:]:
			convmap[chr(cp)] = chr(codepoints[0])



	return convmap

def isplit(iterable, conditional):
	return [list(g) for k,g in itertools.groupby(iterable, conditional) if not k]


class KobatoChanDaiSukiPageProcessor(HtmlProcessor.HtmlPageProcessor):


	wanted_mimetypes = ['text/html']
	want_priority    = 80

	loggerPath = "Main.Text.KobatoChanDaiSuki"

	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https?://(?:www\.)?kobatochan\.com", url):
			print("KobatoChanDaiSukiProcessor Wants url: '%s'" % url)
			return True
		return False

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.sess = db.checkout_session()

	def __del__(self):
		db.release_session(self.sess)

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


			if name and urls:
				fonts[name] = list(set(urls))[0]
		return fonts
	def _getFontLuts(self, fonturls):
		ret = {}
		for key, fonturl in fonturls.items():

			with WebMirror.API.getPageRow(fonturl, ignore_cache=False, session=self.sess) as page:
				mimetype, fname, content = page.getResource()
				print(key, mimetype, fname, fonturl)
				cmap = defont(io.BytesIO(content))
				ret[key] = cmap

		# I'm unclear why just this one char is being missed.
		if 'arial-kcds' in ret:
			ret['arial-kcds']["걣"] = "A"

		return ret


	def getMapTable(self, soup):

		cssUrl = self._getFontUrl(soup)
		if not cssUrl:
			return []
		with WebMirror.API.getPageRow(cssUrl, ignore_cache=False, session=self.sess) as page:
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
			print(key)

		apply_correction_map(soup, soup.body, maptable)

		return soup

def apply_correction_map(soup, tag, cor_map):
	for item in list(tag.descendants):
		if isinstance(item, bs4.NavigableString):
			origstr = str(item)
			itemstr = origstr
			for badc, goodc in cor_map.items():
				if badc in itemstr:
					itemstr = itemstr.replace(badc, goodc)
			if origstr != itemstr:
				news = soup.new_string(itemstr)
				item.replace_with(news)

	# print(str(tag).encode("utf-8"))
	# print("걣 in str:", '걣' in str(tag))
	# print("걣 in cor_map:", '걣' in cor_map)
	# print("놣 in str:", '놣' in str(tag))
