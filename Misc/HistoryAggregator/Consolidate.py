
import sys
import datetime
import traceback
import logging
import os.path
import json
import calendar
import tqdm

# if '__pypy__' not in sys.builtin_module_names:
# 	from pympler import tracker

import objgraph
import code
import concurrent.futures

import sqlalchemy.exc
import sqlalchemy.orm

if '__pypy__' in sys.builtin_module_names:
	import psycopg2cffi as psycopg2
else:
	import psycopg2

import WebMirror.rules
import common.database as db
from sqlalchemy_continuum_vendored.utils import version_table

# # # Do the delete from the versioning table now.
# ctbl = version_table(db.WebPages.__table__)
# loc2 = and_(
# 		ctbl.c.netloc.in_(ruleset['netlocs']),
# 		or_(*(ctbl.c.url.like("%{}%".format(badword)) for badword in ruleset['badwords']))
# 	)
# # print("Doing count on Versioning table ")
# # count = sess.query(ctbl) \
# # 	.filter(or_(*opts)) \
# # 	.count()

# if count == 0:
# 	print("{num} items in versioning table match badwords from file {file}. No deletion required ".format(file=ruleset['filename'], num=count))
# else:
# 	print("{num} items in versioning table match badwords from file {file}. Deleting ".format(file=ruleset['filename'], num=count))

# 	sess.query(ctbl) \
# 		.filter(or_(*loc2)) \
# 		.delete(synchronize_session=False)

FLATTEN_SCAN_INTERVAL = datetime.timedelta(days=30)

def batch(iterable, n=1):
	l = len(iterable)
	for ndx in range(0, l, n):
		yield iterable[ndx:min(ndx + n, l)]

class TransactionTruncator(object):


	def __init__(self):
		self.log = logging.getLogger("Main.DbVersioning.TransactionTruncator")
		self.qlog = logging.getLogger("Main.DbVersioning.TransactionTruncator.Query")

	def truncate_transaction_table(self):
		with db.session_context() as sess:
			self.qlog.info("Deleting items in transaction table")
			sess.execute("""TRUNCATE transaction;""")
			sess.execute("COMMIT;")
			self.qlog.info("Vacuuming table")
			sess.execute("""VACUUM VERBOSE transaction;""")
			sess.execute("COMMIT;")
			self.qlog.info("Table truncated!")

	def _go(self):
		self.truncate_transaction_table()



