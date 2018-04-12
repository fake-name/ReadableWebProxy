
import pprint
import re
import bs4
import collections
import datetime
import json

import xml.etree.ElementTree as et
import xmljson
import WebMirror.OutputFilters.FilterBase

import common.util.urlFuncs
import common.database as db

MIN_RATING = 5

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

def clean_parsed_data(d):
	if isinstance(d, (dict, collections.OrderedDict)):
		d = dict(d)
		if 'ApiChapterList' in d:
			d = clean_parsed_data(d['ApiChapterList'])

			# So XML is annoying, and lists with a single item basically get implicitly unwrapped
			# Anyways, we know this *should* be a list, so if it's not, wrap it into a list manually
			if isinstance(d, dict):
				d = [d]
		else:
			for key in list(d.keys()):
				d[key] = clean_parsed_data(d[key])
				if key in ['FirstUpdate', 'LastUpdate', 'Date']:
					d[key] = datetime.datetime.utcfromtimestamp(d[key])

	elif isinstance(d, (list, tuple)):
		d = [clean_parsed_data(tmp) for tmp in d]
	elif isinstance(d, str):
		d = d.strip()

	return d

class RRLJsonXmlSeriesUpdateFilter(WebMirror.OutputFilters.FilterBase.FilterBase):


	wanted_mimetypes = [
							'text/xml',
							'application/xml',
							'text/json',
							'application/json',
						]
	want_priority    = 50

	loggerPath = "Main.Filter.RoyalRoad.XmlJsonSeries"


	@staticmethod
	def wantsUrl(url):
		want = set([
			'https://royalroadl.com/api/',
			'http://royalroadl.com/api/',
			'https://www.royalroadl.com/api/',
			'http://www.royalroadl.com/api/',
		])
		url = url.lower()
		if any([url.startswith(tmp) for tmp in want]):

			print("RRLJsonXmlSeriesUpdateFilter Wants url: '%s'" % url)
			return True
		# print("RRLJsonXmlSeriesUpdateFilter doesn't want url: '%s'" % url)
		return False

	def __init__(self, **kwargs):

		self.kwargs     = kwargs


		self.pageUrl    = kwargs['pageUrl']

		self.content    = kwargs['pgContent']
		self.mtype      = kwargs['mimeType']
		self.db_sess    = kwargs['db_sess']

		print(kwargs.keys())

		self.log.info("Processing RoyalRoadL Json/XML Item")
		super().__init__(**kwargs)


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################


	def extractSeriesReleases(self, seriesPageUrl, soup):

		containers = soup.find_all('div', class_='fiction-list-item')
		# print(soup)
		# print("container: ", containers)
		if not containers:
			return []
		urls = []
		for item in containers:
			div = item.find('h2', class_='fiction-title')
			a = div.find("a")
			if a:
				url = common.util.urlFuncs.rebaseUrl(a['href'], seriesPageUrl)
				urls.append(url)
			else:
				self.log.error("No series in container: %s", item)

		return set(urls)


	def retrigger_pages(self, releases):
		self.log.info("Total releases found on page: %s. Forcing retrigger of item pages.", len(releases))

		for release_url in releases:
			self.retrigger_page(release_url)

	def load_xml(self):
		xmlstring = re.sub(' xmlns="[^"]+"', '', self.content, count=1)
		tree = et.fromstring(xmlstring)
		loaded = xmljson.parker.data(tree)
		loaded = clean_parsed_data(loaded)

		loaded['ApiFictionInfoWithChapters'].sort(key=lambda x: x['LastUpdate'])

		return loaded

	def load_json(self):
		loaded = json.loads(self.content)
		loaded.sort(key=lambda x: x['LastUpdate'])
		content = {'ApiFictionInfoWithChapters' : loaded}
		content = clean_parsed_data(content)
		return content

	def processParsedData(self, loaded):
		# print(loaded)
		pass


	def processPage(self, url, content):
		self.log.info("processPage() call: %s, %s", self.mtype, self.pageUrl)

		if self.mtype in ['text/xml', 'application/xml']:
			loaded = self.load_xml()
		elif self.mtype in ['text/json', 'application/json']:
			loaded = self.load_json()
		else:
			self.log.error("Unknown content type (%s)!", self.mtype)

		self.processParsedData(loaded)
		return loaded


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################



	def extractContent(self):
		# print("Call to extract!")
		# print(self.amqpint)

		return self.processPage(self.pageUrl, self.content)



def test():
	print("Test mode!")
	import logSetup
	import settings
	from WebMirror.Engine import SiteArchiver

	logSetup.initLogging()


	# urls = [
	# 		'https://royalroadl.com/api/fiction/updates?apiKey=' + settings.RRL_API_KEY,
	# 		# 'https://royalroadl.com/api/fiction/newreleases?apiKey=' + settings.RRL_API_KEY,
	# ]

	# for url in urls:
	# 	with db.session_context() as sess:
	# 		archiver = SiteArchiver(None, sess, None)
	# 		archiver.synchronousJobRequest(url, ignore_cache=True)

	with open("fiction_updates.xml", "r") as fp:
		content = fp.read()

	instance = RRLJsonXmlSeriesUpdateFilter(pageUrl="https://royalroadl.com/api/fiction/updates?apiKey=" + settings.RRL_API_KEY, pgContent=content, mimeType="application/xml", db_sess=None)
	print(instance)
	extracted1 = instance.extractContent()

	with open("json_reenc.json", "r") as fp:
		content2 = fp.read()

	instance = RRLJsonXmlSeriesUpdateFilter(pageUrl="https://royalroadl.com/api/fiction/updates?apiKey=" + settings.RRL_API_KEY, pgContent=content2, mimeType="application/json", db_sess=None)
	print(instance)
	extracted2 = instance.extractContent()
	# print("Extracted:", extracted1)
	# print("Extracted:", extracted2)
	with open("F1.txt", "w") as fp:
		fp.write(pprint.pformat(extracted1))
	with open("F2.txt", "w") as fp:
		fp.write(pprint.pformat(extracted2))

if __name__ == "__main__":
	test()


