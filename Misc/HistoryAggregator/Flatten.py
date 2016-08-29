
import time
import urllib.parse
import pprint
import json
import datetime
import traceback
import logging
import os.path
import json
import calendar

import sqlalchemy.exc

import WebMirror.database as db
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

class DbFlattener(object):


	def __init__(self):
		self.log = logging.getLogger("Main.DbVersioning.Cleaner")
		self.qlog = logging.getLogger("Main.DbVersioning.Query")
		self.sess = db.get_db_session()

		self.snap_times = self.generate_snap_times()

	def __del__(self):
		db.delete_db_session()

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



	def relink_row_sequence(self, rows):
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
				self.sess.execute(update)

				dirty = True
			end_transaction_id = x.transaction_id

		return dirty


	def truncate_url_history(self, url):
		ctbl = version_table(db.WebPages)

		items = self.sess.query(ctbl) \
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
			if item.content == None and item.file == None:
				# self.log.info("Deleting item without a file and no content!")
				# print(type(item), item.mimetype, item.file, item.content)
				# print(ctbl.delete().where(ctbl.c.id == item.id).where(ctbl.c.transaction_id == item.transaction_id))
				# sess.execute(ctbl.delete().where(ctbl.c.id == item.id).where(ctbl.c.transaction_id == item.transaction_id))
				deleted_1 += 1
			elif item.content != None:
				# print(type(item), item.keys(), item.addtime, item.fetchtime)
				closest = min(datevec, key=self.diff_func(item))
				if not closest in attachments:
					attachments[closest] = []
				attachments[closest].append(item)


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
				# 	# sess.execute(ctbl.delete(ctbl.c.id == tmp.id and ctbl.c.transaction_id == tmp.transaction_id))
					# print("Deleting Intermediate item")
					# sess.execute(ctbl.delete().where(ctbl.c.id == tmp.id).where(ctbl.c.transaction_id == tmp.transaction_id))
					deleted_2 += 1
			elif len(superset) == 1:
				out.append(superset[0])
			else:
				raise ValueError("Wat? Key with no items!")

		deleted = deleted_1 + deleted_2
		seq_dirty = self.relink_row_sequence(out)
		if deleted > 0 or seq_dirty:
			# Rewrite the tid links so the history renders properly
			self.sess.commit()
		else:
			self.sess.rollback()

		self.log.info("Deleted: %s items when simplifying history, Total deleted: %s, remaining: %s", deleted_2, deleted, orig_cnt-deleted)

	def consolidate_history(self):

		sess = db.get_db_session()
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
				ORDER BY url
			""")
		end = list(end)
		self.qlog.info("Found %s items with more then 10 history entries. Processing", len(end))

		for count, url in end:
			self.truncate_url_history(url)

	def go(self):
		self.consolidate_history()


def test():
	import logSetup
	logSetup.initLogging()
	print("Wat")
	# truncate_url_history('http://royalroadl.com/fiction/4293')
	proc = DbFlattener()
	proc.go()

if __name__ == '__main__':
	test()