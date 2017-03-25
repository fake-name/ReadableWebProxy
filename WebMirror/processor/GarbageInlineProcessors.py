
import re

from . import HtmlProcessor

########################################################################################################################
#
#	Misc fixer classes for various retarded "protection" shit translators do.
#
########################################################################################################################



class HecatesCornerPageProcessor(HtmlProcessor.HtmlPageProcessor):

	wanted_mimetypes = ['text/html']
	want_priority    = 80

	loggerPath = "Main.Text.HecatesCorner"

	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https?://(?:www\.)?hecatescorner\.wordpress\.com", url):
			print("hecatescorner Wants url: '%s'" % url)
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


class ZenithNovelsPageProcessor(HtmlProcessor.HtmlPageProcessor):

	wanted_mimetypes = ['text/html']
	want_priority    = 80


	loggerPath = "Main.Text.ZenithNovels"

	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https?://(?:www\.)?zenithnovels\.com", url):
			print("zenith novels Wants url: '%s'" % url)
			return True
		# print("zenith novels doesn't want url: '%s'" % url)
		return False

	def preprocessBody(self, soup):

		# Decompose the annoying inline shit.
		# ex: <span style="color:#ffffff;">the truth is out!</span>
		badspans = soup.find_all("span", style=re.compile(r"color\W?:\W?white", re.I))
		for bad in badspans:
			bad.decompose()

		return soup

class LightNovelsWorldPageProcessor(HtmlProcessor.HtmlPageProcessor):

	wanted_mimetypes = ['text/html']
	want_priority    = 80


	loggerPath = "Main.Text.LightNovelsWorld"

	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https?://(?:www\.)?lightnovels\.world", url):
			print("lnw Wants url: '%s'" % url)
			return True
		# print("lnw doesn't want url: '%s'" % url)
		return False

	def preprocessBody(self, soup):

		# Decompose the annoying inline shit.
		# ex: <span style="color:#ffffff;">the truth is out!</span>
		badspans = soup.find_all("span", style=re.compile(r"color\W?:\W?white", re.I))
		for bad in badspans:
			bad.decompose()

		return soup
