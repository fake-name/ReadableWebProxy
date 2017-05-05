
#!/usr/bin/python
# from profilehooks import profile
import urllib.parse
import json
import traceback
import datetime
import WebMirror.OutputFilters.util.feedNameLut as feedNameLut


from WebMirror.OutputFilters.util.TitleParsers import extractVolChapterFragmentPostfix

import WebMirror.OutputFilters.FilterBase
import WebMirror.rules
import flags
import common.global_constants

from common import database as db


from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy import or_
from sqlalchemy.sql import func
from sqlalchemy.orm import outerjoin
import sqlalchemy.exc
import sqlalchemy.orm.exc
from sqlalchemy_continuum.utils import version_table



fmt_str = """
def %s(item):
	'''
	Parser for '%s'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False
	"""

def fname_sanitize(ins):

	# Largely empircally determined
	bad = r":'✱|…。()-:%.'\"!,★♥~?:&、<>"
	for badc in bad:
		ins = ins.replace(badc, "")

	while " " in ins:
		ins = ins.replace(" ", "")
	return ins


def create_function_for_name(name):
	fkey = name.title().strip()

	fName = "extract{}".format(fname_sanitize(fkey))

	assert fName.isidentifier(), "'%s' is not a valid identifier (Base:'%s')" % (fName, name)

	func = fmt_str % (fName, name)
	return func


def getCreateRssSource(db_sess, feedname, feedurl):
	nl = urllib.parse.urlsplit(feedurl).netloc

	if feedname is None:
		feedname = nl

	# We want to always add the netloc if it's missing, but only create the row if needed.

	nl_only = db_sess.query(db.RssFeedUrlMapper) \
		.filter(db.RssFeedUrlMapper.feed_netloc == nl) \
		.all()

	if len(nl_only) == 1:
		ret = nl_only[0].feed_entry
		if not ret.func:
			ret.func = create_function_for_name(feedname)
			db_sess.commit()
		return ret
	elif len(nl_only) > 1:
		raise RuntimeError("Too many entries for feed netloc?")


	feed_row = db_sess.query(db.RssFeedEntry) \
		.filter(db.RssFeedEntry.feed_name == feedname) \
		.scalar()

	if not feed_row:
		feed_row = db.RssFeedEntry(
				version   = 1,
				feed_name = feedname,
				enabled   = False,
				func      = create_function_for_name(feedname),
				last_changed = datetime.datetime.now(),
			)
		db_sess.add(feed_row)
		db_sess.flush()
	feed_id = feed_row.id


	new_nl = db.RssFeedUrlMapper(
			feed_netloc = nl,
			feed_url    = feedurl,
			feed_id     = feed_id,
		)
	db_sess.add(new_nl)

	if not feed_row.func:
		feed_row.func = create_function_for_name(feedname)

	db_sess.commit()

	return feed_row



