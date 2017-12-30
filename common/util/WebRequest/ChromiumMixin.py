#!/usr/bin/python3

import time
import logging
import random
import traceback
import urllib.parse
import threading
import multiprocessing
import gc

import bs4

import ChromeController

# from cachetools import LRUCache

# class ChromeLRUCache(LRUCache):
# 	def __init__(self, *args, **kwargs):
# 		super().__init__(*args, **kwargs)
# 		self.log = logging.getLogger("Main.ChromeInterfaceCache")

# 	def close_chrome(self, pop_key, to_del):
# 		try:
# 			self.log.info("LRU Cache is closing chromium interface for %s", pop_key)
# 			to_del.close()
# 		except Exception:
# 			self.log.error("Exception in chromium teardown!")
# 			for line in traceback.format_exc().split("\n"):
# 				self.log.error("	%s", line)

# 	def popitem(self):
# 		pop_key, to_del = super().popitem()
# 		self.close_chrome(pop_key, to_del)

# 	def close_by_key(self, key):
# 		pop_key, to_del = self.pop(key)
# 		self.close_chrome(pop_key, to_del)


# 	def get_chromium_instance(self, cr_binary, cr_port):
# 		cpid = multiprocessing.current_process().name
# 		ctid = threading.current_thread().name
# 		csid = "{}-{}".format(cpid, ctid)

# 		if csid in self:
# 			self.log.info("Using existing chromium process.")
# 			# We probe the remote chrome to make sure it's not defunct
# 			try:
# 				self[csid].get_current_url()
# 				return self[csid]
# 			except ChromeController.ChromeControllerException:
# 				self.log.error("Chromium appears to be defunct. Creating new")
# 				self.close_by_key(csid)

# 		self.log.info("Creating Chromium process.")
# 		try:
# 			instance = ChromeController.ChromeRemoteDebugInterface(cr_binary, dbg_port = cr_port)
# 		except Exception as e:
# 			self.log.error("Failure creating chromium process!")
# 			for line in traceback.format_exc().split("\n"):
# 				self.log.error("	%s", line)

# 			# Sometimes the old process is around because
# 			# the GC hasn't seen it, and forcing a collection can fix that.
# 			# Yes, this is HORRIBLE.
# 			gc.collect()

# 			raise e

# 		self[csid] = instance
# 		return instance

# CHROME_CACHE = ChromeLRUCache(maxsize=2)


