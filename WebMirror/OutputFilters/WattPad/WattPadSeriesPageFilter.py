


import WebMirror.OutputFilters.FilterBase

import WebMirror.OutputFilters.util.MessageConstructors  as msgpackers
from WebMirror.OutputFilters.util.TitleParsers import extractTitle

import bs4
import re
import markdown
import time
import datetime
import calendar
import WebRequest

from settings import WATTPAD_REQUIRED_TAGS
from settings import WATTPAD_MASKED_TAGS

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

BLOCK_IDS = {

}



IS_BETA = True


class WattPadSeriesPageFilter(WebMirror.OutputFilters.FilterBase.FilterBase):


	wanted_mimetypes = [

							'text/html',
						]
	want_priority    = 50

	loggerPath = "Main.Filter.WattPad"


	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https://www.wattpad.com/story/\d+.+$", url):
			# print("WattPad Processor Wants url: '%s'" % url)
			return True
		return False

	def __init__(self, **kwargs):

		self.kwargs     = kwargs


		self.pageUrl    = kwargs['pageUrl']

		self.content    = kwargs['pgContent']
		self.type       = kwargs['type']

		self.log.info("Processing WattPad Item")
		super().__init__()

		self.wg = WebRequest.WebGetRobust(logPath=self.loggerPath+".Web")


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################


	def extractSeriesReleases(self, seriesPageUrl, metadata, soup):

		title  = metadata['title']
		author = metadata['user']['name']
		desc   = metadata['description']
		tags   = metadata['tags']

		# Apparently the description is rendered in a <pre> tag.
		# Huh?
		desc = markdown.markdown(desc, extensions=["linkify"])

		title = title.strip()

		# Siiiiiigh. Really?
		title = title.replace("[#wattys2015]", "")
		title = title.replace("(Wattys2015) ", "")
		title = title.replace("#Wattys2015", "")
		title = title.replace("Wattys2015", "")
		title = title.strip()

		if metadata['numParts'] < 3:
			return []
		if metadata['voteCount'] < 100:
			return []

		# Language ID 1 is english.
		if metadata['language']['id'] != 1:
			return []

		# Allow blocking of item by ID
		if metadata['id'] in BLOCK_IDS:
			return []

		# for some particularly stupid reasons, the item category tag is
		# not included in the metadata.
		# therefore, we parse it out from the page manually.
		tagdiv = soup.find("div", class_="tags")
		if tagdiv:
			for tag in tagdiv.find_all("a", class_='tag'):
				tags.append(tag.get_text())


		tags = list(set([item.lower().strip().replace("  ", " ").replace(" ", "-") for item in tags]))

		# Mask any content with any of the blocked tags.
		if any([item in tags for item in WATTPAD_MASKED_TAGS]):
			self.log.warning("Item has a masked tag. Not emitting any releases.")
			self.log.warning("Tags: '%s'", tags)
			return

		# And check that at least one of the target tags is present.
		if not any([item in tags for item in WATTPAD_REQUIRED_TAGS]):
			self.log.warning("Item missing required tag. Not emitting any releases.")
			self.log.warning("Tags: '%s'", tags)
			return


		seriesmeta = {}

		extra = {}
		extra['tags']        = tags[:]
		extra['homepage']    = seriesPageUrl
		extra['sourcesite']  = 'WattPad'



		retval = []
		index = 1
		valid = 1
		for release in metadata['parts']:
			chp_title = release['title']

			dt = datetime.datetime.strptime(release['modifyDate'], "%Y-%m-%dT%H:%M:%SZ" )
			reldate = calendar.timegm(dt.timetuple())

			raw_item = {}
			raw_item['srcname']   = "WattPad"
			raw_item['published'] = reldate
			raw_item['linkUrl']   = release['url']
			msg = msgpackers._buildReleaseMessage(raw_item, title, None, index, None, author=author, postfix=chp_title, tl_type='oel', extraData=extra, matchAuthor=True)
			retval.append(msg)

			# Check if there was substantive structure in the chapter
			# name. Used as a crude heuristic for chapter validity.
			# vol, chp, frag, post = extractTitle(chp_title)
			# if any((vol, chp, frag)):
			# 	# print("Valid: ", (vol, chp, frag))
			# 	valid += 1

			index += 1

		# if valid < (index/2):
		# 	print("Half the present chapters are have no numeric content?")
		# 	return []

		# Don't send the series metadata if we didn't find any chapters.
		if not retval:
			print("No chapters!")
			return []


		seriesmeta['title']       = title
		seriesmeta['author']      = author
		seriesmeta['tags']        = tags
		seriesmeta['homepage']    = seriesPageUrl
		seriesmeta['desc']        = desc
		seriesmeta['tl_type']     = 'oel'
		seriesmeta['sourcesite']  = 'WattPad'


		pkt = msgpackers.createSeriesInfoPacket(seriesmeta, beta=IS_BETA, matchAuthor=True)
		self.log.info("Wattpad scraper generated %s amqp messages!", len(retval) + 1)
		self.amqp_put_item(pkt)
		return retval




	def sendReleases(self, releases):
		self.log.info("Total releases found on page: %s", len(releases))
		for release in releases:
			pkt = msgpackers.createReleasePacket(release, beta=IS_BETA)
			self.amqp_put_item(pkt)

	def getJsonMetadata(self, soup):
		# There are a couple of tags with the data-attr "story-id"
		# Grab them all, and while we're at it, check they all match (they should)
		story_id = soup.find_all(True, {'data-story-id' : True})
		assert story_id, "No story ID tag found on page?"
		pre = story_id.pop()['data-story-id']
		for remaining in story_id:

			if not pre == remaining['data-story-id']:
				self.log.warning("Mismatched story-ids when fetching wattpad item metadata: '%s' - '%s'.", pre, remaining['data-story-id'])

		return pre


	def processPage(self, url, content):

		soup = WebRequest.as_soup(self.content)
		sid = self.getJsonMetadata(soup)

		# The GET request url is somewhat ridiculous. Build
		# it up in segments so we don't have a 500 char line
		segments = [
			"https://www.wattpad.com/api/v3/stories/{num}?include_deleted=0&".format(num=sid),
			"fields=id%2Ctitle%2CvoteCount%2CmodifyDate%2CreadCount%2CcommentCount%2Cdescription",
			"%2Curl%2Ccover%2Clanguage%2CisAdExempt%2Cuser(name%2Cusername%2Cavatar%2C"
			"description%2Clocation%2Chighlight_colour%2CbackgroundUrl%2CnumLists%2C",
			"numStoriesPublished%2CnumFollowing%2CnumFollowers%2Ctwitter)%2Ccompleted",
			"%2CnumParts%2Cparts(id%2Ctitle%2Clength%2Curl%2Cdeleted%2Cdraft%2CmodifyDate)%2Ctags%2Ccategories",
			"%2Crating%2Crankings%2Clanguage%2Ccopyright%2CsourceLink%2CfirstPartId%2Cdeleted%2Cdraft",
			]
		surl = "".join(segments)
		print(url)
		metadata = self.wg.getJson(surl, addlHeaders={'Referer': url})

		releases = self.extractSeriesReleases(self.pageUrl, metadata, soup)


		if releases:
			self.sendReleases(releases)




##################################################################################################################################
##################################################################################################################################
##################################################################################################################################



	def extractContent(self):
		# print("Call to extract!")
		# print(self.amqpint)

		self.processPage(self.pageUrl, self.content)



def test():
	print("Test mode!")
	import logSetup
	import WebMirror.rules
	import WebMirror.Engine
	import multiprocessing
	logSetup.initLogging()

	c_lok = cookie_lock = multiprocessing.Lock()
	engine = WebMirror.Engine.SiteArchiver(cookie_lock=c_lok)



	engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fiction/3021'))
	# engine.dispatchRequest(testJobFromUrl('http://www.royalroadl.com/fictions/latest-updates'))



if __name__ == "__main__":
	test()

