

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
from sqlalchemy.sql.expression import nullslast

import common.database as db

import common.get_rpyc
import common.LogBase as LogBase
import random
import bsonrpc.exceptions
from WebMirror.NewJobQueue import buildjob

from WebMirror.OutputFilters.util.MessageConstructors import fix_string
from WebMirror.OutputFilters.util.MessageConstructors import createReleasePacket
from WebMirror.OutputFilters.util.TitleParsers import extractVolChapterFragmentPostfix



# Remove blogspot garbage subdomains from the TLD (if present)
def urls_the_same(url_list):
	fixed_urls = []
	for url in url_list:
		p = urllib.parse.urlparse(url)
		f = (p[0], p[1].split(".blogspot.")[0], p[2], p[3], p[4])
		fixed = urllib.parse.urlunsplit(f)
		fixed_urls.append(fixed)

	return all([fixed_urls[0] == tmp for tmp in fixed_urls])

def load_lut():
	outf = os.path.join(os.path.split(__file__)[0], 'name_fix_lut.json')
	jctnt = open(outf).read()
	lut = json.loads(jctnt)
	return lut

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


	def __init__(self, connect=True):
		super().__init__()

		self.name_lut, self.group_lut = load_lut()
		self.db_sess = db.get_db_session(postfix='nu_header')

		if connect:
			self.check_open_rpc_interface()

	def put_job(self, put=3):
		self.log.info("Loading a row to fetch...")
		# haveq = self.db_sess.query(db.NuReleaseItem)                   \
		# 	.outerjoin(db.NuResolvedOutbound)                         \
		# 	.filter(db.NuReleaseItem.validated == False)              \
		# 	.having(func.count(db.NuResolvedOutbound.parent) < 3)     \
		# 	.order_by(func.random())                                  \
		# 	.group_by(db.NuReleaseItem.id)                            \
		# 	.limit(max(100, put*3))

		# # .order_by(desc(db.NuReleaseItem.first_seen))                \
		# moar = haveq.all()


		self.log.info("Loading a row to fetch...")
		haveq = self.db_sess.query(db.NuReleaseItem)                   \
			.outerjoin(db.NuResolvedOutbound)                         \
			.filter(db.NuReleaseItem.validated == False)              \
			.having(func.count(db.NuResolvedOutbound.parent) < 3)     \
			.order_by(desc(db.NuReleaseItem.first_seen))              \
			.group_by(db.NuReleaseItem.id)                            \
			.limit(max(100, put*3))

		haveset = haveq.all()

		# haveset += moar

		if not haveset:
			self.log.info("No jobs to remote HEAD.")
			return

		# We pick a large number of items, and randomly choose one of them.
		# This lets us weight the fetch preferentially to the recent items, but still
		# have some variability.

		haveset = random.sample(haveset, put)

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

		while self.process_single_avail():
			self.log.info("Processing response!")


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


		errors = 0
		while 1:
			try:
				new = self.rpc.get_job()
				break
			except TypeError:
				self.check_open_rpc_interface()
			except KeyError:
				self.check_open_rpc_interface()
			except bsonrpc.exceptions.BsonRpcError as e:
				errors += 1
				self.check_open_rpc_interface()
				if errors > 3:
					raise e
				else:
					self.log.warning("Exception in RPC request:")
					for line in traceback.format_exc().split("\n"):
						self.log.warning(line)



		expected_keys = ['call', 'cancontinue', 'dispatch_key', 'extradat', 'jobid',
					'jobmeta', 'module', 'ret', 'success', 'user', 'user_uuid']
		if new is None:
			self.log.info("No NU Head responses!")
			return False
		while True:
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
					return True


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
				return True
			except sqlalchemy.exc.InvalidRequestError:
				self.db_sess.rollback()
			except sqlalchemy.exc.OperationalError:
				self.db_sess.rollback()
			except sqlalchemy.exc.IntegrityError:
				self.db_sess.rollback()


			except Exception:
				self.log.error("Error when processing job response!")
				for line in traceback.format_exc().split("\n"):
					self.log.error(line)

				self.log.error("Contents of head response:")

				for line in pprint.pformat(new).split("\n"):
					self.log.error(line)
				return True
		return False


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



	def do_release(self, row):

		if row.seriesname.endswith("..."):
			return

		if not row.releaseinfo:
			return
		if not row.actual_target:
			return

		self.log.info("Release for series: %s -> %s -> %s", row.seriesname, row.releaseinfo, row.actual_target)


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

	def transmit_since(self, earliest=None):
		if not earliest:
			earliest = datetime.datetime.min

		validated = self.db_sess.query(db.NuReleaseItem)      \
			.filter(db.NuReleaseItem.reviewed == True)        \
			.filter(db.NuReleaseItem.validated == True)       \
			.filter(db.NuReleaseItem.validated_on > earliest) \
			.all()

		# print("validated:")
		# print(len(list(validated)))

		for row in validated:
			self.do_release(row)


	def fix_names(self):
		for old, new in self.name_lut.items():
			have = self.db_sess.query(db.NuReleaseItem)         \
				.filter(db.NuReleaseItem.seriesname     == old) \
				.all()
			for row in have:
				try:
					assert row.seriesname == old
					row.seriesname = new
					self.log.info("Fixing name row: %s -> %s", old, row.seriesname)

					self.db_sess.commit()
				except sqlalchemy.exc.IntegrityError:
					self.log.error("Failure")
					traceback.print_exc()
					self.db_sess.rollback()
					self.db_sess.delete(row)
					self.db_sess.commit()

		for old, new in self.group_lut.items():
			have = self.db_sess.query(db.NuReleaseItem)         \
				.filter(db.NuReleaseItem.groupinfo     == old) \
				.all()
			for row in have:
				try:
					assert row.groupinfo == old
					row.groupinfo = new
					self.log.info("Fixing group row: %s -> %s", old, row.groupinfo)

					self.db_sess.commit()
				except sqlalchemy.exc.IntegrityError:
					self.log.error("Failure")
					traceback.print_exc()
					self.db_sess.rollback()
					self.db_sess.delete(row)
					self.db_sess.commit()

		self.db_sess.commit()

def fetch_and_flush():
	hd = NuHeader()
	hd.process_avail()
	hd.validate_from_new()
	hd.timestamp_validated()
	hd.put_job(put=100)
	mins = 10
	for x in range(mins):
		hd.process_avail()
		for y in range(60):
			time.sleep(1)
			print("\r`fetch_and_flush` sleeping for {}\r".format(str((mins * 60) - (x * 60 + y)).rjust(4)), end='')

	hd.validate_from_new()
	hd.timestamp_validated()
	hd.fix_names()

	ago = datetime.datetime.now() - datetime.timedelta(days=3)
	hd.transmit_since(ago)


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
		CLIENT_NUM = 2

		sleeptime = int(random.triangular(15*60, (60*60), (30*60 / CLIENT_NUM)))
		next_exec = datetime.datetime.now() + datetime.timedelta(seconds=sleeptime)
		schedule_next_exec(scheduler, next_exec)

		print("NU Sync executed. Next exec at ", next_exec)



def do_schedule(scheduler):
	print("Autoscheduler!")

	exec_at = datetime.datetime.now() + datetime.timedelta(seconds=5)
	schedule_next_exec(scheduler, exec_at)



