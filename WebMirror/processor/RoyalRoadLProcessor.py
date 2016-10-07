
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




class RoyalRoadLProcessor(HtmlProcessor.HtmlPageProcessor):


	wanted_mimetypes = ['text/html']
	want_priority    = 60

	loggerPath = "Main.Text.HtmlProc"


	@staticmethod
	def wantsUrl(url):
		if "royalroadl.com/fiction/chapter/" in url:
			return True
		if "royalroadl.com/forum/showthread.php?tid=" in url:
			return True
		return False



	def fixCss(self, soup):
		'''
		So, because the color scheme of our interface can vary from the original, we need to fix any cases
		of white text. However, I want to preserve *most* of the color information.
		Therefore, we look at all the inline CSS, and just patch where needed.
		'''

		hascss = soup.find_all(True, attrs={"style" : True})


		# parser = tinycss.make_parser('page3')

		hexr = re.compile('(#(?:[a-fA-F0-9]{6})|#(?:[a-fA-F0-9]{3}))')


		for item in hascss:
			if item['style']:
				ststr = item['style']
				# Prevent inline fonts.
				if 'font:' in ststr.lower() or 'font :' in ststr.lower() :
					item['style'] = ''
				if 'font-family:' in ststr.lower() or 'font-family :' in ststr.lower() :
					item['style'] = ''
				# Disable all explicit width settings.
				if 'width' in ststr.lower():
					item['style'] = ''
				if 'max-width' in ststr.lower():
					item['style'] = ''

				if 'background-image:' in ststr.lower():
					item['style'] = ''

				old = hexr.findall(ststr)
				for match in old:
					color = webcolors.hex_to_rgb(match)
					mean = sum(color)/len(color)

					if mean > 180:
						above = mean - 150
						color = tuple((max(255-cval, 0) for cval in color))
						new = webcolors.rgb_to_hex(color)
						item['style'] = item['style'].replace(match, new)

		return soup

	def removeClasses(self, soup):
		cnt = 0

		validattrs = [
			'href',
			'src',
			# Allow inline styles
			'style',
			'cellspacing',
			'cellpadding',
			'border',
			'colspan',
			'onclick',
			'type',
			'value',
			'width',
		]

		for item in [item for item in soup.find_all(True) if item]:
			tmp_valid = validattrs[:]
			clean = True
			for name, attr in self.preserveAttrs:
				if item.name == name:
					if attr:
						tmp_valid.append(attr)

					else:
						# Preserve all attributes
						clean = False
			if clean and item.attrs:

				for attr, value in list(item.attrs.items()):
					if attr == 'style' and 'float' in value:
						del item[attr]
					elif attr not in tmp_valid:
						del item[attr]

			# Set the class of tables set to have no borders to the no-border css class for later rendering.
			if item.name == "table" and item.has_attr("border") and item['border'] == "0":
				if not item.has_attr("class"):
					item['class'] = ""
				item['class'] += " noborder"


		return soup




	def preprocessBody(self, soup):

		# Destroy the oversized header cover image
		for header_div in soup.find_all("div", class_='fic-header'):
			for img in header_div.find_all("img", id=re.compile(r"^cover\-")):
				img.decompose()

		# And peoples avatars
		for comment in soup.find_all("div", class_='comment-container'):
			for imgdiv in comment.find_all("div", class_='media-left'):
				imgdiv.decompose()


		# Relayout the
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

	def postprocessBody(self, soup):
		for link in soup.find_all("a"):
			if link.has_attr("href"):
				if "javascript:if(confirm(" in link['href']:
					qs = urllib.parse.urlsplit(link['href']).query
					link['href'] = "/viewstory.php?{}".format(qs)

		return soup
