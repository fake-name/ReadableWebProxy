
import time
import urllib.parse
import pprint
import datetime
import traceback
import os.path
import json
import random
import uuid

import calendar

import sqlalchemy.exc
from sqlalchemy.orm import joinedload
from sqlalchemy import desc
from sqlalchemy import func



import common.database as db

import common.get_rpyc
import common.util.rpc_base as rpc_base
import common.StatsdMixin as StatsdMixin
from common.util.remote_base import RpcBaseClass

from WebMirror.JobUtils import buildjob
import WebMirror.TimedTriggers.TriggerBase
import WebMirror.OutputFilters.util.feedNameLut as feedNameLut
from WebMirror.OutputFilters.util.MessageConstructors import fix_string
from WebMirror.OutputFilters.util.MessageConstructors import createReleasePacket
from WebMirror.OutputFilters.util.TitleParsers import extractVolChapterFragmentPostfix

BAD_RESOLVES = [
	'doubleclick.net',
	'm.wuxiaworld.com',  # Fucking mobile sites
	'www.webnovel.com/sw.js',
	'novelsnao.com/?reqp=1&reqr=',
	'data:application/javascript',
	'offer.alibaba.com',
	'about:blank',
	'://localhost/',
]
GONE_RESOLVES = [
	'www1.trungtnguyen123.org',
	'www1.faktranslations.com',
	'faktranslations.com',
]

MAX_TOTAL_FETCH_ATTEMPTS = 7


# Remove blogspot garbage subdomains from the TLD (if present)
def urls_the_same(url_list):
	fixed_urls = []
	for url in url_list:
		p = urllib.parse.urlparse(url)
		f = (p[0], p[1].split(".blogspot.")[0], p[2], p[3], p[4])
		fixed = urllib.parse.urlunsplit(f)

		# Feedburner is a bunch of fucktards, and really REALLY want to know
		# who you are and where you came from. Fuck that.
		fixed = fixed.split('?utm_source=feedburner')[0]
		fixed = fixed.split('#utm_source=feedburner')[0]

		# Ignore http/https differences
		fixed = fixed.replace("http://", 'https://')

		# And missing www.
		fixed = fixed.replace("://www.", '://')

		if fixed.endswith("?m=1"):
			fixed = fixed[:-len("?m=1")]

		fixed_urls.append(fixed)

	# pprint.pprint(fixed_urls)

	return all([fixed_urls[0] == tmp for tmp in fixed_urls])

def load_lut():
	outf = os.path.join(os.path.split(__file__)[0], 'name_fix_lut.json')
	jctnt = open(outf).read()
	lut = json.loads(jctnt)
	return lut

