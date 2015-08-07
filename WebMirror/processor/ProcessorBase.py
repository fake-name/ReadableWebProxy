


import runStatus
runStatus.preloadDicts = False

# import Levenshtein as lv



import WebMirror.util.urlFuncs as urlFuncs
import urllib.parse
import WebMirror.LogBase as LogBase
import abc

import config


class DownloadException(Exception):
	pass



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




GLOBAL_BAD = [
			'gprofiles.js',
			'netvibes.com',
			'accounts.google.com',
			'edit.yahoo.com',
			'add.my.yahoo.com',
			'public-api.wordpress.com',
			'r-login.wordpress.com',
			'twitter.com',
			'facebook.com',
			'public-api.wordpress.com',
			'wretch.cc',
			'ws-na.amazon-adsystem.com',
			'delicious.com',
			'paypal.com',
			'digg.com',
			'topwebfiction.com',
			'/page/page/',
			'addtoany.com',
			'stumbleupon.com',
			'delicious.com',
			'reddit.com',
			'newsgator.com',
			'technorati.com',
			'feeds.wordpress.com',
			'www.addtoany.com'
	]

GLOBAL_DECOMPOSE_BEFORE = [
			{'name'     : 'likes-master'},  # Bullshit sharing widgets
			{'id'       : 'jp-post-flair'},
			{'class'    : 'post-share-buttons'},
			{'class'    : 'commentlist'},  # Scrub out the comments so we don't try to fetch links from them
			{'class'    : 'comments'},
			{'id'       : 'comments'},
		]

GLOBAL_DECOMPOSE_AFTER = []

