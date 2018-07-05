
import time
import urllib.parse
import pprint
import datetime
import traceback
import os.path
import json
import calendar

import sqlalchemy.exc
from sqlalchemy.orm import joinedload
from sqlalchemy import desc
from sqlalchemy import func

from WebMirror.JobUtils import buildjob
import common.database as db

import common.get_rpyc
import common.LogBase as LogBase
import common.StatsdMixin as StatsdMixin
import random

import WebMirror.TimedTriggers.TriggerBase
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

class NuHeader(WebMirror.TimedTriggers.TriggerBase.TriggerBaseClass, StatsdMixin.StatsdMixin):
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


	loggerPath = "Main.Header.Nu"
	statsd_prefix = 'ReadableWebProxy.Nu.Header'

	go = None

	def __init__(self, connect=True):
		super().__init__()

		self.name_lut, self.group_lut = load_lut()
		# db_sess = db.get_db_session(postfix='nu_header')

		if connect:
			self.check_open_rpc_interface()


	def put_job(self, put=3):
		with db.session_context() as db_sess:
			self.log.info("Loading rows to fetch...")
			recent_d = datetime.datetime.now() - datetime.timedelta(hours=72)
			recentq = db_sess.query(db.NuReleaseItem)                \
				.outerjoin(db.NuResolvedOutbound)                         \
				.filter(db.NuReleaseItem.validated == False)              \
				.filter(db.NuReleaseItem.first_seen >= recent_d)          \
				.options(joinedload('resolved'))                          \
				.order_by(desc(db.NuReleaseItem.first_seen))              \
				.group_by(db.NuReleaseItem.id)                            \
				.limit(max(100, put*10))


			bulkq = db_sess.query(db.NuReleaseItem)                  \
				.outerjoin(db.NuResolvedOutbound)                         \
				.filter(db.NuReleaseItem.validated == False)              \
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
					module         = 'WebRequest',
					call           = 'getHeadTitleChromium',
					dispatchKey    = "fetcher",
					jobid          = -1,
					args           = [have.outbound_wrapper, have.referrer],
					kwargs         = {},
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

	def process_single_avail(self):
		'''
		Example response:

		{
			'call': 'getHeadPhantomJS',
			'cancontinue': True,
			'dispatch_key': 'fetcher',
			'extradat': {'mode': 'fetch'},
			'jobid': -1,
			'jobmeta': {'sort_key': 'a269f164a16e11e6891500163ef6fe07'},
			'module': 'NUWebRequest',
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



		expected_keys = ['call', 'cancontinue', 'dispatch_key', 'extradat', 'jobid',
					'jobmeta', 'module', 'ret', 'success', 'user', 'user_uuid']
		if new is None:
			self.log.info("No NU Head responses!")
			return False
		while True:
			with db.session_context() as db_sess:
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

					if respurl.endswith("?m=1"):
						respurl = respurl[:-len("?m=1")]

					self.log.info("Processing remote head response: %s", new)
					self.log.info("Resolved job to URL: %s", respurl)
					self.log.info("Page title: %s", title)

					# Handle the 301/2 not resolving properly.
					netloc = urllib.parse.urlsplit(respurl).netloc
					if "novelupdates" in netloc:
						self.log.warning("Failed to validate external URL. Either scraper is blocked, or phantomjs is failing.")
						return True

					if 'm.wuxiaworld.com' in respurl:
						respurl = respurl.replace('m.wuxiaworld.com', 'www.wuxiaworld.com')
					if 'tseirptranslations.blogspot.com' in respurl:
						respurl = respurl.replace('tseirptranslations.blogspot.com', 'tseirptranslations.com')
					if 'm.xianxiaworld.net' in respurl:
						respurl = respurl.replace('m.xianxiaworld.net', 'www.xianxiaworld.net')
					if 'shikkakutranslations.wordpress.com' in respurl:
						respurl = respurl.replace('shikkakutranslations.wordpress.com', 'shikkakutranslations.com')

					if any([tmp in respurl for tmp in BAD_RESOLVES]):
						self.log.warning("Bad resolve in url: '%s'. Not inserting into DB.", respurl)
						return True

					if not respurl.lower().startswith("http"):
						self.log.warning("URL '%s' does not start with 'http'. Not inserting into DB.", respurl)
						return True



					if '/?utm_source=feedburner' in respurl:
						respurl = respurl.split('/?utm_source=feedburner')[0] + "/"


					have = db_sess.query(db.NuReleaseItem)                                    \
						.options(joinedload('resolved'))                                           \
						.filter(db.NuReleaseItem.outbound_wrapper==new['extradat']['wrapper_url']) \
						.filter(db.NuReleaseItem.referrer==new['extradat']['referrer'])            \
						.scalar()

					if not have:
						self.log.error("Base row deleted from resolve?")
						return


					new = db.NuResolvedOutbound(
							client_id      = new['user'],
							client_key     = new['user_uuid'],
							actual_target  = respurl,
							resolved_title = title,
							fetched_on     = datetime.datetime.now(),
						)

					have.resolved.append(new)
					db_sess.commit()

					self.mon_con.incr('head-received', 1)
					return True
				except sqlalchemy.exc.InvalidRequestError:
					db_sess.rollback()
				except sqlalchemy.exc.OperationalError:
					db_sess.rollback()
				except sqlalchemy.exc.IntegrityError:
					db_sess.rollback()


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
			return
		if row.groupinfo.endswith("..."):
			return

		if not row.releaseinfo:
			return
		if not row.actual_target:
			return

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
				self.log.info("Badword in title: %s", titles)
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
		max_loop_time = 60 * 60
		while 1:
			received += self.process_avail()
			print("\r`fetch_and_flush` sleeping for {} more responses ({} of {}, loop {} of {})\r".format(resp_cnt - received, received, resp_cnt, loops, max_loop_time), end='', flush=True)
			loops += 1
			time.sleep(1)
			if received >= resp_cnt:
				return
			if loops > max_loop_time:
				return

	def trigger_all_urls(self):

		release_urls = []
		with db.session_context() as db_sess:
			validated = db_sess.query(db.NuReleaseItem)      \
				.filter(db.NuReleaseItem.reviewed == 'valid')        \
				.filter(db.NuReleaseItem.validated == True)       \
				.all()

			# print("validated:")
			# print(len(list(validated)))


			for row in validated:
				if not row.releaseinfo:
					continue
				if not row.actual_target:
					continue

				release_urls.append(row.actual_target)

		self.log.info("Found %s URLs", len(release_urls))

		self.retriggerUrlList(release_urls)

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
		active_jobs = self.put_job(put=100)
		self.block_for_n_responses(active_jobs)

		self.validate_from_new()
		self.timestamp_validated()
		self.fix_names()

		self.review_probable_validated()

		ago = datetime.datetime.now() - datetime.timedelta(days=3)
		self.transmit_since(ago)


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

		sleeptime = int(random.triangular(3*60, (30*60), (15*60)))
		next_exec = datetime.datetime.now() + datetime.timedelta(seconds=sleeptime)
		schedule_next_exec(scheduler, next_exec)

		print("NU Sync executed. Next exec at ", next_exec)



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


if __name__ == '__main__':
	import logSetup
	logSetup.initLogging()

	# test_all_the_same()

	hdl = NuHeader()
	hdl.trigger_all_urls()
	# hdl.run()
	# hdl.review_probable_validated()

	# ago = datetime.datetime.now() - datetime.timedelta(days=3)
	# hdl.transmit_since(ago)
