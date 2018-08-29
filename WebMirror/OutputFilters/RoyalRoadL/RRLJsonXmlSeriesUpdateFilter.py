
import pprint
import re
import bs4
import collections
import datetime
import json

import xmljson
import WebRequest
import xml.etree.ElementTree as et

import settings
import WebMirror.OutputFilters.FilterBase
import WebMirror.OutputFilters.util.TitleParsers as titleParsers
import WebMirror.OutputFilters.util.MessageConstructors as msgpackers

import common.util.urlFuncs
import common.database as db

import cachetools

MIN_RATING   = 2.5
MIN_RATE_CNT = 3
MIN_CHAPTERS = 4

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



@cachetools.cached(cachetools.TTLCache(100, 60*30), key=lambda wg, url: cachetools.keys.hashkey(url))
def get_json(wg, url):
	accept_override = {'Accept' : 'application/json,*/*'}
	return wg.getJson(url, addlHeaders=accept_override)



@cachetools.cached(cachetools.TTLCache(100, 60*30), key=lambda wg, url: cachetools.keys.hashkey(url))
def get_spage(wg, url):
	accept_override = {'PlzAddRating' : 'I\'m only making these requests because the series statistics, url slug (for chapter links) and author name '
		+ 'aren\'t available as part of the info or chapters API endpoints already! I just need `author`, chapter url slug, `ratingValue` and `ratingCount`.'}
	return wg.getSoup(url, addlHeaders=accept_override)




