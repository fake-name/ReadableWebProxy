
import re
import tinycss2

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


class ShamelessOniisanPageProcessor(HtmlProcessor.HtmlPageProcessor):

	wanted_mimetypes = ['text/html']
	want_priority    = 80


	loggerPath = "Main.Text.ShamelessOniisan"

	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https?://shamelessoniisan\.wordpress\.com", url):
			print("wwsd Wants url: '%s'" % url)
			return True
		# print("lnw doesn't want url: '%s'" % url)
		return False

	def preprocessBody(self, soup):

		# Decompose the annoying inline shit.
		# ex: <span style="color:#ffffff;">the truth is out!</span>
		badspans = soup.find_all("span", style=re.compile(r"color\W?:\W?#ffffff", re.I))
		for bad in badspans:
			bad.decompose()

		return soup

class WatashiWaSugoiDesuPageProcessor(HtmlProcessor.HtmlPageProcessor):

	wanted_mimetypes = ['text/html']
	want_priority    = 80


	loggerPath = "Main.Text.WatashiWaSugoiDesu"

	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https?://watashiwasugoidesu\.wordpress\.com", url):
			print("wwsd Wants url: '%s'" % url)
			return True
		# print("lnw doesn't want url: '%s'" % url)
		return False

	def preprocessBody(self, soup):

		# Decompose the annoying inline shit.
		# ex: <span style="color:#ffffff;">the truth is out!</span>
		badspans = soup.find_all("span", style=re.compile(r"color\W?:\W?#ffffff", re.I))
		for bad in badspans:
			bad.decompose()

		return soup

class FantasyBooksLiveProcessor(HtmlProcessor.HtmlPageProcessor):

	wanted_mimetypes = ['text/html']
	want_priority    = 80


	loggerPath = "Main.Text.FantasyBooksLive"

	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https?://fantasy\-books\.live", url):
			print("fbl Wants url: '%s'" % url)
			return True
		# print("lnw doesn't want url: '%s'" % url)
		return False

	def preprocessBody(self, soup):

		# Decompose the annoying inline shit.
		# ex: <span style="color:#ffffff;">the truth is out!</span>
		badlinks = soup.find_all('a', href="https://fantasy-books.live/approved-list")
		for bad in badlinks:

			bad.parent.decompose()

		badspans = soup.find_all("div", text=re.compile(r"https://fantasy\-books\.live/approved\-list then this work has been stolen", re.I))
		for bad in badspans:
			print('baddiv', bad)
			bad.decompose()

		return soup

class MayonaizeShrimpLiveProcessor(HtmlProcessor.HtmlPageProcessor):

	wanted_mimetypes = ['text/html']
	want_priority    = 80


	loggerPath = "Main.Text.MayonaizeShrimp"

	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https?://mayonaizeshrimp\.wordpress\.com/", url):
			print("ms Wants url: '%s'" % url)
			return True
		# print("lnw doesn't want url: '%s'" % url)
		return False

	def preprocessBody(self, soup):

		# Decompose the annoying inline shit.
		# ex: <span style="color:#ffffff;">the truth is out!</span>
		badspans = soup.find_all("span", style=re.compile(r"color\W?:\W?#ffffff", re.I))
		for bad in badspans:
			bad.decompose()

		return soup

class RebirthOnlineLiveProcessor(HtmlProcessor.HtmlPageProcessor):

	wanted_mimetypes = ['text/html']
	want_priority    = 80


	loggerPath = "Main.Text.MayonaizeShrimp"

	@staticmethod
	def wantsUrl(url):

		if re.search(r"^https?://(www\.)?rebirth\.online/", url):
			print("ms Wants url: '%s'" % url)
			return True
		# print("lnw doesn't want url: '%s'" % url)
		return False

	def process_css_block(self, css_text):

		ss = tinycss2.parse_stylesheet(css_text, skip_whitespace=True, skip_comments=True)
		# print(ss)

		bad_classes = []

		ssf = [tmp for tmp in ss if tmp.type == "qualified-rule"]
		for rule in ssf:
			prelude = rule.prelude
			content = rule.content
			prelude = [tmp for tmp in prelude if tmp.type != 'whitespace']
			content = [tmp for tmp in content if tmp.type != 'whitespace']
			if (
					len(prelude) == 2 and
					prelude[0].type == "literal" and
					prelude[1].type == "ident" and
					prelude[0].value == "." and
					len(content) == 4 and
					content[0].type == "ident" and
					content[1].type == "literal" and
					content[2].type == "ident" and
					content[3].type == "literal" and
					content[0].lower_value == "display" and
					content[2].lower_value == "none"
				):

				bad_class = prelude[1].value

				bad_classes.append(bad_class)
		return bad_classes

	def preprocessBody(self, soup):
		styles = soup.find_all('style')
		decomp_classes = []
		for style in styles:
			if not style.get_text():
				continue

			new = self.process_css_block(style.get_text())

			decomp_classes.extend(new)

		# Decompose the annoying inline shit.
		for bad_class in decomp_classes:
			bad_p = soup.find_all("p", class_=bad_class)
			for bad in bad_p:
				bad.decompose()

		return soup