class DbFlattener(object):


	def __init__(self):
		self.log = logging.getLogger("Main.DbVersioning.Cleaner")
		self.qlog = logging.getLogger("Main.DbVersioning.Cleaner.Query")

		self.snap_times = self.generate_snap_times()

		rules =  WebMirror.rules.load_rules()
		self.feed_urls = [tmp for item in rules for tmp in item['feedurls']]


	def ago(self, then):
		if then == None:
			return "Never"
		now = datetime.datetime.now()
		delta = now - then

		d = delta.days
		h, s = divmod(delta.seconds, 3600)
		m, s = divmod(s, 60)
		labels = ['d', 'h', 'm', 's']
		dhms = ['%s %s' % (i, lbl) for i, lbl in zip([d, h, m, s], labels)]
		for start in range(len(dhms)):
			if not dhms[start].startswith('0'):
				break
		for end in range(len(dhms)-1, -1, -1):
			if not dhms[end].startswith('0'):
				break
		return ', '.join(dhms[start:end+1])


	def generate_snap_times(self):
		incr = datetime.datetime.now()
		times = []

		# Include the most latest snapshot
		times.append(incr)

		incr = incr.replace(minute=0, second=0, microsecond=0)
		times.append(incr)
		# Hourly snapshots for the last 24 hours
		for dummy_x in range(48):
			incr = incr - datetime.timedelta(hours=1)
			times.append(incr)



		incr = incr.replace(hour=0, minute=0, second=0, microsecond=0)
		# daily snapshots for a month
		for dummy_x in range(32):
			times.append(incr)
			incr = incr - datetime.timedelta(hours=24)

		# for item in times:
		# 	print(ago(item))

		# Weekly snapshots before that
		for dummy_x in range(52*20):
			times.append(incr)
			incr = incr - datetime.timedelta(hours=24 * 7)

		times.sort()
		return times

	def diff_func(self, diff_from):
		# lambda x: abs((x - item.addtime if not item.fetchtime else item.fetchtime).total_seconds())
		def captured_func(diff_to):
			tgt = diff_from.addtime if diff_from.fetchtime is None else diff_from.fetchtime
			ret = tgt - diff_to
			ret = abs(ret.total_seconds())
			return ret

		return captured_func



	def relink_row_sequence(self, sess, rows):
		'''
		Each Sqlalchemy-Continum transaction references the next transaction in the chain as it's `end_transaction_id`
		except the most recent (where the value of end_transaction_id is `None`)

		Therefore, we iterate over the history in reverse, and for each item set it's `end_transaction_id` to the
		id of the next transaction, so the history linked list works correctly.
		'''

		ctbl = version_table(db.WebPages.__table__)

		rows.sort(reverse=True, key=lambda x: (x.id, x.transaction_id, x.end_transaction_id))
		end_transaction_id = None
		dirty = False
		for x in rows:
			if x.end_transaction_id != end_transaction_id:
				self.log.info("Need to change end_transaction_id from %s to %s", x.end_transaction_id, end_transaction_id)

				update = ctbl.update().where(ctbl.c.id == x.id).where(ctbl.c.transaction_id == x.transaction_id).values(end_transaction_id=end_transaction_id)
				# print(update)
				sess.execute(update)

				dirty = True
			end_transaction_id = x.transaction_id

		return dirty

	def consolidate_history(self):
		try:
			with open("high_incidence_items.json") as fp:
				high_incidence_items = json.load(fp)
				self.log.info("Using json cached query results!")
		except Exception:
			self.log.warning("No cached json results. Rerunning query.")
			with db.session_context() as sess:
				self.qlog.info("Querying for items with significant history size")
				high_incidence_items = sess.execute("""
						SELECT
							count(*), url
						FROM
							web_pages_version
						GROUP BY
							url
						HAVING
							COUNT(*) > 10

					""")
				high_incidence_items = [list(tmp) for tmp in high_incidence_items]
				self.qlog.info("Found %s items with more then 10 history entries. Processing", len(high_incidence_items))

				sess.flush()
				sess.expire_all()

			self.log.info("Writing items to json file.")
			with open("high_incidence_items.json", "w") as fp:
				json.dump(high_incidence_items, fp)

		self.log.info("Processing in chunks")

		# high_incidence_items.sort()
		high_incidence_items.sort(reverse=True)

		# m_tracker = tracker.SummaryTracker()
		with concurrent.futures.ThreadPoolExecutor(max_workers = 1) as exc:
			self.log.info("Submitting tasks to worker queue.")
			for batchset in batch(list(batch(high_incidence_items, 50)), 50):
				for paramset in batchset:
					exc.submit(self.incremental_consolidate, paramset)
					# self.incremental_consolidate(paramset)
				# incremental_history_consolidate(paramset);
				# self.log.info("Printing memory deltas.")
				# m_tracker.print_diff()
			self.log.info("All jobs submitted. Waiting for executor to complete!")

	def truncate_url_history(self, sess, url):

		last_check = db.get_from_version_check_table(sess, url)

		if last_check > datetime.datetime.now() - FLATTEN_SCAN_INTERVAL:
			self.log.info("Url %s checked within the check interval (%s, %s). Skipping.", url, FLATTEN_SCAN_INTERVAL, last_check)
			return 0
		else:
			self.log.info("Url %s last checked %s.", url, last_check)


		ctbl = version_table(db.WebPages.__table__)

		if url in self.feed_urls:
			self.log.info("Feed URL (%s)! Deleting history wholesale!", url)

			res = sess.execute(
					ctbl.delete() \
					.where(ctbl.c.url == url)
				)
			self.log.info("Modified %s rows", res.rowcount)
			sess.commit()
			self.log.info("Committed. Setting version log.")
			db.set_in_version_check_table(sess, url, datetime.datetime.now())
			new_val = db.get_from_version_check_table(sess, url)
			self.log.info("New value from DB: %s", new_val)

			return



		self.log.info("Counting rows for url %s.", url)
		orig_cnt = sess.query(ctbl)           \
			.filter(ctbl.c.url == url)     \
			.count()

		self.log.info("Found %s results for url %s. Fetching rows", orig_cnt, url)

		deleted_1 = 0
		deleted_2 = 0

		datevec = self.snap_times
		attachments = {}

		for item in tqdm.tqdm(
			sess.query(ctbl)                               \
			.filter(ctbl.c.url == url)                     \
			.order_by(ctbl.c.id, ctbl.c.transaction_id)    \
			.yield_per(50), total=orig_cnt):

			if item.state != "complete" and item.state != 'error':
				deleted_1 += 1
				self.log.info("Deleting incomplete item for url: %s (state: %s)!", url, item.state)
				sess.execute(ctbl.delete().where(ctbl.c.id == item.id).where(ctbl.c.transaction_id == item.transaction_id))
			elif item.content is None and item.file is None:
				self.log.info("Deleting item without a file and no content for url: %s!", url)
				# print(type(item), item.mimetype, item.file, item.content)
				# print(ctbl.delete().where(ctbl.c.id == item.id).where(ctbl.c.transaction_id == item.transaction_id))
				sess.execute(ctbl.delete().where(ctbl.c.id == item.id).where(ctbl.c.transaction_id == item.transaction_id))
				deleted_1 += 1
			elif item.content != None:
				closest = min(datevec, key=self.diff_func(item))
				if not closest in attachments:
					attachments[closest] = []

				attachments[closest].append({
						'addtime'        : item.addtime,
						'fetchtime'      : item.fetchtime,
						'id'             : item.id,
						'transaction_id' : item.transaction_id,
					})

			elif item.file != None:
				pass
			else:
				print("Wat?")



		self.log.info("Found %s items missing both file reference and content", deleted_1)
		keys = list(attachments.keys())
		keys.sort()

		out = []

		for key in tqdm.tqdm(keys):
			superset = attachments[key]
			if len(superset) > 1:
				# print("lolercoaster")
				superset.sort(key=lambda x: (x['addtime'] if x['fetchtime'] is None else x['fetchtime'], x['id'], x['transaction_id']), reverse=True)
				out.append(superset[0])
				# print(superset[0].fetchtime, superset[0].id, superset[0].transaction_id)
				self.log.info("Deleting %s items (out of %s) from date-segment %s", len(superset)-1, len(superset), key)
				for tmp in superset[1:]:
					sess.execute(ctbl.delete().where(ctbl.c.id == tmp['id']).where(ctbl.c.transaction_id == tmp['transaction_id']))
					deleted_2 += 1
			elif len(superset) == 1:
				out.append(superset[0])
			else:
				raise ValueError("Wat? Key with no items!")

		deleted = deleted_1 + deleted_2
		# seq_dirty = self.relink_row_sequence(sess, out)
		# if deleted > 0 or seq_dirty:
		if deleted > 0:
			# Rewrite the tid links so the history renders properly
			# self.log.info("Committing because %s items were removed!", deleted)
			sess.commit()
		else:
			sess.rollback()

		db.set_in_version_check_table(sess, url, datetime.datetime.now())

		self.log.info("Deleted: %s items when simplifying history, %s incomplete items, Total deleted: %s, remaining: %s", deleted_2, deleted_1, deleted, orig_cnt-deleted)
		return deleted

	def truncate_url_range(self, sess, range_start, range_end):
		# self.log.info("Querying for items with significant history size in range %s -> %s", range_start, range_end)
		urls = sess.execute("""
				SELECT
					count(*), url
				FROM
					web_pages_version
				WHERE
					id > :min_id
				AND
					id <= :max_id
				GROUP BY
					url
				HAVING
					COUNT(*) > 10
				ORDER BY COUNT(*) DESC

			""", {
				'min_id' : range_start,
				'max_id' : range_end,
			})
		urls = list(urls)
		urls = [tmp[1] for tmp in urls]

		urls = [tmp for tmp in urls if tmp not in self.url_hit_list]

		ret = 0

		for url in urls:
			self.url_hit_list.add(url)
			ret += self.truncate_url_history(sess, url)

		return ret
		# self.log.info("Found %s URLs in range that require processing.", len(urls))

		# self.log.info("Deleted: %s items when simplifying history, Total deleted: %s, remaining: %s", deleted_2, deleted, orig_cnt-deleted)

	def consolidate_history_new(self):

		with db.session_context() as sess:
			self.qlog.info("Querying for items with significant history size")
			end = sess.execute("""
					SELECT
						min(id), max(id)
					FROM
						web_pages_version
				""")
			start, end = list(end)[0]
			self.qlog.info("Database Extents: %s -> %s", start, end)

			sess.flush()
			sess.expire_all()

		self.url_hit_list = set()

		step = 50000
		start = start - (start % step)
		pbar = tqdm.tqdm(range(start, end, step))

		# m_tracker = tracker.SummaryTracker()

		delta = 0

		deleted = 0
		for x in pbar:
			with db.session_context() as sess:
				pbar.set_description("Deleted %s. Processed %s urls" % (deleted, len(self.url_hit_list)))
				try:
					changed  = self.truncate_url_range(sess, x, x+step)
					deleted += changed

				except sqlalchemy.exc.OperationalError:
					self.log.error("Error in range section %s -> %s", x, x+step)
					for line in traceback.format_exc().split("\n"):
						self.log.error(line)
					sess.rollback()

				delta   += 1
				if delta > 5000:
					delta = 0
					# m_tracker.print_diff()
		# worker_count = 4
		# executor = concurrent.futures.ProcessPoolExecutor(max_workers = worker_count)
		# for batchset in batch(list(batch(end, 50)), 50):
		# 	executor = concurrent.futures.ProcessPoolExecutor(max_workers = worker_count)
		# 	res = []
		# 	for paramset in batchset:

		# 		future = executor.submit(incremental_history_consolidate, paramset)
		# 		res.append(future)

		# 		if len(res) > 10:
		# 			self.log.info("Processing results incrementally.")
		# 			while res:
		# 				res.pop().result()

		# executor.shutdown()

			# for res in batch_res:
			# 	self.log.info("Processed %s of %s (%s%%)", len(end)-remaining, len(end), 100-((remaining/len(end)) * 100) )


	def incremental_consolidate(self, batched):

		for count, url in batched:
			with db.session_context() as temp_sess:
				while 1:
					try:
						self.truncate_url_history(temp_sess, url)
						break
					except psycopg2.InternalError:
						temp_sess.rollback()
					except sqlalchemy.exc.OperationalError:
						temp_sess.rollback()
					except Exception:
						temp_sess.rollback()
						traceback.print_exc()

	def tickle_rows(self, sess, urlset):
		jobs = []
		self.log.info("Querying for records")
		try:

			for url in urlset:
				jobs.append(sess.query(db.WebPages).filter(db.WebPages.url == url).scalar())

		except sqlalchemy.exc.OperationalError:
			self.log.error("Failure during update (OperationalError)?")
			sess.rollback()
			return

		except sqlalchemy.exc.InvalidRequestError:
			self.log.error("Failure during update (InvalidRequestError)?")
			sess.rollback()
			return
		self.log.info("Processing fetched records")

		while True:
			try:

				for job in jobs:
					if not job:
						continue
					# self.log.info("Need to push content into history table for URL: %s.", job.url)

					cachedtitle = job.title
					cachedtime  = job.fetchtime

					job.title           = (job.title + " ")    if job.title    else " "
					job.fetchtime = datetime.datetime.now()
					# print("Mutated", job, job.fetchtime)
				sess.commit()
				for job in jobs:

					job.title     = cachedtitle
					job.fetchtime = cachedtime
					job.ignoreuntiltime = datetime.datetime.min
					# print("Mutated", job, job.fetchtime)
				sess.flush()
				sess.commit()
				# self.log.info("Pushed!")

				break
			except sqlalchemy.exc.OperationalError:
				self.log.error("Failure during update (OperationalError)?")
				sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				self.log.error("Failure during update (InvalidRequestError)?")
				sess.rollback()

		sess.flush()

		for item in jobs:
			del item
		del jobs

	def fix_missing_history(self):

		with db.session_context() as sess:
			self.qlog.info("Querying for DB items without any history")
			end = sess.execute("""
				SELECT
					t1.url
				FROM
					web_pages t1
				LEFT JOIN
					web_pages_version t2 ON t2.url = t1.url
				WHERE
					t2.url IS NULL

				""")
			end = [tmp[0] for tmp in end]
			self.log.info("Found %s rows missing history content!", len(end))

			loop = 0
			remaining = len(end)
			for urlset in batch(end, 50):
				self.tickle_rows(sess, urlset)
				sess.expire_all()

				remaining = remaining - len(urlset)
				self.log.info("Processed %s of %s (%s%%)", len(end)-remaining, len(end), 100-((remaining/len(end)) * 100) )

				print("Growth:")
				growth = objgraph.show_growth(limit=10)
				print(growth)


	def wat(self):
		with db.session_context() as sess:
			urls = ['http://rancerqz.com/tag/chapter-release/']
			self.tickle_rows(sess, urls)


	def _go(self):
		self.consolidate_history()
		self.fix_missing_history()

def incremental_history_consolidate(batched):
	proc = DbFlattener()
	proc.incremental_consolidate(batched)

def consolidate_history():
	proc = DbFlattener()
	proc.consolidate_history()

def fix_missing_history():
	proc = DbFlattener()
	proc.fix_missing_history()

def test():
	import logSetup
	logSetup.initLogging()
	# truncate_url_history('http://royalroadl.com/fiction/4293')
	proc = DbFlattener()
	# proc.wat()
	proc.fix_missing_history()
	# proc._go()

def test_jt_big_page_flatten():
	import logSetup
	logSetup.initLogging()

	print("Trying to flatten huge history")

	giant_history = 'http://japtem.com/fanfic.php'


	proc = DbFlattener()
	with db.session_context() as sess:
		proc.truncate_url_history(sess, giant_history)

if __name__ == '__main__':
	test_jt_big_page_flatten()
