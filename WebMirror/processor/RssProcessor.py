


import runStatus
runStatus.preloadDicts = False

from . import ProcessorBase


import feedparser
import json
import calendar
import WebMirror.OutputFilters.rss.FeedDataParser

# import TextScrape.RelinkLookup
# import TextScrape.RELINKABLE as RELINKABLE



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




class RssProcessor(ProcessorBase.PageProcessor, WebMirror.OutputFilters.rss.FeedDataParser.DataParser):


	wanted_mimetypes = [
							'application/atom+xml',
							'application/rdf+xml',
							'application/rss+xml',
							'application/xml',
							'text/xml',
						]
	want_priority    = 50

	loggerPath = "Main.Text.RssProcessor"


	@staticmethod
	def wantsFromContent(content):
		try:
			# Check if the feed has a version
			feed = feedparser.parse(content)
			return bool(feed['version'])
		except Exception:
			return False

	def __init__(self, pageUrl, loggerPath, pgContent, type, **kwargs):
		self.loggerPath = loggerPath+".RssProcessor"
		self.pageUrl    = pageUrl

		self.content    = pgContent
		self.type       = type

		self.log.info("Processing RSS Item")
		super().__init__()


	# @profile
	def parseFeed(self, rawFeed):
		return feedparser.parse(rawFeed)


	# Methods to allow the child-class to modify the content at various points.
	def extractMarkdownTitle(self, content, url):
		# Take the first non-empty line, and just assume it's the title. It'll be close enough.

		prefix = None
		for urlText, prepend in self.urlLut.items():
			if urlText in url:
				prefix = prepend

		title = content.strip().split("\n")[0].strip()

		if prefix:
			title = "{prefix} - {title}".format(prefix=prefix, title=title)

		return title


	def extractContent(self):


		feed = self.parseFeed(self.content)
		data = self.processFeed(feed, self.pageUrl)


		# self.insertFeed(tableName, tableKey, pluginName, feedUrl, data, badwords)


		# title = self.extractMarkdownTitle(self.content, self.pageUrl)
		# procContent = markdown.markdown(self.content)

		# self.log.info("Processed title: '%s'", title)

		ret = {}
		# No links here
		ret['plainLinks'] = []
		ret['rsrcLinks']  = []
		ret['title']      = []
		ret['contents']   = []

		return ret



	def processFeed(self, feed, feedUrl):


		meta = feed['feed']
		entries = feed['entries']

		ret = []

		for entry in entries:
			item = {}

			item['title'] = entry['title']
			item['guid'] = entry['guid']

			item['tags'] = []
			if 'tags' in entry:
				for tag in entry['tags']:
					item['tags'].append(tag['term'])


			item['linkUrl'] = entry['link']


			if 'content' in entry:
				item['contents'] = entry['content']
			elif 'summary' in entry:
				item['contents'] = entry['summary']
			else:
				self.log.error('Empty item in feed?')
				self.log.error('Feed url: %s', feedUrl)
				continue

			item['authors'] = entry['authors']
			# guid
			# contents
			# contentHash
			# author
			# linkUrl
			# tags


			if 'updated_parsed' in entry:
				item['updated'] = calendar.timegm(entry['updated_parsed'])

			if 'published_parsed' in entry:
				item['published'] = calendar.timegm(entry['published_parsed'])

			if not 'published' in item or ('updated' in item and item['published'] > item['updated']):
				item['published'] = item['updated']
			if not 'updated' in item:
				item['updated'] = -1

			item['feedtype'] = self.type


			self.processFeedData(item)

			item['tags'] = json.dumps(item['tags'])

			ret.append(item)
		return ret

	def insertFeed(self, tableName, tableKey, pluginName, feedUrl, feedContent, badwords):
		print("InsertFeed!")
		dbFunc = TextScrape.utilities.Proxy.EmptyProxy(tableKey=tableKey, tableName=tableName, scanned=[feedUrl])

		for item in feedContent:
			if item['title'].startswith('User:') and tableKey == 'tsuki':
				# The tsuki feed includes changes to user pages. Fuck that noise. Ignore that shit.
				continue

			try:
				ret = self.extractContents(feedUrl, item['contents'])
				# print(ret)
				# ret = dbFunc.processHtmlPage(feedUrl, item['contents'])
			except RuntimeError:
				ret = {}
				ret['contents'] = '<H2>WARNING - Failure when cleaning and extracting content!</H2><br><br>'
				ret['contents'] += item['contents']
				ret['rsrcLinks'] = []
				ret['plainLinks'] = []
				self.log.error("Wat? Error when extracting contents!")



			if not self.itemInDB(contentid=item['guid']):

				self.log.info("New article in feed!")


				row = {
					'srcname'    : tableKey,
					'feedurl'    : feedUrl,
					'contenturl' : item['linkUrl'],
					'contentid'  : item['guid'],
					'title'      : item['title'],
					'contents'   : ret['contents'],
					'author'     : '',
					'tags'       : item['tags'],
					'updated'    : item['updated'],
					'published'  : item['published'],
				}

				self.insertIntoDb(**row)

			dbFunc.upsert(item['linkUrl'], dlstate=0, distance=0, walkLimit=1)
			for link in ret['plainLinks']:
				# print("Adding link '%s' to the queue" % link)
				if not any([badword in link for badword in badwords]):
					dbFunc.upsert(link, dlstate=0, distance=0, walkLimit=1)
				else:
					print("Filtered link!", link)
			for link in ret['rsrcLinks']:
				if not any([badword in link for badword in badwords]):
					dbFunc.upsert(link, distance=0, walkLimit=1, istext=False)




def test():
	print("Test mode!")
	import logSetup
	import WebMirror.rules
	import WebMirror.Fetch
	logSetup.initLogging()

	loaded_rules = WebMirror.rules.load_rules()
	for ruleset in loaded_rules:
		print(ruleset.keys())
		print(ruleset['type'])
		print(ruleset['feedurls'])

	url = 'http://taulsn.wordpress.com/feed/'
	fetcher = WebMirror.Fetch.ItemFetcher(WebMirror.rules.load_rules(), url, url)
	response = fetcher.fetch()


	url = 'http://turb0translation.blogspot.com/feeds/posts/default'
	fetcher = WebMirror.Fetch.ItemFetcher(WebMirror.rules.load_rules(), url, url)
	response = fetcher.fetch()


	url = 'http://www.w3schools.com/xml/note.xml'
	fetcher = WebMirror.Fetch.ItemFetcher(WebMirror.rules.load_rules(), url, url)
	response = fetcher.fetch()


if __name__ == "__main__":
	test()