class WebGetCrMixin(object):
	# creds is a list of 3-tuples that gets inserted into the password manager.
	# it is structured [(top_level_url1, username1, password1), (top_level_url2, username2, password2)]
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._cr_binary = "google-chrome"


	def _syncIntoChromium(self, cr):
		# Headers are a list of 2-tuples. We need a dict
		hdict = dict(self.browserHeaders)
		cr.update_headers(hdict)
		for cookie in self.cj:
			cr.set_cookie(cookie)

	def _syncOutOfChromium(self, cr):
		for cookie in cr.get_cookies():
			self.cj.set_cookie(cookie)

	def getItemChromium(self, itemUrl):
		self.log.info("Fetching page for URL: '%s' with Chromium" % itemUrl)

		with ChromeController.ChromeContext(self._cr_binary) as cr:

			self._syncIntoChromium(cr)

			response = cr.blocking_navigate_and_get_source(itemUrl, timeout=10)

			raw_url = cr.get_current_url()
			fileN = urllib.parse.unquote(urllib.parse.urlparse(raw_url)[2].split("/")[-1])
			fileN = bs4.UnicodeDammit(fileN).unicode_markup

			self._syncOutOfChromium(cr)

		# Probably a bad assumption
		if response['binary']:
			mType = "application/x-binary"
		else:
			mType = "text/html"

		# So, self._cr.page_source appears to be the *compressed* page source as-rendered. Because reasons.
		content = response['content']
		return content, fileN, mType

	def getHeadTitleChromium(self, url, referrer=None):
		self.log.info("Getting HEAD with Chromium")
		if not referrer:
			referrer = url

		with ChromeController.ChromeContext(self._cr_binary) as cr:
			self._syncIntoChromium(cr)

			cr.blocking_navigate(referrer)
			time.sleep(random.uniform(2, 6))
			cr.blocking_navigate(url)

			title, cur_url = cr.get_page_url_title()

			self._syncOutOfChromium(cr)

		self.log.info("Resolved URL for %s -> %s", url, cur_url)

		ret = {
			'url': cur_url,
			'title': title,
		}
		return ret

	def getHeadChromium(self, url, referrer=None):
		self.log.info("Getting HEAD with Chromium")
		if not referrer:
			referrer = url

		with ChromeController.ChromeContext(self._cr_binary) as cr:
			self._syncIntoChromium(cr)


			cr.blocking_navigate(referrer)
			time.sleep(random.uniform(2, 6))
			cr.blocking_navigate(url)

			dummy_title, cur_url = cr.get_page_url_title()

			self._syncOutOfChromium(cr)

		return cur_url


	def chromiumGetRenderedItem(self, url):

		with ChromeController.ChromeContext(self._cr_binary) as cr:
			self._syncIntoChromium(cr)

			# get_rendered_page_source
			cr.blocking_navigate(url)


			content = cr.get_rendered_page_source()
			mType = 'text/html'
			fileN = ''
			self._syncOutOfChromium(cr)


		return content, fileN, mType


	def __del__(self):
		# print("ChromiumMixin destructor")
		sup = super()
		if hasattr(sup, '__del__'):
			sup.__del__()

	# def stepThroughCloudFlare_cr(self, url, titleContains='', titleNotContains=''):
	# 	'''
	# 	Use Selenium+Chromium to access a resource behind cloudflare protection.

	# 	Params:
	# 		``url`` - The URL to access that is protected by cloudflare
	# 		``titleContains`` - A string that is in the title of the protected page, and NOT the
	# 			cloudflare intermediate page. The presence of this string in the page title
	# 			is used to determine whether the cloudflare protection has been successfully
	# 			penetrated.

	# 	The current WebGetRobust headers are installed into the selenium browser, which
	# 	is then used to access the protected resource.

	# 	Once the protected page has properly loaded, the cloudflare access cookie is
	# 	then extracted from the selenium browser, and installed back into the WebGetRobust
	# 	instance, so it can continue to use the cloudflare auth in normal requests.

	# 	'''

	# 	if (not titleContains) and (not titleNotContains):
	# 		raise ValueError("You must pass either a string the title should contain, or a string the title shouldn't contain!")

	# 	if titleContains and titleNotContains:
	# 		raise ValueError("You can only pass a single conditional statement!")

	# 	self.log.info("Attempting to access page through cloudflare browser verification.")

	# 	dcap = dict(DesiredCapabilities.Chromium)
	# 	wgSettings = dict(self.browserHeaders)

	# 	# Install the headers from the WebGet class into Chromium
	# 	dcap["Chromium.page.settings.userAgent"] = wgSettings.pop('User-Agent')
	# 	for headerName in wgSettings:
	# 		dcap['Chromium.page.customHeaders.{header}'.format(header=headerName)] = wgSettings[headerName]

	# 	driver = selenium.webdriver.Chromium(desired_capabilities=dcap)
	# 	driver.set_window_size(1024, 768)

	# 	driver.get(url)

	# 	if titleContains:
	# 		condition = EC.title_contains(titleContains)
	# 	elif titleNotContains:
	# 		condition = title_not_contains(titleNotContains)
	# 	else:
	# 		raise ValueError("Wat?")

	# 	try:
	# 		WebDriverWait(driver, 20).until(condition)
	# 		success = True
	# 		self.log.info("Successfully accessed main page!")
	# 	except TimeoutException:
	# 		self.log.error("Could not pass through cloudflare blocking!")
	# 		success = False
	# 	# Add cookies to cookiejar

	# 	for cookie in driver.get_cookies():
	# 		self.addSeleniumCookie(cookie)
	# 		#print cookie[u"value"]

	# 	self._syncCookiesFromFile()

	# 	return success
