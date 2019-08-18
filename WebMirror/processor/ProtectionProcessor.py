
import re
import markdown
import WebRequest

from . import HtmlProcessor

########################################################################################################################
#
#	Misc fixer classes for various retarded "protection" shit translators do.
#
########################################################################################################################


class XiAiNovelPageProcessor(HtmlProcessor.HtmlPageProcessor):

	wanted_mimetypes = ['text/html']
	want_priority    = 80

	loggerPath = "Main.Text.XiAiNovel"


	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https?://(?:www\.)?xiainovel\.com", url, flags=re.IGNORECASE):
			print("XiAiNovel Wants url: '%s'" % url)
			return True
		# print("hecatescorner doesn't want url: '%s'" % url)
		return False

	def preprocessBody(self, soup):

		# Decompose the annoying inline shit.
		# ex: <span style="color:#ffffff;">the truth is out!</span>
		badspans = soup.find_all("span", style=re.compile(r"color\W?:\W?#ffffff", re.I))
		for bad in badspans:
			bad.decompose()

		return soup



class FoxTellerPageProcessor(HtmlProcessor.HtmlPageProcessor):

	wanted_mimetypes = ['text/html']
	want_priority    = 80

	loggerPath = "Main.Text.FoxTeller"


	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https?://(?:www\.)?foxteller\.com", url, flags=re.IGNORECASE):
			print("FoxTeller Wants url: '%s'" % url)
			return True
		# print("hecatescorner doesn't want url: '%s'" % url)
		return False

	def preprocessBody(self, soup):

		# Decompose the annoying inline shit.
		# ex: <span style="color:#ffffff;">the truth is out!</span>
		badspans = soup.find_all("img", class_="main")
		for bad in badspans:
			bad.decompose()
		badspans = soup.find_all("img", class_="mini")
		for bad in badspans:
			bad.decompose()
		badspans = soup.find_all("span", class_="daeun")
		for bad in badspans:
			bad.decompose()
		badspans = soup.find_all("span", class_="laeon")
		for bad in badspans:
			bad.decompose()
		badspans = soup.find_all("span", class_="mdao")
		for bad in badspans:
			bad.decompose()
		badspans = soup.find_all("span", class_="neqji")
		for bad in badspans:
			bad.decompose()
		badspans = soup.find_all("span", class_="praw")
		for bad in badspans:
			bad.decompose()
		badspans = soup.find_all("span", class_="rawp")
		for bad in badspans:
			bad.decompose()
		badspans = soup.find_all("span", class_="warp")
		for bad in badspans:
			bad.decompose()

		badspans = soup.find_all("span", class_=re.compile(r"^laeon", re.I))
		for bad in badspans:
			bad.decompose()
		badspans = soup.find_all("span", class_=re.compile(r"^neqji", re.I))
		for bad in badspans:
			bad.decompose()

		return soup
