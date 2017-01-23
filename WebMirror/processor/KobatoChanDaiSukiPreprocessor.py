
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
import markdown


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
	elif in_coords.numberOfContours == 0:
		return tuple()
	else:
		print("Wat?")
		return tuple()


def defont():
	f = TTFont("170122074156ARIAL-KCDS.woff")

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

	for codepoints, symbols in items:
		convs = " <- ".join([chr(cp) for cp in codepoints])
		print("Conversion tree: '{}' (Raw: {})".format(str(convs).rjust(10), (codepoints, symbols)))




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

	def preprocessBody(self, soup):
		ss = soup.find_all('link', rel='stylesheet')
		print(ss)

		return soup