class NuHeader(WebMirror.TimedTriggers.TriggerBase.TriggerBaseClass, StatsdMixin.StatsdMixin, rpc_base.RpcMixin):
	'''
		NU Updates are batched and only forwarded to the output periodically,
		to make timing attacks somewhat more difficult.
		It's still possible to look at execution edge-times, albeit somewhat
		smeared out by the multiple intercontinental message queues, but if that
		becomes an issue, it'll be simple enough to introduce fuzzy delays.

		Also, hurrah, I got my distributed RPC system going again, so that's nice.

		Example JSON response from distributed worker:
			{
			    "nu_release": {
			        "actual_target": "http://shiroyukitranslations.com/the-strongest-dan-god-chapter-63-dominating-business-channels/",
			        "seriesname": "The Strongest Dan God",
			        "outbound_wrapper": "http://www.novelupdates.com/extnu/134595/",
			        "groupinfo": "Shiroyukineko Translations",
			        "releaseinfo": "c63",
			        "addtime": "2016-05-30T04:16:41.351430",
			        "referrer": "https://www.novelupdates.com"
			    }
			}
	'''

	pluginName = "Nu Header"
	pluginName = "NuRpcGet"


	loggerPath = "Main.Header.Nu"
	statsd_prefix = 'ReadableWebProxy.Nu.Header'

	go = None

	def __init__(self, connect=True):
		super().__init__()

		self.name_lut, self.group_lut = load_lut()

		if connect:
			self.check_open_rpc_interface()


	def put_head_jobs(self, put=3):
		with db.session_context() as db_sess:
			self.log.info("Loading rows to fetch..")
			recent_d_1 = datetime.datetime.now() - datetime.timedelta(hours=72)
			recentq = db_sess.query(db.NuReleaseItem)                     \
				.outerjoin(db.NuResolvedOutbound)                         \
				.filter(db.NuReleaseItem.validated == False)              \
				.filter(db.NuReleaseItem.release_date >= recent_d_1)        \
				.options(joinedload('resolved'))                          \
				.order_by(desc(db.NuReleaseItem.first_seen))              \
				.group_by(db.NuReleaseItem.id)                            \
				.limit(max(100, put*10))


			recent_d_2 = datetime.datetime.now() - datetime.timedelta(hours=24*14)
			bulkq = db_sess.query(db.NuReleaseItem)                       \
				.outerjoin(db.NuResolvedOutbound)                         \
				.filter(db.NuReleaseItem.validated == False)              \
				.filter(db.NuReleaseItem.release_date >= recent_d_2)        \
				.options(joinedload('resolved'))                          \
				.order_by(desc(db.NuReleaseItem.first_seen))              \
				.group_by(db.NuReleaseItem.id)                            \
				.limit(max(100, put*6))

			bulkset   = bulkq.all()
			recentset = recentq.all()

			self.log.info("Have %s recent items, %s long-term items to fetch", len(recentset), len(bulkset))
			haveset   = bulkset + recentset
			filtered = {tmp.id : tmp for tmp in haveset}
			haveset = list(filtered.values())
			self.log.info("Total items after filtering for uniqueness %s", len(haveset))

			if not haveset:
				self.log.info("No jobs to remote HEAD.")
				return

			# We pick a large number of items, and randomly choose one of them.
			# This lets us weight the fetch preferentially to the recent items, but still
			# have some variability.
			# We prefer to fetch items that'll resolve as fast as possible.
			preferred_2 = [tmp for tmp in haveset if len(tmp.resolved) == 2]
			preferred_1 = [tmp for tmp in haveset if len(tmp.resolved) == 1]
			fallback    = [tmp for tmp in haveset if len(tmp.resolved) == 0]


			haveset = random.sample(preferred_2, min(put, len(preferred_2)))
			if len(haveset) < put:
				haveset.extend(random.sample(preferred_1, min(put-len(haveset), len(preferred_1))))
			if len(haveset) < put:
				haveset.extend(random.sample(fallback, min(put-len(haveset), len(fallback))))

			put = 0
			active = set()

			for have in haveset:
				if len(list(have.resolved)) >= 3:
					raise RuntimeError("Overresolved item that's not valid.")

				if (have.referrer == "http://www.novelupdates.com" or
					have.referrer == "https://www.novelupdates.com" or
					have.referrer == "https://www.novelupdates.com/" or
					have.referrer == "http://www.novelupdates.com/"):
					self.log.error("Wat?")
					self.log.error("Bad Referrer URL got into the input queue!")
					self.log.error("Id: %s, ref: %s", have.id, have.referrer)
					for bad_resolve in have.resolved:
						db_sess.delete(bad_resolve)
					db_sess.delete(have)
					db_sess.commit()
					continue

				if have.fetch_attempts > MAX_TOTAL_FETCH_ATTEMPTS:
					self.log.error("Wat?")
					self.log.error("Item fetched too many times!")
					self.log.error("Id: %s", have.id)
					self.log.error("Attempted more then %s resolves. Disabling.", MAX_TOTAL_FETCH_ATTEMPTS)
					have.reviewed = 'rejected'
					have.validated = True
					db_sess.commit()
					continue

				if have.outbound_wrapper in active:
					continue
				active.add(have.outbound_wrapper)

				have.fetch_attempts += 1
				db_sess.commit()

				self.log.info("Putting job for url '%s', with %s resolves so far", have.outbound_wrapper, len(have.resolved))
				self.log.info("Referring page '%s'", have.referrer)


				raw_job = buildjob(
					module         = 'SmartWebRequest',
					call           = 'getHeadTitleChromium',
					dispatchKey    = "fetcher",
					jobid          = -1,
					args           = [],
					kwargs         = {
						"url"           : have.outbound_wrapper,
						"referrer"      : have.referrer,
						"title_timeout" : 30,
					},
					additionalData = {
						'mode'        : 'fetch',
						'wrapper_url' : have.outbound_wrapper,
						'referrer'    : have.referrer
						},
					postDelay      = 0,
					unique_id      = have.outbound_wrapper,
					serialize      = 'Nu-Header',
				)

				self.rpc.put_job(raw_job)
				put += 1

		return put



	def get_rpc_head_lists(self, chunks=7, chunklength=15, chunkdupes=2):
		put = chunks * chunklength

		with db.session_context() as db_sess:
			self.log.info("Loading rows to fetch..")
			recent_d_1 = datetime.datetime.now() - datetime.timedelta(hours=72)
			recentq = db_sess.query(db.NuReleaseItem)                     \
				.outerjoin(db.NuResolvedOutbound)                         \
				.filter(db.NuReleaseItem.validated == False)              \
				.filter(db.NuReleaseItem.release_date >= recent_d_1)        \
				.options(joinedload('resolved'))                          \
				.order_by(desc(db.NuReleaseItem.first_seen))              \
				.group_by(db.NuReleaseItem.id)                            \
				.limit(max(100, put*10))


			recent_d_2 = datetime.datetime.now() - datetime.timedelta(hours=24*14)
			bulkq = db_sess.query(db.NuReleaseItem)                       \
				.outerjoin(db.NuResolvedOutbound)                         \
				.filter(db.NuReleaseItem.validated == False)              \
				.filter(db.NuReleaseItem.release_date >= recent_d_2)        \
				.options(joinedload('resolved'))                          \
				.order_by(desc(db.NuReleaseItem.first_seen))              \
				.group_by(db.NuReleaseItem.id)                            \
				.limit(max(100, put*6))

			bulkset   = bulkq.all()
			recentset = recentq.all()

			self.log.info("Have %s recent items, %s long-term items to fetch", len(recentset), len(bulkset))
			haveset   = bulkset + recentset
			filtered = {tmp.id : tmp for tmp in haveset}
			haveset = list(filtered.values())
			self.log.info("Total items after filtering for uniqueness %s", len(haveset))

			if not haveset:
				self.log.info("No jobs to remote HEAD.")
				return

			# We pick a large number of items, and randomly choose one of them.
			# This lets us weight the fetch preferentially to the recent items, but still
			# have some variability.
			# We prefer to fetch items that'll resolve as fast as possible.
			preferred_2 = [tmp for tmp in haveset if len(tmp.resolved) == 2]
			preferred_1 = [tmp for tmp in haveset if len(tmp.resolved) == 1]
			fallback    = [tmp for tmp in haveset if len(tmp.resolved) == 0]


			haveset = random.sample(preferred_2, min(put, len(preferred_2)))
			if len(haveset) < put:
				haveset.extend(random.sample(preferred_1, min(put-len(haveset), len(preferred_1))))
			if len(haveset) < put:
				haveset.extend(random.sample(fallback, min(put-len(haveset), len(fallback))))

			put = 0
			active = set()
			chunks = []

			chunk = ()
			for have in haveset:

				if len(list(have.resolved)) >= 3:
					raise RuntimeError("Overresolved item that's not valid.")

				if (have.referrer == "http://www.novelupdates.com" or
					have.referrer == "https://www.novelupdates.com" or
					have.referrer == "https://www.novelupdates.com/" or
					have.referrer == "http://www.novelupdates.com/"):
					self.log.error("Wat?")
					self.log.error("Bad Referrer URL got into the input queue!")
					self.log.error("Id: %s, ref: %s", have.id, have.referrer)
					for bad_resolve in have.resolved:
						db_sess.delete(bad_resolve)
					db_sess.delete(have)
					db_sess.commit()
					continue

				if have.fetch_attempts > MAX_TOTAL_FETCH_ATTEMPTS:
					self.log.error("Wat?")
					self.log.error("Item fetched too many times!")
					self.log.error("Id: %s", have.id)
					self.log.error("Attempted more then %s resolves. Disabling.", MAX_TOTAL_FETCH_ATTEMPTS)
					have.reviewed = 'rejected'
					have.validated = True
					db_sess.commit()
					continue

				if have.outbound_wrapper in active:
					self.log.warning("Duplicates for outbound '%s' -> '%s'", have.outbound_wrapper, have.referrer)
					continue

				active.add(have.outbound_wrapper)

				have.fetch_attempts += chunkdupes
				db_sess.commit()

				self.log.info("Putting job for url '%s', with %s resolves so far", have.outbound_wrapper, len(have.resolved))
				self.log.info("Referring page '%s'", have.referrer)

				chunk = chunk + ({'wrapper' : have.outbound_wrapper, 'referrer' : have.referrer}, )
				if len(chunk) > chunklength:
					for _ in range(chunkdupes):
						chunks.append(chunk)
					chunk = ()


			# 	raw_job = buildjob(
			# 		module         = 'SmartWebRequest',
			# 		call           = 'getHeadTitleChromium',
			# 		dispatchKey    = "fetcher",
			# 		jobid          = -1,
			# 		args           = [],
			# 		kwargs         = {
			# 			"url"           : have.outbound_wrapper,
			# 			"referrer"      : have.referrer,
			# 			"title_timeout" : 30,
			# 		},
			# 		additionalData = {
			# 			'mode'        : 'fetch',
			# 			'wrapper_url' : have.outbound_wrapper,
			# 			'referrer'    : have.referrer
			# 			},
			# 		postDelay      = 0,
			# 		unique_id      = have.outbound_wrapper,
			# 		serialize      = 'Nu-Header',
			# 	)

			# 	self.rpc.put_job(raw_job)
			# 	put += 1
		if chunk:
			for _ in range(chunkdupes):
				chunks.append(chunk)
		self.log.info("Attempting to fetch %s url chunks!")
		return chunks


	def process_avail(self):
		received = 0
		while self.process_single_avail():
			received += 1
			self.log.info("Processing response!")
		return received

	def check_open_rpc_interface(self):
		try:
			if self.rpc.check_ok():
				return

		except Exception:
			try:
				self.rpc.close()
			except Exception:
				pass
			self.rpc = common.get_rpyc.RemoteJobInterface("NuHeader")

	def process_single_source_target_mapping(
				self,
				from_outbound_wrapper,
				from_outbound_referrer,
				to_url,
				to_url_title,
				client_id,
				client_key
			):

		if to_url.endswith("?m=1"):
			to_url = to_url[:-len("?m=1")]
		if "?utm_source=" in to_url:
			to_url = to_url.split("?utm_source=")[0]



		self.log.info("Processing remote head response: %s", (from_outbound_wrapper, from_outbound_referrer))
		self.log.info("Resolved job to URL: %s", to_url)
		self.log.info("Page title: %s", to_url_title)

		# Handle the 301/2 not resolving properly.
		netloc = urllib.parse.urlsplit(to_url).netloc
		if "novelupdates" in netloc:
			self.log.warning("Failed to validate external URL. Either scraper is blocked, or phantomjs is failing.")
			return True

		if 'm.wuxiaworld.com' in to_url:
			to_url = to_url.replace('m.wuxiaworld.com', 'www.wuxiaworld.com')
		if 'tseirptranslations.blogspot.com' in to_url:
			to_url = to_url.replace('tseirptranslations.blogspot.com', 'tseirptranslations.com')
		if 'm.xianxiaworld.net' in to_url:
			to_url = to_url.replace('m.xianxiaworld.net', 'www.xianxiaworld.net')
		if 'shikkakutranslations.wordpress.com' in to_url:
			to_url = to_url.replace('shikkakutranslations.wordpress.com', 'shikkakutranslations.com')

		if any([tmp in to_url for tmp in BAD_RESOLVES]):
			self.log.warning("Bad resolve in url: '%s'. Not inserting into DB.", to_url)
			return True

		if not to_url.lower().startswith("http"):
			self.log.warning("URL '%s' does not start with 'http'. Not inserting into DB.", to_url)
			return True

		if '/?utm_source=feedburner' in to_url:
			to_url = to_url.split('/?utm_source=feedburner')[0] + "/"

		while True:
			with db.session_context() as db_sess:
				try:
					self.log.info("Trying for upsert")
					have = db_sess.query(db.NuReleaseItem)                                   \
						.options(joinedload('resolved'))                                     \
						.filter(db.NuReleaseItem.outbound_wrapper == from_outbound_wrapper)  \
						.filter(db.NuReleaseItem.referrer         == from_outbound_referrer) \
						.scalar()

					if not have:
						self.log.error("Base row deleted from resolve?")
						return

					if to_url_title.strip().lower() == to_url.strip().lower():
						self.log.warning("Item didn't resolve to a name properly!")
						return

					new = db.NuResolvedOutbound(
							client_id      = client_id,
							client_key     = client_key,
							actual_target  = to_url,
							resolved_title = to_url_title,
							fetched_on     = datetime.datetime.now(),
						)

					have.resolved.append(new)
					db_sess.commit()
					return False

				except sqlalchemy.exc.InvalidRequestError as e:
					self.log.error("Exception: %s!", e)

					db_sess.rollback()
				except sqlalchemy.exc.OperationalError as e:
					self.log.error("Exception: %s!", e)

					db_sess.rollback()
				except sqlalchemy.exc.IntegrityError as e:
					self.log.error("Exception: %s!", e)
					db_sess.rollback()
					return False


				except Exception:
					self.mon_con.incr('head-failed', 1)
					self.log.error("Error when processing job response!")
					for line in traceback.format_exc().split("\n"):
						self.log.error(line)

					self.log.error("Contents of head response:")

					for line in pprint.pformat(new).split("\n"):
						self.log.error(line)
					return True

		return False



	def process_single_avail(self):
		'''
		Example response:

		{
			'call': 'getHeadTitleChromium',
			'cancontinue': True,
			'dispatch_key': 'fetcher',
			'extradat': {'mode': 'fetch'},
			'jobid': -1,
			'jobmeta': {'sort_key': 'a269f164a16e11e6891500163ef6fe07'},
			'module': 'SmartWebRequest',
			'ret': 'http://lightnovels.world/the-nine-godheads/nine-godheads-chapter-74/',
			'success': True,
			'user': 'scrape-worker-2',
			'user_uuid': 'urn:uuid:0a243518-834f-46d8-b34c-7f2afd20d37f'
		 }

		'''
		self.check_open_rpc_interface()

		while 1:
			try:
				new = self.rpc.get_job()
				break
			except TypeError:
				self.check_open_rpc_interface()
			except KeyError:
				self.check_open_rpc_interface()


		if new is None:
			self.log.info("No NU Head responses!")
			return False

		expected_keys = ['call', 'cancontinue', 'dispatch_key', 'extradat', 'jobid',
					'jobmeta', 'module', 'ret', 'success', 'user', 'user_uuid']
		try:
			assert all([key in new for key in expected_keys])

			assert 'referrer'    in new['extradat']
			assert 'wrapper_url' in new['extradat']

			if new['call'] == 'getHeadPhantomJS':
				respurl, title = new['ret'], ""
			elif new['call'] == 'getHeadTitlePhantomJS' or new['call'] == 'getHeadTitleChromium':
				if isinstance(new['ret'], (tuple, list)):
					respurl, title = new['ret']
				elif isinstance(new['ret'], dict):
					respurl = new['ret']['url']
					title   = new['ret']['title']
				else:
					raise RuntimeError("Don't know what the return type of `getHeadTitlePhantomJS` is! Type: %s" % type(new['ret']))

			else:
				raise RuntimeError("Response to unknown call: %s!" % new)


			self.process_single_source_target_mapping(
					from_outbound_wrapper  = new['extradat']['wrapper_url'],
					from_outbound_referrer = new['extradat']['referrer'],
					to_url                 = respurl,
					to_url_title           = title,
					client_id              = new['user'],
					client_key             = new['user_uuid'],
				)

			self.mon_con.incr('head-received', 1)
			return True

		except Exception:
			self.mon_con.incr('head-failed', 1)
			self.log.error("Error when processing job response!")
			for line in traceback.format_exc().split("\n"):
				self.log.error(line)

			self.log.error("Contents of head response:")

			for line in pprint.pformat(new).split("\n"):
				self.log.error(line)
			return True
		return False


	def validate_from_new(self):
		with db.session_context() as db_sess:

			have = db_sess.query(db.NuReleaseItem)                \
				.outerjoin(db.NuResolvedOutbound)                      \
				.filter(db.NuReleaseItem.validated == False)           \
				.having(func.count(db.NuResolvedOutbound.parent) >= 3) \
				.group_by(db.NuReleaseItem.id)

			new_items = []

			for valid in have.all():
				if valid.validated is False:
					assert len(list(valid.resolved)) >= 3
					not_disabled = [tmp for tmp in valid.resolved if not tmp.disabled]
					matches = urls_the_same([tmp.actual_target for tmp in not_disabled])
					if matches:
						# Since all the URLs match, just use one of them.
						valid.actual_target = valid.resolved[0].actual_target
						new_items.append((valid.seriesname, valid.actual_target))
						valid.validated = True
						self.mon_con.incr('validated', 1)

					else:
						bad = []

						# If the item resolves out to a url that indicates a squatter,
						# drop it immediately
						for resolve in valid.resolved:
							bad.append(any([tmp in resolve.actual_target for tmp in GONE_RESOLVES]))
						if any(bad):
							self.log.warning("Domain appears to now be gone. Disabling.")
							valid.reviewed = 'rejected'
							valid.validated = True
							db_sess.commit()
							return

						if len(valid.resolved) >= MAX_TOTAL_FETCH_ATTEMPTS:
							self.log.warning("Attempted more then 10 resolves. Disabling.")
							valid.reviewed = 'rejected'
							valid.validated = True
							db_sess.commit()
							return


						self.log.error("Invalid or not-matching URL set for wrapper %s!", valid.id)

						for lookup in not_disabled:
							self.log.error("	Resolved URL: %s->%s (%s)", lookup.id, lookup.actual_target, lookup.disabled)



						self.log.info("Masking oldest value.")
						oldest_time = datetime.datetime.max
						oldest_row  = None

						for lookup in not_disabled:
							if lookup.fetched_on < oldest_time:
								oldest_row = lookup
								oldest_time = lookup.fetched_on
						if oldest_row:
							self.log.info("Disabling row with ID: %s (%s) Total resolves = %s", oldest_row.id, oldest_row.actual_target, len(valid.resolved))
							oldest_row.disabled = True
							db_sess.commit()

						self.mon_con.incr('invalidated', 1)

			db_sess.commit()
			self.log.info("Added validated series: %s", len(new_items))
			for new in new_items:
				self.log.info("	Series: %s", new)

	def timestamp_validated(self):
		self.log.info("Applying a timestamp to all newly validated rows!")
		with db.session_context() as db_sess:
			unstamped = db_sess.query(db.NuReleaseItem)      \
				.filter(db.NuReleaseItem.validated == True) \
				.filter(db.NuReleaseItem.validated_on == None) \
				.all()

			for item in unstamped:
				item.validated_on = datetime.datetime.now()

			db_sess.commit()


	def do_release(self, row):

		if row.seriesname.endswith("..."):
			self.log.warning("Series name ends with dots. Skipping (%s -> %s -> %s)",
				row.seriesname.strip(), row.releaseinfo.strip(), row.actual_target.strip())
			return
		if row.groupinfo.endswith("..."):
			self.log.warning("Group name ends with dots. Skipping (%s -> %s -> %s -> %s)",
				row.groupinfo, row.seriesname.strip(), row.releaseinfo.strip(), row.actual_target.strip())
			return

		if not row.releaseinfo:
			return
		if not row.actual_target:
			return


		# Had a typo in the name_fix_lut.json file. Fix that. Also, derp.
		if row.groupinfo == 'Misty Cloud Translations' and '//2slow2latemtl.icu/' in row.actual_target:
			row.groupinfo = "2Slow2Late MTL"
			self.log.error("What?")


		if "www.webnovel.com" in row.actual_target and "/rssbook/" in row.actual_target:
			return

		self.log.info("Release for series: %s -> %s -> %s", row.seriesname.strip(), row.releaseinfo.strip(), row.actual_target.strip())


		vol, chap, frag, postfix = extractVolChapterFragmentPostfix(row.releaseinfo)


		ret = {
			'srcname'      : fix_string(row.groupinfo),
			'series'       : fix_string(row.seriesname),
			'vol'          : vol,
			'chp'          : chap,
			'frag'         : frag,
			'published'    : calendar.timegm(row.first_seen.timetuple()),
			'itemurl'      : row.actual_target,
			'postfix'      : fix_string(postfix),
			'author'       : None,
			'tl_type'      : 'translated',
			'match_author' : False,

			'nu_release'   : True

		}

		release = createReleasePacket(ret, beta=False)
		# print("Packed release:", release)
		self.rpc.put_feed_job(release)

		return row.actual_target

	def transmit_since(self, earliest=None):
		if not earliest:
			earliest = datetime.datetime.min

		release_urls = []
		with db.session_context() as db_sess:
			validated = db_sess.query(db.NuReleaseItem)      \
				.filter(db.NuReleaseItem.reviewed == 'valid')        \
				.filter(db.NuReleaseItem.validated == True)       \
				.filter(db.NuReleaseItem.validated_on > earliest) \
				.all()

			# print("validated:")
			# print(len(list(validated)))


			for row in validated:
				relurl = self.do_release(row)
				if relurl:
					release_urls.append(relurl)

			db_sess.commit()

		self.retriggerUrlList(release_urls)

	def fix_names(self):
		with db.session_context() as db_sess:
			for old, new in self.name_lut.items():
				have = db_sess.query(db.NuReleaseItem)         \
					.filter(db.NuReleaseItem.seriesname     == old) \
					.all()
				for row in have:
					try:
						assert row.seriesname == old
						row.seriesname = new
						self.log.info("Fixing name row: %s -> %s", old, row.seriesname)

						db_sess.commit()
					except sqlalchemy.exc.IntegrityError:
						self.log.error("Failure")
						traceback.print_exc()
						db_sess.rollback()
						db_sess.delete(row)
						db_sess.commit()

			for old, new in self.group_lut.items():
				have = db_sess.query(db.NuReleaseItem)         \
					.filter(db.NuReleaseItem.groupinfo     == old) \
					.all()
				for row in have:
					try:
						assert row.groupinfo == old
						row.groupinfo = new
						self.log.info("Fixing group row: %s -> %s", old, row.groupinfo)

						db_sess.commit()
					except sqlalchemy.exc.IntegrityError:
						self.log.error("Failure")
						traceback.print_exc()
						db_sess.rollback()
						db_sess.delete(row)
						db_sess.commit()

			db_sess.commit()

	def review_probable_validated_row(self, row):
		titles = [tmp.resolved_title for tmp in row.resolved]
		tgts   = [tmp.actual_target for tmp in row.resolved]
		if not all(titles):
			return

		badwords = [
			'523',
			'404',
			'sucuri website firewall',
			'403',
			'not found',
			'error',
			'wordpress.com',
			'access denied',
			'unavailable',
			'nothing found',
			'stole this page',
		]
		for title in titles:
			if any([badword in title.lower() for badword in badwords]):
				self.log.info("Badword in title: %s (%s)", titles, [badword for badword in badwords if badword in title.lower()])
				return

		if not all([tgts[0] == tgt for tgt in tgts]):
			self.log.info("URL Mismatch!")
			return

		row.reviewed = 'valid'

		self.mon_con.incr('reviewed', 1)

	def review_probable_validated(self):
		self.log.info("Doing optional validation")
		with db.session_context() as db_sess:
			new_items = db_sess.query(db.NuReleaseItem)           \
					.filter(db.NuReleaseItem.validated == True)        \
					.filter(db.NuReleaseItem.reviewed == 'unverified') \
					.filter(db.NuReleaseItem.actual_target != None)    \
					.order_by(desc(db.NuReleaseItem.first_seen))       \
					.all()


			unverified = db_sess.query(db.NuReleaseItem)           \
					.filter(db.NuReleaseItem.validated == False)        \
					.filter(db.NuReleaseItem.actual_target != None)    \
					.count()

			self.log.info("Have %s items to do validity checks on", len(new_items))
			self.log.info("%s items needing checking", unverified)

			for row in new_items:
				self.review_probable_validated_row(row)

			db_sess.commit()

	def block_for_n_responses(self, resp_cnt):
		if not resp_cnt:
			self.log.info("No head requests! Nothing to do!")
			return

		received = 0
		loops = 0
		max_loop_time = 60 * 30
		while 1:
			received += self.process_avail()
			print("\r`fetch_and_flush` sleeping for {} more responses ({} of {}, loop {} of {})\r".format(resp_cnt - received, received, resp_cnt, loops, max_loop_time), end='', flush=True)
			loops += 1
			time.sleep(1)
			if received >= resp_cnt:
				return
			if loops > max_loop_time:
				return

	def get_dotted(self):
		self.fix_names()

		dotted_series = []
		dotted_authors = []

		with db.session_context() as db_sess:
			print("Counting items to load.")
			count = db_sess.query(db.NuReleaseItem)           \
				.filter(db.NuReleaseItem.reviewed == 'valid') \
				.filter(db.NuReleaseItem.validated == True)   \
				.count()

			print("Loading")
			validated = db_sess.query(db.NuReleaseItem)       \
				.filter(db.NuReleaseItem.reviewed == 'valid') \
				.filter(db.NuReleaseItem.validated == True)   \
				.yield_per(1000)
			validated = [tmp for tmp in validated]
			# validated = [tmp for tmp in tqdm.tqdm(validated, total=count)]

		print("Found %s releases" % len(validated))

		# for row in tqdm.tqdm(validated):
		for row in validated:
			if row.seriesname.endswith("..."):
				dotted_series.append((row.seriesname.strip(), row.actual_target))
			if row.groupinfo.endswith("..."):
				dotted_authors.append((row.groupinfo, row.actual_target))

		dseries = {}
		dauths  = {}




		with db.session_context() as db_sess:
			for name, url in dotted_series:
				nl = urllib.parse.urlparse(url).netloc
				nlname = feedNameLut.getNiceName(db_sess, url)
				if not nlname:
					nlname = nl
				dseries.setdefault(nlname, {})
				dseries[nlname][name] = url

			for name, url in dotted_authors:
				nl = urllib.parse.urlparse(url).netloc
				nlname = feedNameLut.getNiceName(db_sess, url)
				if not nlname:
					nlname = nl
				dauths.setdefault(nlname, {})
				dauths[nlname][name] = url

		self.log.info("Found %s dotted series, %s dotted authors", len(dseries), len(dauths))


		with open("dotted_nu_items.pyson", "w") as fp:
			out = pprint.pformat((dseries, dauths), indent=4)
			fp.write(out)

		return (dseries, dauths)

	def trigger_all_urls(self):

		release_urls = []
		with db.session_context() as db_sess:
			validated = db_sess.query(db.NuReleaseItem)        \
				.filter(db.NuReleaseItem.reviewed  == 'valid') \
				.filter(db.NuReleaseItem.validated == True)       \
				.all()

			for row in validated:
				if not row.releaseinfo:
					continue
				if not row.actual_target:
					continue

				release_urls.append(row.actual_target)

		self.log.info("Found %s URLs", len(release_urls))

		self.retriggerUrlList(release_urls)

	def go(self):
		self.run()

	def run(self):
		self.process_avail()

		self.validate_from_new()
		self.timestamp_validated()
		self.fix_names()

		self.review_probable_validated()

		ago = datetime.datetime.now() - datetime.timedelta(days=3)
		self.transmit_since(ago)

		self.validate_from_new()
		self.timestamp_validated()

		self.do_chunk_rpc_heads()

		# active_jobs = self.put_head_jobs(put=100)
		# self.block_for_n_responses(active_jobs)

		self.validate_from_new()
		self.timestamp_validated()
		self.fix_names()

		self.review_probable_validated()

		ago = datetime.datetime.now() - datetime.timedelta(days=3)
		self.transmit_since(ago)


	def do_chunk_rpc_heads(self):

		items = self.get_rpc_head_lists()
		if not items:
			return

		jobids = [
				self.put_job(
					remote_cls    = RemoteHeaderClass,
					call_kwargs   = {'urls_to_head' : item},
					job_unique_id = str(item),
					)
			for
				item
			in
				items

		]

		for everything, ret in self.process_response_items(jobids):
			for item in ret:
				fetch_params, resp_params = item
				try:
					self.process_single_source_target_mapping(
							from_outbound_wrapper  = fetch_params['wrapper'],
							from_outbound_referrer = fetch_params['referrer'],
							to_url                 = resp_params['url'],
							to_url_title           = resp_params['title'],
							client_id              = everything['user'],
							client_key             = everything['user_uuid'],
						)


				except Exception as e:
					print()
					print(e)
					traceback.print_exc()
					print()


		# jobid = self.put_job(remote_cls, call_kwargs, meta, job_uid=job_uid)
		# ret = self.process_response_items([jobid], expect_partials)
		# if not expect_partials:
		# 	ret = next(ret)
		# return ret


