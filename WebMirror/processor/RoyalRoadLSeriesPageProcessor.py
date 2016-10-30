
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




class RoyalRoadLSeriesPageProcessor(HtmlProcessor.HtmlPageProcessor):


	wanted_mimetypes = ['text/html']
	want_priority    = 60

	loggerPath = "Main.Text.RRLProc"


	@staticmethod
	def wantsUrl(url):
		if re.search(r"^http://(?:www\.)?royalroadl\.com/fiction/\d+/?$", url):
			print("RRLSeriesPageProcessor Wants url: '%s'" % url)
			return True
		return False

	def preprocessBody(self, soup):


		for header_div in soup.find_all("div", class_='fiction-stats'):
			header_div.parent.decompose()

		authdivs = soup.find_all("span", class_='caption-subject', text=re.compile("Achievements", flags=re.IGNORECASE))
		#for authd in authdivs:
		#	authd.parent.parent.next_sibling.next_sibling.decompose()
		#	authd.decompose()
		# for sidebar_pane in soup.find_all('div', class_='profile-sidebar'):
		# 	for trophy_chunk in sidebar_pane.find_all('i', class_='fa-trophy'):
		# 		print(trophy_chunk)

		parentdecomps = [
			'fa-book',
			'fa-trophy',
		]
		#for decomp in parentdecomps:
		#	for header_div in soup.find_all("div", class_=decomp):
		#		header_div.parent.parent.decompose()

		decompose_checkboxes = [
			'showMore',
			'showTags',
			'showStats',
		]
		#for bad_input_id in decompose_checkboxes:
		#	for badcb in soup.find_all("input", id=bad_input_id):
		#		badcb.parent.decompose()

		for bad in soup.find_all('i', class_='fa-list-alt'):
			bad.parent.decompose()

		for ad in soup.find_all("h6", text=re.compile("Advertisement", flags=re.IGNORECASE)):
			ad.parent.decompose()

		chapters = soup.find("table", id='chapters')
		if chapters:
			chp_container = chapters.parent
			chapters.extract()

			newlist = soup.new_tag("ul")
			for row in chapters.find_all("tr"):
				tds = row.find_all("td")
				if len(tds) == 2:
					linktd, datetd = tds
					newlink = soup.new_tag("a", href=linktd.a['href'])
					newlink.string = linktd.a.get_text()
					li = soup.new_tag("li")
					li.append(newlink)
					li.append(" ")
					li.append(datetd.get_text().strip())

					newlist.append(li)

			chp_container.append(newlist)

		return soup
