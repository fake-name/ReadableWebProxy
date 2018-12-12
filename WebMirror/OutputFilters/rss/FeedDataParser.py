
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



fmt_str = """
def %s(item):
	'''
	Parser for '%s'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


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

	assert nl, "Netloc for url '%s' (feed '%s') is empty!" % (feedurl, feedname)

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
		assert feedname, "Null feed names not allowed."
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


# Manual patches for dealing with a few broken feeds.
def should_ignore_feed_post(feedDat):

	# Japtem seems to put their comments in their main feed, for no good reason.
	if feedDat['srcname'] == "Japtem" and feedDat['title'].startswith("By: "):
		return True
	if feedDat['srcname'] == "Zeonic" and feedDat['title'].startswith("By: "):
		return True
	if feedDat['srcname'] == 'Sora Translations' and feedDat['title'].startswith("Comment on"):
		return True
	if feedDat['srcname'] == 'Uncommitted Translations' and ' comments on ' in feedDat['title']:
		return True
	if feedDat['srcname'] == 'Uncommitted Translations' and feedDat['title'].startswith("Comment by "):
		return True
	if '?showComment='.lower() in feedDat['linkUrl'].lower():
		return True
	if '.bravesites.com/'.lower() in feedDat['linkUrl'].lower() and 'Comment by ' in feedDat['title']:
		return True

	if any([item in feedDat['linkUrl'] for item in common.global_constants.RSS_SKIP_FILTER]):
		return True


	bad_starts = [
		('FeedProxy', 'Comment on '),
		("Krytyk's Translations", 'By: '),
		('Prince Revolution!', 'By: '),
		('Blazing Translations', 'By: '),
		('Blazing Translations', 'Comment on '),
		('Aran Translations', 'Comment on '),
	]

	if any([(feedDat['title'].startswith(bad) and feedDat['srcname'] == src) for src, bad in bad_starts]):
		return True
	return False

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


	def dispatchReleaseDbBacked(self, item):

		processor_row = self.db_sess.query(db.RssFeedEntry)       \
			.filter(db.RssFeedEntry.feed_name == item['srcname']) \
			.scalar()
		if not processor_row:
			raise RuntimeError("No feed filter system found for {} from url {}.".format(item['srcname'], item['linkUrl']))

		# Pull the function from the database
		func = processor_row.get_func()

		# And then use it.
		ret = func(item)
		return ret

	def dispatchRelease(self, item):

		ret = False


		try:
			feed = getCreateRssSource(self.db_sess, item['srcname'], item['linkUrl'])
			db_func = feed.get_func()

			ret = db_func(item)

		except Exception as e:
			print("Failure when trying to extract item for source '%s'" % item['srcname'])
			raise e


		if ret is None:
			return False


		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if ret:
			assert 'type' in ret
			assert 'data' in ret

			if ret['type'] == 'parsed-release' or ret['type'] == 'delete-release':
				reldata = ret['data']

				# Only return a value if we've actually found a chapter/vol
				if reldata and not (reldata['vol'] or reldata['chp'] or reldata['postfix']):
					self.log.info("Skipping item due to no chapter/vol/postfix: '%s', '%s', '%s', '%s', '%s', '%s', '%s'", item['srcname'], item['title'], item['tags'], vol, chp, frag, postfix)
					ret = False

				# Do not trigger if there is "preview" in the title.
				if 'preview' in item['title'].lower():
					self.log.info("Skipping item due to preview string: '%s', '%s', '%s', '%s', '%s', '%s', '%s'", item['srcname'], item['title'], item['tags'], vol, chp, frag, postfix)
					ret = False
				if reldata:
					assert 'tl_type' in reldata



		return ret


	def getProcessedReleaseInfo(self, feedDat):

		if any([item in feedDat['linkUrl'] for item in common.global_constants.RSS_SKIP_FILTER]):
			print("Skipping!")
			return


		release = self.dispatchRelease(feedDat)

		if release:
			return json.dumps(release)
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


	def processFeedData(self, session, feedDat, tx_raw=True, tx_parse=True):


		if any([item in feedDat['linkUrl'] for item in common.global_constants.RSS_SKIP_FILTER]):
			print("LinkURL '%s' contains a filtered string. Not fetching!" % feedDat['linkUrl'])
			return

		if any([feedDat['title'].lower().startswith(item) for item in common.global_constants.RSS_TITLE_FILTER]):
			print("LinkURL '%s' contains a filtered string. Not fetching!" % feedDat['linkUrl'])
			return


		# print("Feed item title: ", feedDat['title'], feedDat)

		if feedDat['title'].lower().startswith("by: "):
			self.log.warning("Skipping due to title: '%s'", feedDat['title'])
			return


		netloc = urllib.parse.urlparse(feedDat['linkUrl']).netloc

		nicename = feedNameLut.getNiceName(session, feedDat['linkUrl'])
		if not nicename:
			nicename = netloc
		feedDat['srcname'] = nicename

		if should_ignore_feed_post(feedDat):
			self.log.warning("Skipping due to should_ignore_feed_post")
			return

		# print("ProcessFeedData! ", netloc)

		# A bunch of crap is aggregated through the "feedproxy.google.com" netloc.
		if "feedproxy.google.com" in netloc:
			print("Not sending data for feedproxy netloc: ", netloc)
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
				self.log.info("Sending parsed release!")
				self.amqp_put_item(new)

		# A bunch of crap is aggregated through the "feedproxy.google.com" netloc.
		if not WebMirror.rules.netloc_send_feed(netloc):
			print("Not sending raw feed for netloc due to rules: ", netloc)
			return

		raw = self.getRawFeedMessage(feedDat)
		if tx_raw:
			if raw:
				self.amqp_put_item(raw)