def fetch_and_flush():
	hd = NuHeader()
	hd.run()

def schedule_next_exec(scheduler, at_time):
	# NU Sync system has to run with a memory jobstore, and a process pool executor,
	# because otherwise it'll try to serialize the job, and you can't serialize the
	# scheduler itself.
	scheduler.add_job(do_nu_sync,
		args               = (scheduler, ),
		trigger            = 'date',
		run_date            = at_time,
		jobstore           = 'memory',
		# executor           = 'on_the_fly',
		replace_existing   = True,
		max_instances      = 1,
		coalesce           = True,
		misfire_grace_time = 2**30)


def do_nu_sync(scheduler):
	print("do_nu_sync!", scheduler)
	try:
		fetch_and_flush()
	finally:

		sleeptime = int(random.triangular(1*60, (10*60), (5*60)))
		next_exec = datetime.datetime.now() + datetime.timedelta(seconds=sleeptime)
		schedule_next_exec(scheduler, next_exec)

		print("NU Sync executed. Next exec at ", next_exec)


class RemoteHeaderClass(RpcBaseClass):
	logname = "Main.RemoteExec.TestClass"

	def do_head_sequence(self, lock_interface, urls_to_head):
		import random

		ret = []
		if not urls_to_head:
			return ret

		with self.wg.chromiumContext(urls_to_head[0]['referrer']) as cr:
			cr.navigate_to(urls_to_head[0]['referrer'])

		sleeptime = random.triangular(2,6,10)
		self.log.info("Sleeping %s seconds", sleeptime)
		time.sleep(sleeptime)

		with self.wg.chromiumContext(urls_to_head[0]['referrer']) as cr:
			self.log.info("Current URL: %s", cr.get_current_url())


		for url_set in urls_to_head:
			try:
				self.log.info("%s", url_set)

				if lock_interface.seen_item(url_set['wrapper']):
					self.log.warning("Have seen URL %s. Skipping!", url_set['wrapper'])
					continue

				lock_interface.add_item(url_set['wrapper'])

				with self.wg.chromiumContext(urls_to_head[0]['referrer']) as cr:
					cr.navigate_to(url_set['referrer'])

				sleeptime = random.triangular(2,6,10)
				self.log.info("Sleeping %s seconds", sleeptime)
				time.sleep(sleeptime)

				val = self.wg.getHeadTitleChromium(url=url_set['wrapper'], referrer=url_set['referrer'])
				self.log.info("Head for %s -> %s", url_set['wrapper'], val)
				ret.append((url_set, val))

				sleeptime = random.triangular(2,6,10)
				self.log.info("Sleeping %s seconds", sleeptime)
				time.sleep(sleeptime)

			except Exception as e:
				self.log.error("Exception: %s", e)
				for line in traceback.format_exc().split("\n"):
					self.log.error(line)

		return ret

	def _go(self, partial_resp_interface, lock_interface, urls_to_head):
		print("%s" % (urls_to_head, ))
		self.log.info("%s", urls_to_head, )
		self.log.info("WG: %s", self.wg)
		self.log.info("partial_resp_interface: %s", partial_resp_interface)
		self.log.info("lock_interface: %s", lock_interface)
		self.log.info("WG.twocaptcha_api_key: %s", self.wg.twocaptcha_api_key)
		self.log.info("WG.anticaptcha_api_key: %s", self.wg.anticaptcha_api_key)
		self.log.info("Using shared chrome: %s", self.wg.borg_chrome_pool)

		self.log.info("lock_interface dir: %s", dir(lock_interface))
		self.log.info("lock_interface seen: %s", lock_interface.get_seen())
		# self.log.info(str(dir(lock_interface)))

		# return "Lolwat"

		return self.do_head_sequence(lock_interface, urls_to_head)

