

import time
import urllib.parse
import pprint
import json
import datetime
import traceback
import os.path
import json
import calendar
import urllib.parse

import sqlalchemy.exc
from sqlalchemy.orm import joinedload
from sqlalchemy import desc
from sqlalchemy import func

import common.database as db

import common.get_rpyc
import common.LogBase as LogBase
import random
from WebMirror.NewJobQueue import buildjob


# Remove blogspot garbage subdomains from the TLD (if present)
def urls_the_same(url_list):
	fixed_urls = []
	for url in url_list:
		p = urllib.parse.urlparse(url)
		f = (p[0], p[1].split(".blogspot.")[0], p[2], p[3], p[4])
		fixed = urllib.parse.urlunsplit(f)
		fixed_urls.append(fixed)

	return all([fixed_urls[0] == tmp for tmp in fixed_urls])


class NuHeader(LogBase.LoggerMixin):
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

	loggerPath = "Main.Neader.Nu"


	def __init__(self):
		super().__init__()

		self.db_sess = db.get_db_session(postfix='nu_header')
		self.rpc = common.get_rpyc.RemoteJobInterface("NuHeader")

	def put_job(self, put=3):
		self.log.info("Loading a row to fetch...")
		haveq = self.db_sess.query(db.NuReleaseItem)                   \
			.outerjoin(db.NuResolvedOutbound)                         \
			.filter(db.NuReleaseItem.validated == False)              \
			.having(func.count(db.NuResolvedOutbound.parent) < 3)     \
			.order_by(func.random())                                  \
			.group_by(db.NuReleaseItem.id)                            \
			.limit(max(1000, put))

		# .order_by(desc(db.NuReleaseItem.first_seen))              \
		haveset = haveq.all()

		if not haveset:
			self.log.info("No jobs to remote HEAD.")
			return

		# We pick a large number of items, and randomly choose one of them.
		# This lets us weight the fetch preferentially to the recent items, but still
		# have some variability.
		random.shuffle(haveset)

		haveset = haveset[:put]

		for have in haveset:
			if len(list(have.resolved)) >= 3:
				raise RuntimeError("Overresolved item that's not valid.")

			self.log.info("Putting job for url '%s'", have.outbound_wrapper)
			self.log.info("Referring page '%s'", have.referrer)
			raw_job = buildjob(
				module         = 'NUWebRequest',
				call           = 'getHeadPhantomJS',
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
				unique_id      = have.outbound_wrapper
			)

			self.rpc.put_job(raw_job)


	def process_avail(self):
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
		new = self.rpc.get_job()

		expected_keys = ['call', 'cancontinue', 'dispatch_key', 'extradat', 'jobid',
					'jobmeta', 'module', 'ret', 'success', 'user', 'user_uuid']
		if new is None:
			self.log.info("No NU Head responses!")
			return

		try:
			self.log.info("Processing remote head response: %s", new)
			assert all([key in new for key in expected_keys])
			assert new['call'] == 'getHeadPhantomJS'

			assert 'referrer'    in new['extradat']
			assert 'wrapper_url' in new['extradat']

			# Handle the 301/2 not resolving properly.
			netloc = urllib.parse.urlsplit(new['ret']).netloc
			if "novelupdates" in netloc:
				self.log.warning("Failed to validate external URL. Either scraper is blocked, or phantomjs is failing.")
				return


			have = self.db_sess.query(db.NuReleaseItem)                                    \
				.options(joinedload('resolved'))                                           \
				.filter(db.NuReleaseItem.outbound_wrapper==new['extradat']['wrapper_url']) \
				.filter(db.NuReleaseItem.referrer==new['extradat']['referrer'])            \
				.one()

			new = db.NuResolvedOutbound(
					client_id      = new['user'],
					client_key     = new['user_uuid'],
					actual_target  = new['ret'],
					fetched_on     = datetime.datetime.now(),
				)

			have.resolved.append(new)
			self.db_sess.commit()
		except Exception:
			self.log.error("Error when processing job response!")
			for line in traceback.format_exc().split("\n"):
				self.log.error(line)

			self.log.error("Contents of head response:")

			for line in pprint.pformat(new).split("\n"):
				self.log.error(line)

	def validate_from_new(self):
		have = self.db_sess.query(db.NuReleaseItem)                \
			.outerjoin(db.NuResolvedOutbound)                      \
			.filter(db.NuReleaseItem.validated == False)           \
			.having(func.count(db.NuResolvedOutbound.parent) >= 3) \
			.group_by(db.NuReleaseItem.id)

		new_items = []

		for valid in have.all():
			if valid.validated is False:
				assert len(list(valid.resolved)) >= 3
				matches = urls_the_same([tmp.actual_target for tmp in valid.resolved])
				if matches:
					# Since all the URLs match, just use one of them.
					valid.actual_target = valid.resolved[0].actual_target

					if not valid.seriesname.endswith("..."):
						new_items.append((valid.seriesname, valid.actual_target))
						valid.validated = True

				else:
					self.log.error("Invalid or not-matching URL set for wrapper!")

					for lookup in valid.resolved:
						self.log.error("	Resolved URL: %s", lookup.actual_target)

		self.db_sess.commit()
		self.log.info("Added validated series: %s", len(new_items))
		for new in new_items:
			self.log.info("	Series: %s", new)

	def timestamp_validated(self):
		self.log.info("Applying a timestamp to all newly validated rows!")
		unstamped = self.db_sess.query(db.NuReleaseItem)      \
			.filter(db.NuReleaseItem.validated == True) \
			.filter(db.NuReleaseItem.validated_on == None) \
			.all()

		for item in unstamped:
			item.validated_on = datetime.datetime.now()

		self.db_sess.commit()


def fetch_and_flush():
	hd = NuHeader()
	hd.process_avail()
	hd.validate_from_new()
	hd.timestamp_validated()
	hd.put_job(put=100)
	for x in range(10):
		hd.process_avail()
		time.sleep(60)

	hd.validate_from_new()
	hd.timestamp_validated()

def schedule_next_exec(scheduler, at_time):
	# NU Sync system has to run with a memory jobstore, and a process pool executor,
	# because otherwise it'll try to serialize the job, and you can't serialize the
	# scheduler itself.
	scheduler.add_job(do_nu_sync,
		args               = (scheduler, ),
		trigger            = 'date',
		run_date            = at_time,
		jobstore           = 'memory',
		executor           = 'on_the_fly',
		replace_existing   = True,
		max_instances      = 1,
		coalesce           = True,
		misfire_grace_time = 2**30)


def do_nu_sync(scheduler):
	print("do_nu_sync!", scheduler)
	try:
		fetch_and_flush()
	finally:
		CLIENT_NUM = 3

		sleeptime = int(random.triangular(15*60, (60*60), (30*60 / CLIENT_NUM)))
		next_exec = datetime.datetime.now() + datetime.timedelta(seconds=sleeptime)
		schedule_next_exec(scheduler, next_exec)

		print("NU Sync executed. Next exec at ", next_exec)



def do_schedule(scheduler):
	print("Autoscheduler!")

	exec_at = datetime.datetime.now() + datetime.timedelta(seconds=5)
	schedule_next_exec(scheduler, exec_at)


	pass

