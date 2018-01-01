
import time
import multiprocessing
import urllib.parse
import pprint
import json
import datetime
import traceback
import logging
import os.path
import json
import calendar

from pympler import tracker
import objgraph
import code

import sqlalchemy.exc

import common.database as db
from sqlalchemy_continuum.utils import version_table


# # # Do the delete from the versioning table now.
# ctbl = version_table(db.WebPages)
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
			sess.execute("""
				DELETE FROM transaction;
				""")
			sess.execute("COMMIT;")


	def _go(self):
		self.truncate_transaction_table()



class DbFlattener(object):


	def __init__(self):
		self.log = logging.getLogger("Main.DbVersioning.Cleaner")
		self.qlog = logging.getLogger("Main.DbVersioning.Cleaner.Query")

		self.snap_times = self.generate_snap_times()


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

		ctbl = version_table(db.WebPages)

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


	def truncate_url_history(self, sess, url):
		ctbl = version_table(db.WebPages)

		items = sess.query(ctbl) \
			.filter(ctbl.c.url == url) \
			.all()

		items.sort(key=lambda x: (x.id, x.transaction_id, x.end_transaction_id))
		# for x in items:
		# 	print(x.id, x.transaction_id, x.end_transaction_id)

		deleted_1 = 0
		deleted_2 = 0

		orig_cnt = len(items)
		datevec = self.snap_times
		self.log.info("Clearing history for URL: %s (items: %s)", url, orig_cnt)
		attachments = {}
		for item in items:
			if item.state != "complete":
				deleted_1 += 1
				self.log.info("Deleting incomplete item for url: %s!", url)
				sess.execute(ctbl.delete().where(ctbl.c.id == item.id).where(ctbl.c.transaction_id == item.transaction_id))
			elif item.content == None and item.file == None:
				self.log.info("Deleting item without a file and no content for url: %s!", url)
				# print(type(item), item.mimetype, item.file, item.content)
				# print(ctbl.delete().where(ctbl.c.id == item.id).where(ctbl.c.transaction_id == item.transaction_id))
				sess.execute(ctbl.delete().where(ctbl.c.id == item.id).where(ctbl.c.transaction_id == item.transaction_id))
				deleted_1 += 1
			elif item.content != None:
				# print(type(item), item.keys(), item.addtime, item.fetchtime)
				closest = min(datevec, key=self.diff_func(item))
				if not closest in attachments:
					attachments[closest] = []
				attachments[closest].append(item)
			elif item.file != None:
				pass
			else:
				print("Wat?")


		self.log.info("Found %s items missing both file reference and content", deleted_1)
		keys = list(attachments.keys())
		keys.sort()

		out = []

		for key in keys:
			superset = attachments[key]
			if len(superset) > 1:
				# print("lolercoaster")
				superset.sort(key=lambda x: (x.addtime if x.fetchtime is None else x.fetchtime, x.id, x.transaction_id), reverse=True)
				out.append(superset[0])
				# print(superset[0].fetchtime, superset[0].id, superset[0].transaction_id)
				for tmp in superset[1:]:
					sess.execute(ctbl.delete().where(ctbl.c.id == tmp.id).where(ctbl.c.transaction_id == tmp.transaction_id))
					deleted_2 += 1
			elif len(superset) == 1:
				out.append(superset[0])
			else:
				raise ValueError("Wat? Key with no items!")

		deleted = deleted_1 + deleted_2
		seq_dirty = self.relink_row_sequence(sess, out)
		if deleted > 0 or seq_dirty:
			# Rewrite the tid links so the history renders properly
			self.log.info("Committing because %s items were removed!", deleted)
			sess.commit()
		else:
			sess.rollback()

		self.log.info("Deleted: %s items when simplifying history, Total deleted: %s, remaining: %s", deleted_2, deleted, orig_cnt-deleted)

	def consolidate_history(self):

		with db.session_context() as sess:
			self.qlog.info("Querying for items with significant history size")
			end = sess.execute("""
					SELECT
						count(*), url
					FROM
						web_pages_version
					GROUP BY
						url
					HAVING
						COUNT(*) > 10
					ORDER BY COUNT(*) DESC

				""")
			end = list(end)
			self.qlog.info("Found %s items with more then 10 history entries. Processing", len(end))

			sess.flush()
			sess.expire_all()

		remaining = len(end)
		for batched in batch(end, 50):

			p = multiprocessing.Process(target=incremental_history_consolidate, args=(batched, ))
			p.start()
			p.join()

			remaining = remaining - len(batched)
			self.log.info("Processed %s of %s (%s%%)", len(end)-remaining, len(end), 100-((remaining/len(end)) * 100) )

			print("Growth:")
			growth = objgraph.show_growth(limit=10)
			print(growth)


	def incremental_consolidate(self, batched):

		for count, url in batched:
			with db.session_context() as temp_sess:
				while 1:
					try:
						self.truncate_url_history(temp_sess, url)
						break
					except sqlalchemy.exc.OperationalError:
						temp_sess.rollback()

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

if __name__ == '__main__':
	test()