def do_schedule(scheduler):
	print("Autoscheduler!")

	exec_at = datetime.datetime.now() + datetime.timedelta(seconds=5)
	schedule_next_exec(scheduler, exec_at)

def test_all_the_same():
	set1 = [
			'http://jigglypuffsdiary.com/gk/goblin-kingdom-volume-3-the-age-of-warlords-chapter-158-maneuvering-1-2/',
			'http://jigglypuffsdiary.com/gk/goblin-kingdom-volume-3-the-age-of-warlords-chapter-158-maneuvering-1-2/?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+JigglypuffsDiary+%28Jigglypuff%27s+Diary%29',
			'http://jigglypuffsdiary.com/gk/goblin-kingdom-volume-3-the-age-of-warlords-chapter-158-maneuvering-1-2/?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+JigglypuffsDiary+%28Jigglypuff%27s+Diary%29',
		]

	set2 = [
			'http://jigglypuffsdiary.com/gk/goblin-kingdom-volume-3-the-age-of-warlords-chapter-158-confrontation-2-2/',
			'http://jigglypuffsdiary.com/gk/goblin-kingdom-volume-3-the-age-of-warlords-chapter-158-confrontation-2-2/?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+JigglypuffsDiary+%28Jigglypuff%27s+Diary%29',
			'http://jigglypuffsdiary.com/gk/goblin-kingdom-volume-3-the-age-of-warlords-chapter-158-confrontation-2-2/?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+JigglypuffsDiary+%28Jigglypuff%27s+Diary%29',
		]
	print("Set 1: ", urls_the_same(set1))
	print("Set 2: ", urls_the_same(set2))


def test():
	pass

	hdl = NuHeader()
	hdl.do_chunk_rpc_heads()
	hdl.validate_from_new()

	return

	# hdl.trigger_all_urls()
	# hdl.put_job()
	# hdl.run()
	items = hdl.get_rpc_head_lists(chunklength=15)
	pprint.pprint(items[0])


	everything, resp = hdl.blocking_dispatch_call(remote_cls=RemoteHeaderClass, call_kwargs={'urls_to_head' : items[0]})

	# print("Everything:", everything)

	pprint.pprint(everything)

	for fetch_params, (fetch_params, resp_params) in resp:
		hdl.process_single_source_target_mapping(
				from_outbound_wrapper  = fetch_params['wrapper'],
				from_outbound_referrer = fetch_params['referrer'],
				to_url                 = resp_params['url'],
				to_url_title           = resp_params['title'],
				client_id              = everything['user'],
				client_key             = everything['user_uuid'],
			)

	# hdl.review_probable_validated()

	# ago = datetime.datetime.now() - datetime.timedelta(days=30)
	# hdl.transmit_since(ago)
	# hdl.get_dotted()


if __name__ == '__main__':
	import logSetup
	logSetup.initLogging()

	# test_all_the_same()
	test()
