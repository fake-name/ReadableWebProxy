
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




class RoyalRoadLChapterPageProcessor(HtmlProcessor.HtmlPageProcessor):


	wanted_mimetypes = ['text/html']
	want_priority    = 60

	loggerPath = "Main.Text.RRLProc"


	@staticmethod
	def wantsUrl(url):
		if "royalroadl.com/fiction/chapter/" in url:
			return True
		if "royalroadl.com/forum/showthread.php?tid=" in url:
			return True
		return False


	def preprocessBody(self, soup):

		# Destroy the oversized header cover image
		for header_div in soup.find_all("div", class_='fic-header'):
			for img in header_div.find_all("img", id=re.compile(r"^cover\-")):
				img.decompose()

		# And peoples avatars
		for comment in soup.find_all("div", class_='comment-container'):
			for imgdiv in comment.find_all("div", class_='media-left'):
				imgdiv.decompose()

		# Relayout the chapter nav buttons.
		for div in soup.find_all('div', class_='margin-bottom-10'):
			button_footer = div.find("a", href=re.compile(r"^/fiction/\d+"))
			newtbl = None
			if button_footer and button_footer.parent:
				parent = button_footer.parent
				elements = parent.find_all(["a", "button"])
				if len(elements) == 3:
					newtbl = soup.new_tag("table", width="100%")
					row = soup.new_tag("tr")
					newtbl.append(row)

					for item in elements:

						td = soup.new_tag("td")
						row.append(td)
						if item.name == "a":
							newlink = soup.new_tag("a", href=item['href'])
							newlink.string = item.get_text()
							td.append(newlink)
						elif item.name == "button":
							newlink = soup.new_tag("span")
							newlink.string = item.get_text()
							td.append(newlink)

				div.clear()
				div.append(newtbl)

		return soup
