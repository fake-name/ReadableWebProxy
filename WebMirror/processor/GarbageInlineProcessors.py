
import re
import markdown
import bs4
import tinycss2

from . import HtmlProcessor

########################################################################################################################
#
#	Misc fixer classes for various retarded "protection" shit translators do.
#
########################################################################################################################



class CreativeNovelsPageProcessor(HtmlProcessor.HtmlPageProcessor):

	wanted_mimetypes = ['text/html']
	want_priority    = 80

	loggerPath = "Main.Text.CreativeNovels"

	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https?://(?:www\.)?creativenovels.com", url):
			print("CreativeNovels Wants url: '%s'" % url)
			return True
		# print("hecatescorner doesn't want url: '%s'" % url)
		return False

	def preprocessBody(self, soup):

		for bad in soup.find_all("style"):
			bad.decompose()
		for bad in soup.find_all("noscript"):
			bad.decompose()

		return soup

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



class XiAiNovelPageProcessor(HtmlProcessor.HtmlPageProcessor):

	wanted_mimetypes = ['text/html']
	want_priority    = 80

	loggerPath = "Main.Text.XiAiNovel"

	# Miscellaneous spot-fixes for specific sites.
	def spotPatch(self, soup):

		# Replace <pre> tags on wattpad.
		# wp_div = soup.find_all('div', class_="panel-reading")
		# for item in wp_div:
		# Fukkit, just nuke them in general
		for pre in soup.find_all("pre"):
			pre.name = "div"
			contentstr = pre.encode_contents().decode("utf-8")

			formatted = markdown.markdown(contentstr, extensions=["linkify"])
			formatted = WebRequest.as_soup(formatted)
			if formatted.find("html"):
				formatted.html.unwrap()
				formatted.body.unwrap()
				pre.replace_with(formatted)
			# print(pre)
		return soup


	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https?://(?:www\.)?xiainovel\.com", url):
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

		# Decompose the annoying inline shit.
		# ex: <span style="color:#ffffff;">the truth is out!</span>
		badspans = soup.find_all("span", style=re.compile(r"color\W?:\W?#000909", re.I))
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


class ConvallariasLibraryProcessor(HtmlProcessor.HtmlPageProcessor):

	wanted_mimetypes = ['text/html']
	want_priority    = 80


	loggerPath = "Main.Text.ConvallariasLibrary"

	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https?://www\.convallariaslibrary\.com/", url):
			print("ms Wants url: '%s'" % url)
			return True
		# print("lnw doesn't want url: '%s'" % url)
		return False

	def preprocessBody(self, soup):

		# Decompose the annoying inline shit.
		# ex: <span style="color:#ffffff;">the truth is out!</span>
		badspans = soup.find_all("span", style=re.compile(r"font-size\W?:\W?0px", re.I))
		for bad in badspans:
			bad.decompose()

		return soup

class RebirthOnlineLiveProcessor(HtmlProcessor.HtmlPageProcessor):

	wanted_mimetypes = ['text/html']
	want_priority    = 80


	loggerPath = "Main.Text.RebirthOnline"

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

			print("Rule:", (prelude, content))

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
			if (
					len(prelude) == 2 and
					prelude[0].type == "literal" and
					prelude[1].type == "ident" and
					prelude[0].value == "." and
					"left" in str(content) and
					"-9999px" in str(content)
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



class AfterAugustMakingProcessor(HtmlProcessor.HtmlPageProcessor):

	wanted_mimetypes = ['text/html']
	want_priority    = 80


	loggerPath = "Main.Text.AfterAugustMaking"

	@staticmethod
	def wantsUrl(url):

		if re.search(r"^https?://translations\.afteraugustmaking\.me/", url):
			print("AAM Wants url: '%s'" % url)
			return True
		# print("lnw doesn't want url: '%s'" % url)
		return False


	def preprocessBody(self, soup):
		for bad in soup.find_all('div', id='sitedescription'):
			bad.decompose()
		for bad in soup.find_all('td', id='staticpanel'):
			bad.decompose()
		for bad in soup.find_all('td', id='foohide'):
			bad.decompose()
		for bad in soup.find_all('canvas'):
			bad.decompose()

		for styled_div in soup.find_all("div", style=True):
			styled_div.attrs = {}

		if soup.table:
			soup.table.unwrap()

		for wat in soup.find_all("ng-view"):
			wat.unwrap()

		textbody = soup.find("h4", id='novelText')
		if textbody:
			for text in textbody.find_all(text=True):
				content = soup.new_tag("p")
				for line in text.split("\n"):
					content.append(soup.new_string(line))
					content.append(soup.new_tag('br'))

				text.replace_with(content)


		for span in soup.find_all("span", title=True):
			replacement = soup.new_tag('sup')
			replacement.string = span['title']
			span.replace_with(replacement)

			wrapper1 = soup.new_tag("sub")
			replacement.wrap(wrapper1)

			wrapper2 = soup.new_tag("p")
			replacement.wrap(wrapper2)



		return soup


