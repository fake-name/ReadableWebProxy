
import bs4
import copy
import re
import time
import webcolors
import urllib.parse
import common.util.webFunctions

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




class NuProcessor(HtmlProcessor.HtmlPageProcessor):


	wanted_mimetypes = ['text/html']
	want_priority    = 90

	loggerPath = "Main.Text.NUProc"



	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https?://(?:www\.)?novelupdates\.com", url):
			print("NovelUpdates Wants url: '%s'" % url)
			return True

		return False



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


	# Basically all processing for NU pages is disabled. I want to be able to do postprocessing
	# stuff.

	def destyleItems(self, soup):

		return soup

	def decomposeItems(self, soup, toDecompose):
		return soup

	def decomposeAdditional(self, soup):
		return soup


	def fixCss(self, soup):
		return soup

	def cleanHtmlPage(self, soup, url=None):
		# /don't/ relink.
		# soup = self.relink(soup)
		title = self.extractTitle(soup, url)
		contents = soup.prettify()
		return title, contents



	def removeClasses(self, soup):

		return soup


	def spotPatch(self, soup):

		return soup

	def preprocessBody(self, soup):

		return soup
