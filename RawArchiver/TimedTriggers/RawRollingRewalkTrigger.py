

import config
import urllib.parse
import datetime
import traceback
import time
import zlib
import settings
import datetime
import sqlalchemy.exc
from sqlalchemy import or_
from sqlalchemy import and_
from sqlalchemy import func
import common.database as dbm

import RawArchiver.TimedTriggers.TriggerBase


class RollingRawRewalkTriggerBase(RawArchiver.TimedTriggers.TriggerBase.TriggerBaseClass):


	pluginName = "RollingRewalk Trigger"

	loggerPath = 'Main.RollingRewalk'


	def retrigger_netloc(self, netloc, ago):
		self.log.info("Retrigging for netloc: %s", netloc)
		self.log.info("Fetching IDs requiring retriggering.")
		sess = self.db.get_db_session()
		q = sess.query(self.db.RawWebPages.id)                    \
					.filter(
						and_(
							self.db.RawWebPages.netloc == netloc,
							self.db.RawWebPages.state != 'new',
							or_(
								self.db.RawWebPages.fetchtime       < ago,
								self.db.RawWebPages.fetchtime is None
							)
							# self.db.RawWebPages.ignoreuntiltime > (datetime.datetime.min + datetime.timedelta(days=1)),
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
					q = sess.query(self.db.RawWebPages)
					q = q.filter(self.db.RawWebPages.id.in_(chunk))

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
		sess = self.db.get_db_session()
		ago = datetime.datetime.now() - datetime.timedelta(days=settings.REWALK_INTERVAL_DAYS + 2)

		minid = sess.query(func.min(self.db.RawWebPages.id)).scalar()
		maxid = sess.query(func.max(self.db.RawWebPages.id)).scalar()

		print(minid, maxid)
		chunk_size = 50000
		ids_tot = maxid - minid
		affected = 0
		for chunk in range(minid, maxid, chunk_size):
			while 1:
				try:
					self.log.info("Doing general unspecified netloc retrigger.")
					q = sess.query(self.db.RawWebPages)
					q = q.filter(self.db.RawWebPages.state != 'new')
					q = q.filter(self.db.RawWebPages.fetchtime < ago)
					q = q.filter(self.db.RawWebPages.id < (chunk + chunk_size))
					q = q.filter(self.db.RawWebPages.id >= chunk)

					affected_rows = q.update({"state" : "new"})
					affected += affected_rows
					sess.commit()
					self.log.info("Updated for all unspecified netlocs - %s rows (%s total), Id: %s, %f%% done.",
						affected_rows, affected, chunk, ((chunk - minid) / ids_tot) * 100)
					break
				except sqlalchemy.exc.InternalError:
					self.log.info("Transaction error. Retrying.")
					sess.rollback()
				except sqlalchemy.exc.OperationalError:
					self.log.info("Transaction error. Retrying.")
					sess.rollback()
				except sqlalchemy.exc.IntegrityError:
					self.log.info("Transaction error. Retrying.")
					sess.rollback()
				except sqlalchemy.exc.InvalidRequestError:
					self.log.info("Transaction error. Retrying.")
					sess.rollback()


	def go(self):

		print("Startup?")


		self.log.info("Rolling re-trigger of starting URLs.")

		starturls = []
		for module in RawArchiver.RawActiveModules.ACTIVE_MODULES:
			for url in module.get_start_urls():
				nl = urllib.parse.urlsplit(url).netloc
				self.log.info("Interval: %s, netloc: %s", module.rewalk_interval, nl)
				starturls.append((module.rewalk_interval, nl))

		starturls = set(starturls)
		starturls = list(starturls)
		starturls.sort(key=lambda x: (x[1], x[0]))

		sess = self.db.get_db_session()

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

		self.log.info("Now retriggering all old items.")
		self.retrigger_other()
		self.log.info("Old files retrigger complete.")


if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()
	run = RollingRawRewalkTriggerBase()
	run.retrigger_other()
	# run._go()

