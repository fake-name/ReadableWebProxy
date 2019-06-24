

import config
import urllib.parse
import datetime
import traceback
import time
import tqdm
import zlib
import settings
import datetime
import sqlalchemy.exc
from sqlalchemy import or_
from sqlalchemy import and_
from sqlalchemy import not_
from sqlalchemy import func
from sqlalchemy import text
import common.database as dbm

import WebMirror.rules
import WebMirror.TimedTriggers.TriggerBase


class RollingRewalkTriggersBase(WebMirror.TimedTriggers.TriggerBase.TriggerBaseClass):


	pluginName = "RollingRewalk Trigger"

	loggerPath = 'Main.RollingRewalker'


	def retrigger_netloc(self, netloc, ago):
		self.log.info("Retrigging for netloc: %s", netloc)
		self.log.info("Fetching IDs requiring retriggering.")
		with self.db.session_context(override_timeout_ms = 5 * 60 * 1000) as sess:
			q = sess.query(self.db.WebPages.id)                    \
						.filter(
							and_(
								self.db.WebPages.netloc == netloc,
								self.db.WebPages.state != 'new',
								self.db.WebPages.state != 'specialty_blocked',
								or_(
									self.db.WebPages.fetchtime       < ago,
									self.db.WebPages.fetchtime is None
								)
								# self.db.WebPages.ignoreuntiltime < (datetime.datetime.min + datetime.timedelta(days=1)),
							)
						)
			# print("Query:", q)
			ids = q.all()

			# Returned list of IDs is each ID packed into a 1-tuple. Unwrap those tuples so it's just a list of integer IDs.
			ids = [tmp[0] for tmp in ids]

			if ids:
				self.log.info("Updating for netloc %s. %s rows requiring update.", netloc, len(ids))
			else:
				self.log.info("No rows needing retriggering for netloc %s.", netloc)

			chunk_size = 5000
			for chunk in range(0, len(ids), chunk_size):
				chunk = ids[chunk:chunk+chunk_size]
				while 1:
					try:
						q = sess.query(self.db.WebPages)
						q = q.filter(self.db.WebPages.id.in_(chunk))

						affected_rows = q.update({"state" : "new", "ignoreuntiltime" : datetime.datetime.min}, synchronize_session=False)
						sess.commit()
						self.log.info("Update modified %s rows for netloc %s.", affected_rows, netloc)
						break
					except sqlalchemy.exc.InternalError:
						self.log.info("Transaction error (sqlalchemy.exc.InternalError). Retrying.")
						sess.rollback()
					except sqlalchemy.exc.OperationalError:
						self.log.info("Transaction error (sqlalchemy.exc.OperationalError). Retrying.")
						sess.rollback()
					except sqlalchemy.exc.IntegrityError:
						self.log.info("Transaction error (sqlalchemy.exc.IntegrityError). Retrying.")
						sess.rollback()
					except sqlalchemy.exc.InvalidRequestError:
						self.log.info("Transaction error (sqlalchemy.exc.InvalidRequestError). Retrying.")
						traceback.print_exc()
						sess.rollback()

	def retrigger_other(self):

		# Don't retrigger the URLs marked as not-rewalkable
		rules = WebMirror.rules.load_rules()
		urls = [tmp['starturls'] for tmp in rules if (tmp and tmp['starturls'] and tmp['rewalk_disabled'] == True)]
		urls = [item for sub in urls for item in sub]
		nls = list(set([urllib.parse.urlsplit(url).netloc for url in urls]))

		# Disallow nulls.
		nls = tuple([tmp for tmp in nls if tmp])

		with self.db.session_context() as sess:
			ago = datetime.datetime.now() - datetime.timedelta(days=settings.REWALK_INTERVAL_DAYS + 2)

			minid = sess.query(func.min(self.db.WebPages.id)).scalar()
			maxid = sess.query(func.max(self.db.WebPages.id)).scalar()

			update_query = text("""
				UPDATE
					web_pages
				SET
					state = 'new'
				WHERE
						state NOT IN ('new', 'error', 'removed', 'disabled', 'specialty_blocked', 'specialty_deferred')
					AND
						fetchtime < :fetch_time_ago
					AND
						id <  :max_rid
					AND
						id >= :min_rid
					AND
						netloc NOT IN :netloc_list
				""")

			self.log.info("Have to process from ID %s to %s", minid, maxid)
			chunk_size = 50000
			affected = 0

		# pbar = tqdm.tqdm(range(minid, maxid, chunk_size), desc="Retriggering non-rule URLs")
		pbar = range(minid, maxid, chunk_size)

		with self.db.session_context() as sess:
			for chunk in pbar:
				while 1:
					try:
						ret = sess.execute(update_query,
								{
									'fetch_time_ago' : ago,
									'max_rid'        : chunk + chunk_size,
									'min_rid'        : chunk,
									'netloc_list'    : nls,
								}
							)

						affected += ret.rowcount
						sess.commit()
						desc = 'Changed: %10i' % (affected, )
						pbar.set_description(desc)

						break

					except sqlalchemy.exc.InternalError:
						sess.rollback()
						self.log.warning("InternalError error. Retrying.")
						for line in traceback.format_exc().split("\n"):
							self.log.warning(line)
					except sqlalchemy.exc.OperationalError:
						sess.rollback()
						self.log.warning("OperationalError error. Retrying.")
						for line in traceback.format_exc().split("\n"):
							self.log.warning(line)
					except sqlalchemy.exc.IntegrityError:
						sess.rollback()
						self.log.warning("IntegrityError error. Retrying.")
						for line in traceback.format_exc().split("\n"):
							self.log.warning(line)
					except sqlalchemy.exc.InvalidRequestError:
						sess.rollback()
						self.log.warning("InvalidRequestError error. Retrying.")
						for line in traceback.format_exc().split("\n"):
							self.log.warning(line)
						raise

					except RecursionError:
						self.log.info("Recursion error!")
						sess.rollback()


	def go(self):

		self.log.info("Rolling re-trigger of starting URLs.")

		self.log.info("Now retriggering all old items.")
		self.retrigger_other()

		self.log.info("Retriggering all main items.")
		rules = WebMirror.rules.load_rules()


		starturls = []
		for ruleset in [tmp for tmp in rules if (tmp and tmp['starturls'] and tmp['rewalk_disabled'] == False)]:
			for starturl in ruleset['starturls']:
				if not ruleset['rewalk_interval_days']:
					interval = settings.REWALK_INTERVAL_DAYS
				else:
					interval = ruleset['rewalk_interval_days']
				nl = urllib.parse.urlsplit(starturl).netloc
				self.log.info("Interval: %s, netloc: %s", interval, nl)
				starturls.append((interval, nl))

		starturls = set(starturls)
		starturls = list(starturls)
		starturls.sort(key=lambda x: (x[1], x[0]))

		for interval, nl in starturls:

			if "wattpad.com" in nl:
				continue
			if "booksie.com" in nl:
				continue

			# "+2" is to (hopefully) allow the normal rewalk system to catch the site.
			ago = datetime.datetime.now() - datetime.timedelta(days=(interval + 2))
			self.retrigger_netloc(nl, ago)

			# def conditional_check(row):
			# 	if day == today or row.fetchtime < (datetime.datetime.now() - datetime.timedelta(days=settings.REWALK_INTERVAL_DAYS)):
			# 		print("Retriggering: ", row, row.fetchtime, row.url)
			# 		row.state    = "new"
			# 		row.distance = 0
			# 		row.priority = dbm.DB_IDLE_PRIORITY
			# 		row.ignoreuntiltime = datetime.datetime.now() - datetime.timedelta(days=1)

			# self.retriggerUrl(url, conditional=conditional_check)

		self.log.info("Old files retrigger complete.")


if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()
	run = RollingRewalkTriggersBase()
	run.retrigger_other()
	# run._go()