def clean_parsed_data(d):

	if isinstance(d, (dict, collections.OrderedDict)):
		d = dict(d)
		if 'chapters' in d and not isinstance(d['chapters'], list):
			d = clean_parsed_data(d['chapters'])

			# So XML is annoying, and lists with a single item basically get implicitly unwrapped
			# Anyways, we know this *should* be a list, so if it's not, wrap it into a list manually
			if isinstance(d, dict):
				d = [d]
		else:
			for key in list(d.keys()):
				d[key] = clean_parsed_data(d[key])
				if key in ['firstUpdate', 'lastUpdate', 'date']:
					d[key] = datetime.datetime.utcfromtimestamp(d[key])

	elif isinstance(d, (list, tuple)):
		d = [clean_parsed_data(tmp) for tmp in d]
	elif isinstance(d, str):
		d = d.strip()
	elif isinstance(d, (int, float)):
		pass
	elif d is None:
		pass
	else:
		raise RuntimeError("Unknown type: %s" % type(d))

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

		self.wg = WebRequest.WebGetRobust()
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

	def validate_sdata(self, sinfo):
		# {
		#     "description": "<p>This is the tale of Noah, Pestilence in game, who starts his adventure in the newest all promising VRMMORPG: Vesper.</p>\n<p>Vesper's design is maximum freedom, a fun and everlasting adventure to keep you enthralled. Its purpose is to create a new reality where everyone can have a shot&nbsp;at the top!</p>\n<p>When he&nbsp;has no clear future ahead, he will live day by day but&nbsp;with<em> death</em>, he shall rest!</p>\n<p>-----<br><br>Hello! I'm Matt, an Italian guy with little experience in English. I got the language down by reading a lot of web novels so expect&nbsp;some grammar mistakes and spelling errors, I'm trying to&nbsp;improve my writing so every comment and correction is very welcome!</p>\n<p>This story will focus on a necromantic adventure with some out of game development, actually, there is no <span style=\"text-decoration: line-through\">skeleton</span>(pun)&nbsp; programmed development and I'm writing day by day. I'm open to suggestions both in progress and revising of content.</p>\n<p>&nbsp;</p>\n<p>&nbsp;</p>\n<p>&nbsp;</p>",
		#     "firstUpdate": 1531778821,
		#     "lastUpdate": 1534548542,
		#     "tags": "action,adventure,fantasy,litrpg,psychological,slice_of_life,magic,gore,traimatising",
		#     "id": 19442,
		#     "title": "The Grand General - MmoRpg",
		#     "cover": null,
		#     "topCover": null,
		#     "topCoverAlignment": 0
		# }

		expect = ["description", "firstUpdate", "lastUpdate", "tags", "id", "title", "cover", "topCover", "topCoverAlignment"]

		have_expected = all([tmp in sinfo for tmp in expect])

		return have_expected


	def validate_cdata(self, cinfo):
		if not isinstance(cinfo, list):
			return False

		if len(cinfo) < MIN_CHAPTERS:
			self.log.info("Too few chapters. Not adding.")
			return False

		return True

	def validate_rdata(self, soup):
		rtag = soup.find("meta", property='ratingValue')
		ctag = soup.find("meta", property='ratingCount')

		if not rtag and ctag:
			return False

		rating = float(rtag.get('content', 0))
		rcnt   = float(ctag.get('content', 0))

		if rating > MIN_RATING and rcnt > MIN_RATE_CNT:
			return True

		self.log.info("Failed validation due to low/few ratings: %s ratings, with a value of %s.", rcnt, rating)

		return False



	def extract_description(self, desc_str):

		soup = bs4.BeautifulSoup(desc_str, "html.parser")

		bad_attrs = ['style', 'font', 'size']

		for tag in soup.find_all():
			for bad_attr in bad_attrs:
				if bad_attr in tag.attrs:
					tag.attrs.pop(bad_attr)

		return soup.prettify()


	def process_series(self, series):
		expected_keys = ['chapters', 'cover', 'description', 'firstUpdate', 'id', 'lastUpdate', 'tags', 'title']
		if not all([tmp in series for tmp in expected_keys]):
			self.log.error("Missing key(s) %s from series %s. Cannot continue", [tmp for tmp in expected_keys if not tmp in series], series)
			return


		# {
		# 	'topCover': None,
		# 	'description': "<p>Gerald, born a Viscount's son, spent most of his life since he was six as an enemy Duke's 'ward', nothing short "
		#  "of a hostage. Until a shocking letter arrived requesting that he be sent back to inherit his father's territory and title.</p>\n<p>Now "
		#  "he has to return and rule the ruin that is his family's lands. Bandits roam&nbsp;and enemies leer. Conspiracies brew and wars rage. "
		#  "Meanwhile, Gerald has to rise with his house from the ashes.</p>\n<p>&nbsp;</p>\n<p>Schedule: Updates 4 times a week--&gt; Monday-"
		#  "Thursday.</p>\n<p>&nbsp;</p>\n<p>Additional tags: Kingdom Building - Strategy - War - Army Building.</p>",
		# 	'id': 19290,
		# 	'firstUpdate': datetime.datetime(2018, 7, 10, 6, 35, 48),
		# 	'topCoverAlignment': 0,
		# 	'chapters': [{'title': 'Chapter 33',
		# 	'fictionId': 19290,
		# 	'date': datetime.datetime(2018, 8, 28, 1, 55, 48),
		# 	'id': 285611}],
		# 	'cover': 'https://royalroadlupload.blob.core.windows.net/thundersurfer/rise-of-the-lord-full-AAAASg1dcgo=.jpg',
		# 	'tags': 'action,fantasy,martial_arts,male_lead,strategy,profanity,gore',
		# 	'title': 'Rise of the Lord',
		# 	'lastUpdate': datetime.datetime(2018, 8, 28, 1, 55, 48)
		#  }




		sinfo = get_json(self.wg, "https://royalroadl.com/api/fiction/info/{sid}?apikey={key}"    .format(sid=series['id'], key=settings.RRL_API_KEY))

		if not self.validate_sdata(sinfo):
			self.log.warning("Series data for sid %s failed validation" % series['id'])
			return

		cinfo = get_json(self.wg, "https://royalroadl.com/api/fiction/chapters/{sid}?apikey={key}".format(sid=series['id'], key=settings.RRL_API_KEY))
		if not self.validate_cdata(cinfo):
			return

		seriesPageUrl = "https://www.royalroad.com/fiction/{sid}/".format(sid=series['id'])
		rinfo = get_spage(self.wg, seriesPageUrl)


		# print("Series", )
		# pprint.pprint(series)
		# print("Sinfo")
		# pprint.pprint(sinfo)
		# print("Chapter")
		# pprint.pprint(cinfo)

		if not self.validate_rdata(rinfo):
			return

		author_tag = rinfo.find(property="author")
		if not author_tag and author_tag.a:
			self.log.error("Could not find author tag on url '%s'", seriesPageUrl)
			return

		if isinstance(sinfo['tags'], str):
			tags = sinfo['tags'].split(",")
		elif isinstance(sinfo['tags'], (list, tuple)):
			tags = list(sinfo['tags'])
		else:
			print("sinfo unknown type: ", sinfo['tags'])
			print("Sinfo: ", sinfo)

		# pprint.pprint(sinfo)
		# pprint.pprint(cinfo)
		# print(rinfo)

		description = self.extract_description(sinfo['description'])

		title = sinfo['title'].strip()
		author = author_tag.a.get_text(strip=True)

		seriesmeta = {}

		seriesmeta['title']       = msgpackers.fix_string(title)
		seriesmeta['author']      = msgpackers.fix_string(author)
		seriesmeta['tags']        = tags
		seriesmeta['homepage']    = seriesPageUrl
		seriesmeta['desc']        = description
		seriesmeta['tl_type']     = 'oel'
		seriesmeta['sourcesite']  = 'RoyalRoadL'
		seriesmeta['create_tags'] = True
		meta_pkt = msgpackers.createSeriesInfoPacket(seriesmeta, matchAuthor=True)

		messages = [meta_pkt]
		trigger_urls = [seriesPageUrl]

		extra = {}
		extra['tags']     = tags
		extra['homepage'] = seriesPageUrl
		extra['sourcesite']  = 'RoyalRoadL'


		for chapter in cinfo:

			reldate = chapter['date']
			chap_url = "https://www.royalroad.com/fiction/{sid}/rrl-doesnt-provide-the-series-slug/chapter/{cid}/apparently-this-needs-to-be-here-too".format(
				sid = series['id'], cid=chapter['id'])


			chp_title = chapter['title']
			# print("Chp title: '{}'".format(chp_title))
			vol, chp, frag, _ = titleParsers.extractTitle(chp_title + " " + title)

			raw_item = {}
			raw_item['srcname']   = "RoyalRoadL"
			raw_item['published'] = float(reldate)
			raw_item['linkUrl']   = chap_url

			raw_msg = msgpackers.buildReleaseMessage(raw_item, title, vol, chp, frag, author=author, postfix=chp_title, tl_type='oel', extraData=extra, matchAuthor=True)
			release_msg = msgpackers.createReleasePacket(raw_msg)

			trigger_urls.append(chap_url)
			messages.append(release_msg)

		self.amqp_put_many(messages)
		self.low_priority_links_trigger(trigger_urls)




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
		data = xmljson.parker.data(tree)

		loaded = clean_parsed_data(data['ApiFictionInfoWithChapters'])
		loaded.sort(key=lambda x: x['lastUpdate'])

		return loaded

	def load_json(self):
		loaded = json.loads(self.content)


		loaded.sort(key=lambda x: x['lastUpdate'])

		# pprint.pprint(loaded)
		content = clean_parsed_data(loaded)
		# pprint.pprint("Cleaned: ")
		# pprint.pprint(loaded)

		return content

	def processParsedData(self, loaded):
		# pprint.pprint(loaded)
		for series in loaded:
			self.process_series(series)

	def processPage(self, url, content):
		self.log.info("processPage() call: %s, %s", self.mtype, self.pageUrl)

		if self.mtype in ['text/xml', 'application/xml']:
			loaded = self.load_xml()
		elif self.mtype in ['text/json', 'application/json']:
			loaded = self.load_json()
		else:
			self.log.error("Unknown content type (%s)!", self.mtype)

		return self.processParsedData(loaded)


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

	# with open("fiction_updates.xml", "r") as fp:
	# 	content = fp.read()

	# instance = RRLJsonXmlSeriesUpdateFilter(
	# 		pageUrl   = "https://royalroadl.com/api/fiction/updates?apiKey=" + settings.RRL_API_KEY,
	# 		pgContent = content,
	# 		mimeType  = "application/xml",
	# 		db_sess   = None
	# 	)
	# print(instance)
	# extracted1 = instance.extractContent()

	# with open("json_reenc.json", "r") as fp:
	# 	content2 = fp.read()

	# instance = RRLJsonXmlSeriesUpdateFilter(pageUrl="https://royalroadl.com/api/fiction/updates?apiKey=" + settings.RRL_API_KEY, pgContent=content2, mimeType="application/json", db_sess=None)
	# print(instance)
	# extracted2 = instance.extractContent()


if __name__ == "__main__":
	test()


