


import runStatus
runStatus.preloadDicts = False

# import Levenshtein as lv



import common.util.urlFuncs as urlFuncs
import urllib.parse
import common.LogBase as LogBase
import abc

import config




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




class PageProcessor(LogBase.LoggerMixin, metaclass=abc.ABCMeta):


	@abc.abstractproperty
	def wanted_mimetypes(self):
		pass

	# The first plugin with mimetype_catchall == True gets anything the other plugins didn't match.
	mimetype_catchall = False

	@abc.abstractproperty
	def want_priority(self):
		pass


	@abc.abstractmethod
	def extractContent(self):
		pass

	@staticmethod
	def wantsUrl(url):
		return True

	@staticmethod
	def wantsFromContent(content):
		return True

	_relinkDomains  = []
	_scannedDomains = []
	_badwords       = []


	_no_ret = False

	# Hook so plugins can modify the internal URLs as part of the relinking process
	def preprocessReaderUrl(self, inUrl):
		return inUrl


	def convertToReaderUrl(self, inUrl, resource=False):
		inUrl = urlFuncs.urlClean(inUrl)
		inUrl = self.preprocessReaderUrl(inUrl)
		# The link will have been canonized at this point

		# Do not relink inline images
		if inUrl.startswith("data:"):
			return inUrl

		# or links that are NOP()ed with javascript
		if inUrl.startswith("javascript:void(0);"):
			return inUrl


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
					except TypeError:
						# Empty href tags, not sure how this happens.
						continue
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

					except TypeError:
						continue
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

		url = urlFuncs.cleanUrl(url)
		if not url:
			return None

		# Fucking tumblr redirects.
		if url.startswith("https://www.tumblr.com/login"):
			return None

		for badword in self._badwords:
			if badword in url:
				return

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
		# print("Extracting links!")
		for (dummy_isImg, tag, attr) in urlFuncs.urlContainingTargets:

			for link in soup.findAll(tag):

				# Skip empty anchor tags
				try:
					url = link[attr]
				except KeyError:
					continue


				item = self.processLinkItem(url, baseUrl)
				if item:
					ret.append(item.strip())

		return set(ret)

	def processImageLink(self, url, baseUrl):

		# Skip tags with `img src=""`.
		# No idea why they're there, but they are
		if not url:
			return None

		# # Filter by domain
		# if not self.allImages and not any([base in url for base in self._fileDomains]):
		# 	return

		# and by blocked words
		hadbad = False
		urll = url.lower()
		for badword in self._badwords:
			if badword.lower() in urll:
				hadbad = True
		if hadbad:
			return None


		url = urlFuncs.urlClean(url)

		return self.processNewUrl(url, baseUrl=baseUrl, istext=False)

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
		return set(ret)



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
		# if urlFuncs.isGdocUrl(url) or urlFuncs.isGFileUrl(url):
		# 	if urlFuncs.trimGDocUrl(url) != url:
		# 		raise ValueError("Invalid link crept through! Link: '%s'" % url)


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
			'db_sess',
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
			'type',
			'decompose_svg',
			'message_q',
			'job',
			'wg_proxy',
		]

		assert len(params) == len(expected), "Incorrect number of passed plugin parameters?"
		for expect in expected:
			assert expect in params, "Plugin missing expected argument: '%s'" % expect

		assert params['job'].url
		assert params['job'].netloc
		assert params['job'].starturl
		assert params['job'].distance is not None
		assert params['job'].priority

		instance = cls(**params)
		# print("Instantiated plugin: ", instance)
		# print("Now calling: ", instance.extractContent)
		ret = instance.extractContent()
		# print("Call returned data: ", bool(ret))

		# Filters don't return anything, so
		# don't check for return stuff
		if instance._no_ret:
			return

		# Copy the mime-type into the return, since bothering to round-trip
		# it through the processor class is silly.
		ret['mimeType'] = params['mimeType']

		# Google doc returns include inline content (images, usualy)
		gdoc_ret_expected = ['plainLinks', 'rsrcLinks', 'title', 'contents', 'mimeType', 'resources']

		# Normal return have just markup, title, contents, and the mime-type
		text_ret_expected = ['plainLinks', 'rsrcLinks', 'title', 'contents', 'mimeType']

		# File content doesn't contain links or a title, but does include the file-name (generally from the URL or the content-disposition headers)
		file_ret_expected = ['file', 'content', 'fName', 'mimeType']

		# Rss content is a set of responses (one per article), so we just have two high-level entries.
		rss_ret_expected  = ['mimeType', 'rss-content']

		if "file" in ret and ret['file'] == True:
			assert len(ret) == len(file_ret_expected), "File response length mismatch! Expect: %s, received %s (expect keys: '%s', received keys '%s')" % (len(file_ret_expected), len(ret), file_ret_expected, list(ret.keys()))
			for expect in file_ret_expected:
				assert expect in ret, "Expected key '%s' in ret (keys: '%s')" % (expect, list(ret.keys()))
		elif 'rss-content' in ret:
			for expect in rss_ret_expected:
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

		# These assertions will generally throw if something has invalidate the db session.
		# Check for anonymous context managers
		assert params['job'].url
		assert params['job'].netloc
		assert params['job'].starturl
		assert params['job'].distance is not None
		assert params['job'].priority


		return ret