class PageProcessor(LogBase.LoggerMixin, metaclass=abc.ABCMeta):


	@abc.abstractproperty
	def wanted_mimetypes(self):
		pass

	@abc.abstractproperty
	def want_priority(self):
		pass


	@abc.abstractmethod
	def extractContent(self):
		pass

	@staticmethod
	def wantsUrl(url):
		return True

	_relinkDomains  = []
	_scannedDomains = []
	_badwords       = []


	# Hook so plugins can modify the internal URLs as part of the relinking process
	def preprocessReaderUrl(self, inUrl):
		return inUrl


	def convertToReaderUrl(self, inUrl, resource=False):
		inUrl = urlFuncs.urlClean(inUrl)
		inUrl = self.preprocessReaderUrl(inUrl)
		# The link will have been canonized at this point

		# Fix protocol-relative URLs
		if inUrl.startswith("//"):
			if hasattr(self, "pageUrl"):
				scheme = urllib.parse.urlsplit(self.pageUrl).scheme
			else:
				self.log.warning("No pageUrl member variable? Guessing about the protocol type!")
				scheme = "http"
			inUrl = "{}:{}".format(scheme, inUrl)

		if resource:
			prefix = "RESOURCE:{}".format(config.relink_secret)
		else:
			prefix = "CONTENT:{}".format(config.relink_secret)
		url = '%s%s' % (prefix.lower(), urllib.parse.quote(inUrl))
		return url

	def convertToReaderImage(self, inStr):
		inStr = urlFuncs.urlClean(inStr)
		return self.convertToReaderUrl(inStr, resource=True)

	def relink(self, soup, imRelink=None):
		# The google doc reader relinking mechanisms requires overriding the
		# image relinking mechanism. As such, allow that to be overridden
		# if needed
		# print("relink call!")
		# print(self._relinkDomains)
		if not imRelink:
			imRelink = self.convertToReaderImage


		for (isImg, tag, attr) in urlFuncs.urlContainingTargets:

			if not isImg:
				for link in soup.findAll(tag):
					try:
						# print("Link!", self.checkRelinkDomain(link[attr]), link[attr])
						# if self.checkRelinkDomain(link[attr]):
						link[attr] = self.convertToReaderUrl(link[attr])

						if "google.com" in urllib.parse.urlsplit(link[attr].lower()).netloc:
							link[attr] = urlFuncs.trimGDocUrl(link[attr])
							# print("Relinked", link[attr])
					except KeyError:
						continue

			else:
				for link in soup.findAll(tag):
					try:
						link[attr] = imRelink(link[attr])

						if tag == 'img':
							# Force images that are oversize to fit the window.
							link["style"] = 'max-width: 95%;'

							if 'width' in link.attrs:
								del link.attrs['width']
							if 'height' in link.attrs:
								del link.attrs['height']

					except KeyError:
						continue


		# Keyhole patch for fictionpress next/prev buttons onclick elements.
		for button in [item for item in soup.findAll('button') if item.has_attr("onclick")]:
			if button['onclick'].startswith("self.location='") \
				and button['onclick'].endswith("'")            \
				and button['onclick'].count("'") == 2:
								prefix, url, postfix = button['onclick'].split("'")
				url = urlFuncs.rebaseUrl(url, self.pageUrl)
				url = self.convertToReaderUrl(url)
				button['onclick'] = "'".join((prefix, url, postfix))

		return soup



	# check if domain `url` is a sub-domain of the domains we should relink.
	def checkRelinkDomain(self, url):
		# if "drive" in url:

		# print("CheckDomain", any([rootUrl in url.lower() for rootUrl in self._relinkDomains]), url)
		# print(self._relinkDomains)
		# dom = list(self._relinkDomains)
		# dom.sort()
		# for rootUrl in dom:
		# 	print(rootUrl in url.lower(), rootUrl)

		return any([rootUrl in url.lower() for rootUrl in self._relinkDomains])



	# check if domain `url` is a sub-domain of the scanned domains.
	def checkDomain(self, url):
		# if "drive" in url:
		for rootUrl in self._scannedDomains:
			if urllib.parse.urlsplit(url).netloc:
				if urllib.parse.urlsplit(url).netloc == rootUrl:
					return True

			if url.lower().startswith(rootUrl):
				return True

		# print("CheckDomain False", url)
		return False

	def checkFollowGoogleUrl(self, url):
		'''
		I don't want to scrape outside of the google doc document context.

		Therefore, if we have a URL that's on docs.google.com, and doesn't have
		'/document/d/ in the URL, block it.
		'''
		# Short circuit for non docs domains
		url = url.lower()
		netloc = urllib.parse.urlsplit(url).netloc
		if not "docs.google.com" in netloc:
			return True

		if '/document/d/' in url:
			return True

		return False


	def processLinkItem(self, url, baseUrl):
		url = urlFuncs.clearOutboundProxy(url)
		url = urlFuncs.clearBitLy(url)

		for badword in self._badwords:
			if badword in url:
				return


		url = urlFuncs.urlClean(url)

		if "google.com" in urllib.parse.urlsplit(url.lower()).netloc:
			url = urlFuncs.trimGDocUrl(url)

			if url.startswith('https://docs.google.com/document/d/images'):
				return

			# self.log.info("Resolved URL = '%s'", url)
			ret = self.processNewUrl(url, baseUrl)
			return ret
			# self.log.info("New G link: '%s'", url)

		else:
			# Remove any URL fragments causing multiple retreival of the same resource.
			if url != urlFuncs.trimGDocUrl(url):
				print('Old URL: "%s"' % url)
				print('Trimmed: "%s"' % urlFuncs.trimGDocUrl(url))
				raise ValueError("Wat? Url change? Url: '%s'" % url)
			ret = self.processNewUrl(url, baseUrl)
			# print("Returning:", ret)
			return ret
			# self.log.info("Newlink: '%s'", url)


	def extractLinks(self, soup, baseUrl):
		# All links have been resolved to fully-qualified paths at this point.
		ret = []
		print("Extracting links!")
		for (dummy_isImg, tag, attr) in urlFuncs.urlContainingTargets:

			for link in soup.findAll(tag):

				# Skip empty anchor tags
				try:
					url = link[attr]
				except KeyError:
					continue


				item = self.processLinkItem(url, baseUrl)
				if item:
					ret.append(item)

		return ret


	def extractImages(self, soup, baseUrl):
		ret = []
		for imtag in soup.find_all("img"):
						# Skip empty anchor tags
			try:
				url = imtag["src"]
			except KeyError:
				continue

			item = self.processImageLink(url, baseUrl)
			if item:
				ret.append(item)
		return ret



	def postprocessBody(self, soup):
		return soup

	def preprocessBody(self, soup):
		return soup


	# Methods to allow the child-class to modify the content at various points.
	def extractTitle(self, srcSoup, url):

		if srcSoup.title:
			return srcSoup.title.get_text().strip()


		return "'%s' has no title!" % url



	def processNewUrl(self, url, baseUrl=None, istext=True):
		if not url.lower().startswith("http"):
			if baseUrl:
				# If we have a base-url to extract the scheme from, we pull that out, concatenate
				# it onto the rest of the url segments, and then unsplit that back into a full URL
				scheme = urllib.parse.urlsplit(baseUrl.lower()).scheme
				rest = urllib.parse.urlsplit(baseUrl.lower())[1:]
				params = (scheme, ) + rest

				# self.log.info("Had to add scheme (%s) to URL: '%s'", scheme, url)
				url = urllib.parse.urlunsplit(params)

			elif self.ignoreBadLinks:
				self.log.error("Skipping a malformed URL!")
				self.log.error("Bad URL: '%s'", url)
				return
			else:
				raise ValueError("Url isn't a url: '%s'" % url)
		if urlFuncs.isGdocUrl(url) or urlFuncs.isGFileUrl(url):
			if urlFuncs.trimGDocUrl(url) != url:
				raise ValueError("Invalid link crept through! Link: '%s'" % url)


		if not url.lower().startswith('http'):
			raise ValueError("Failure adding scheme to URL: '%s'" % url)

		if '/view/export?format=zip' in url:
			raise ValueError("Wat?")

		return url



	# Proxy call for enforcing call-correctness
	@classmethod
	def process(cls, params):
		expected = [
			'pageUrl',
			'pgContent',
			'mimeType',
			'baseUrls',
			'loggerPath',
			'badwords',
			'decompose',
			'decomposeBefore',
			'fileDomains',
			'allImages',
			'ignoreBadLinks',
			'stripTitle',
			'relinkable',
			'destyle',
			'preserveAttrs',
		]

		assert len(params) == len(expected)
		for expect in expected:
			assert expect in params

		instance = cls(**params)
		ret = instance.extractContent()

		# Copy the mime-type into the return, since bothering to round-trip
		# it through the processor class is silly.
		ret['mimeType'] = params['mimeType']

		gdoc_ret_expected = ['plainLinks', 'rsrcLinks', 'title', 'contents', 'mimeType', 'resources']
		text_ret_expected = ['plainLinks', 'rsrcLinks', 'title', 'contents', 'mimeType']
		file_ret_expected = ['file', 'content', 'fName', 'mimeType']
		if "file" in ret and ret['file'] == True:
			assert len(ret) == len(file_ret_expected), "File response length mismatch! Expect: %s, received %s (expect keys: '%s', received keys '%s')" % (len(file_ret_expected), len(ret), file_ret_expected, list(ret.keys()))
			for expect in file_ret_expected:
				assert expect in ret, "Expected key '%s' in ret (keys: '%s')" % (expect, list(ret.keys()))
		else:

			if len(ret) == len(text_ret_expected):
				for expect in text_ret_expected:
					assert expect in ret, "Expected key '%s' in ret (keys: '%s')" % (expect, list(ret.keys()))
			elif len(ret) == len(gdoc_ret_expected):
				for expect in gdoc_ret_expected:
					assert expect in ret, "Expected key '%s' in ret (keys: '%s')" % (expect, list(ret.keys()))
			else:
				raise ValueError("Invalid number of items in ret. Keys = '%s'" % list(ret.keys()))

		return ret

