
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

	# Miscellaneous spot-fixes for specific sites.
	def spotPatch(self, soup):

		# Replace <pre> tags on wattpad.
		# wp_div = soup.find_all('div', class_="panel-reading")
		# for item in wp_div:
		# Fukkit, just nuke them in general
		for pre in soup.find_all("div", class_='story-content '):
			pre.name = "div"
			contentstr = pre.encode_contents().decode("utf-8")

			formatted = markdown.markdown(contentstr.strip(), extensions=["mdx_linkify"])
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