class DataParser(WebMirror.OutputFilters.FilterBase.FilterBase):

	amqpint = None
	amqp_connect = True

	def __init__(self, transfer=True, debug_print=False, write_debug=False, **kwargs):
		super().__init__(**kwargs)

		self.dbg_print = debug_print
		self.transfer = transfer
		self.names = set()

		self.write_debug = write_debug

	####################################################################################################################################################
	####################################################################################################################################################
	##
	##  Dispatcher
	##
	####################################################################################################################################################
	####################################################################################################################################################

	def getFunctionFromDb(self, srcname):
		self.db_sess


	def dispatchReleaseDbBacked(self, item):
		processor_row = self.db_sess.query(db.RssFeedEntry)       \
			.filter(db.RssFeedEntry.feed_name == item['srcname']) \
			.scalar()
		if not processor_row:
			raise RuntimeError("No feed filter system found for {} from url {}.".format(item['srcname'], item['linkUrl']))

		# Pull the function from the database
		func = processor_row.get_func()

		# And then use it.
		return(func(item))

	def dispatchRelease(self, item):

		ret = False


		try:
			feed = getCreateRssSource(self.db_sess, item['srcname'], item['linkUrl'])
			db_func = feed.get_func()

			ret = db_func(item)

		except Exception as e:
			print("Failure when trying to extract item for source '%s'" % item['srcname'])
			raise e

		# NanoDesu is annoying and makes their releases basically impossible to parse. FFFUUUUUu
		if "(NanoDesu)" in item['srcname'] and not ret:
			return False

		if ret is None:
			return False

		bad_starts = [
			('FeedProxy', 'Comment on '),
			("Krytyk's Translations", 'By: '),
			('Prince Revolution!', 'By: '),
			('Blazing Translations', 'By: '),
			('Blazing Translations', 'Comment on '),
			('Aran Translations', 'Comment on '),

		]

		if (
				(flags.RSS_DEBUG or self.dbg_print)   and
				self.write_debug                      and
				ret is False                          and
				not "teaser" in item['title'].lower() and
				not "Preview" in item['tags']
			):
			vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
			if vol or chp or frag and not flags.RSS_DEBUG:

				if not any([(item['title'].startswith(bad) and item['srcname'] == src) for src, bad in bad_starts]):
					with open('rss_filter_misses-1.json', "a") as fp:

						write_items = {
							"SourceName" : item['srcname'],
							"Title"      : item['title'],
							"Tags"       : list(item['tags']),
							"Vol"        : False if not vol else vol,
							"Chp"        : False if not chp else chp,
							"Frag"       : False if not frag else frag,
							"Postfix"    : postfix,
							"Feed URL"   : item['linkUrl'],
							"GUID"       : item['guid'],
						}


						fp.write("%s" % (json.dumps(write_items, )))
						fp.write("\n")

		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if self.dbg_print or flags.RSS_DEBUG:
			# False means not caught. None means intentionally ignored.

			if (
					ret is False         and
					(vol or chp or frag) and
					not "teaser" in item['title'].lower()
				):
				print("Missed:")
				print("	Source: '%s'" % (item['srcname'], ))
				print("	Title:  '%s'" % (item['title'], ))
				print("	Tags:   '%s'" % (item['tags'], ))
				print("	Vol %s, chp %s, fragment %s, postfix '%s'" % (vol, chp, frag, postfix))
				# print("Missed: '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (item['srcname'], item['title'], item['tags'], vol, chp, frag, postfix))
			elif ret:
				pass
				# print("OK! '%s', V:'%s', C:'%s', '%s', '%s', '%s'" % (ret['srcname'], ret['vol'], ret['chp'], ret['postfix'], ret['series'], item['title']))
			else:
				pass
				# print("Wat: '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (item['srcname'], item['title'], item['tags'], vol, chp, frag, postfix, item['linkUrl']))

			if flags.RSS_DEBUG:
				ret = False

		# Only return a value if we've actually found a chapter/vol
		if ret and not (ret['vol'] or ret['chp'] or ret['postfix']):
			self.log.info("Skipping item due to no chapter/vol/postfix: '%s', '%s', '%s', '%s', '%s', '%s', '%s'", item['srcname'], item['title'], item['tags'], vol, chp, frag, postfix)
			ret = False

		# Do not trigger if there is "preview" in the title.
		if 'preview' in item['title'].lower():
			self.log.info("Skipping item due to preview string: '%s', '%s', '%s', '%s', '%s', '%s', '%s'", item['srcname'], item['title'], item['tags'], vol, chp, frag, postfix)
			ret = False
		if ret:
			assert 'tl_type' in ret



		return ret


	def getProcessedReleaseInfo(self, feedDat):

		if any([item in feedDat['linkUrl'] for item in common.global_constants.RSS_SKIP_FILTER]):
			print("Skipping!")
			return


		release = self.dispatchRelease(feedDat)

		if release:
			ret = {
				'type' : 'parsed-release',
				'data' : release
			}
			return json.dumps(ret)
		return False


	def getRawFeedMessage(self, feedDat):

		feedDat = feedDat.copy()

		# remove the contents item, since it can be
		# quite large, and is not used.
		feedDat.pop('contents')
		ret = {
			'type' : 'raw-feed',
			'data' : feedDat
		}
		try:
			return json.dumps(ret)
		except TypeError:
			return None

	# Manual patches for dealing with a few broken feeds.
	def checkIgnore(self, feedDat):

		# Japtem seems to put their comments in their main feed, for no good reason.
		if feedDat['srcname'] == "Japtem" and feedDat['title'].startswith("By: "):
			return True
		if feedDat['srcname'] == "Zeonic" and feedDat['title'].startswith("By: "):
			return True
		if feedDat['srcname'] == 'Sora Translations' and feedDat['title'].startswith("Comment on"):
			return True


		return False

	def processFeedData(self, session, feedDat, tx_raw=True, tx_parse=True):

		if any([item in feedDat['linkUrl'] for item in common.global_constants.RSS_SKIP_FILTER]):
			# print("LinkURL '%s' contains a filtered string. Not fetching!" % feedDat['linkUrl'])
			return

		if any([feedDat['title'].lower().startswith(item) for item in common.global_constants.RSS_TITLE_FILTER]):
			# print("LinkURL '%s' contains a filtered string. Not fetching!" % feedDat['linkUrl'])
			return


		# print("Feed item title: ", feedDat['title'], feedDat)

		if feedDat['title'].lower().startswith("by: "):
			return


		netloc = urllib.parse.urlparse(feedDat['linkUrl']).netloc

		nicename = feedNameLut.getNiceName(session, feedDat['linkUrl'])
		if not nicename:
			nicename = netloc
		feedDat['srcname'] = nicename

		if self.checkIgnore(feedDat):
			return

		# print("ProcessFeedData! ", netloc)

		# A bunch of crap is aggregated through the "feedproxy.google.com" netloc.
		if not WebMirror.rules.netloc_send_feed(netloc) and not "feedproxy.google.com" in netloc:
			print("Not sending data for netloc: ", netloc)
			return

		try:
			new = self.getProcessedReleaseInfo(feedDat)
		except AssertionError:
			self.log.error("Exception when processing release!")
			for line in traceback.format_exc().split("\n"):
				self.log.error(line.rstrip())

			return

		if tx_parse:
			if new:
				self.amqp_put_item(new)


		raw = self.getRawFeedMessage(feedDat)
		if tx_raw:
			if raw:
				self.amqp_put_item(raw)

