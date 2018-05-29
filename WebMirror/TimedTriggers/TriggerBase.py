

import logging
import tqdm
import abc
import datetime

import sys
if '__pypy__' in sys.builtin_module_names:
	import psycopg2cffi as psycopg2
else:
	import psycopg2

import traceback
import urllib.parse
import sqlalchemy.exc
import common.database as db
import common.LogBase

class TriggerBaseClass(common.LogBase.LoggerMixin, metaclass=abc.ABCMeta):

	# Abstract class (must be subclassed)
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def pluginName(self):
		return None

	@abc.abstractmethod
	def go(self):
		return None


	def __init__(self):
		super().__init__()
		self.loggerPath = "Main.Trigger.%s" % self.loggerPath
		self.db = db
		self.log.info("Loading %s Runner", self.pluginName)


	def _go(self):
		self.log.info("Checking %s for updates", self.pluginName)

		self.go()
		self.log.info("Update check for %s finished.", self.pluginName)


	def __raw_retrigger_with_cursor(self, url, cursor):

		# self.log.info("Retriggering fetch for URL: %s", url)

		#  Fucking huzzah for ON CONFLICT!
		cmd = """

				INSERT INTO
					web_pages
					(url, starturl, netloc, distance, is_text, priority, addtime, state)
				VALUES
					(%(url)s, %(starturl)s, %(netloc)s, %(distance)s, %(is_text)s, %(priority)s, %(addtime)s, %(state)s)
				ON CONFLICT (url) DO
					UPDATE
						SET
							state           = %(state)s,
							distance        = LEAST(EXCLUDED.distance, web_pages.distance),
							priority        = LEAST(EXCLUDED.priority, web_pages.priority),
							addtime         = LEAST(EXCLUDED.addtime, web_pages.addtime),
							ignoreuntiltime = LEAST(EXCLUDED.addtime, web_pages.addtime, %(ignoreuntiltime)s)
						WHERE
						(
								(web_pages.state = 'complete' OR web_pages.state = 'new' OR web_pages.state = 'fetching' OR web_pages.state = 'error')
							AND
								web_pages.url = %(url)s
						)
				RETURNING
					web_pages.state, web_pages.url
					;

			""".replace("	", " ").replace("\n", " ")

		url_netloc = urllib.parse.urlsplit(url).netloc

		assert url.startswith("http")
		assert url_netloc


		# Forward-data the next walk, time, rather then using now-value for the thresh.
		data = {
			'url'             : url,
			'starturl'        : url,
			'netloc'          : url_netloc,
			'distance'        : 0,
			'is_text'         : True,
			'priority'        : db.DB_HIGH_PRIORITY,
			'state'           : "new",
			'addtime'         : datetime.datetime.now(),

			# Don't retrigger unless the ignore time has elaped.
			'ignoreuntiltime' : datetime.datetime.min,
			}

		cursor.execute(cmd, data)
		ret = cursor.fetchall()
		if not ret:
			self.log.warning("Row appears to already be in the new state: %s", url)
		return ret

	def retriggerUrlList(self, urlList):

		sess = self.db.get_db_session()

		raw_cur = sess.connection().connection.cursor()
		commit_each = False
		while 1:
			loopcnt = 0
			try:
				try:
					for url in tqdm.tqdm(urlList, desc="Retriggering for %s plugin" % self.pluginName):
						loopcnt += 1
						self.__raw_retrigger_with_cursor(url, raw_cur)
						if (commit_each and (loopcnt % 5) == 0) or (loopcnt % 250) == 0:
							self.log.info("Committing!")
							raw_cur.execute("COMMIT;")
					raw_cur.execute("COMMIT;")
					break
				except AttributeError:
					self.log.warning("TQDM Issue. Siiiiiiigh")
					for url in urlList:
						loopcnt += 1
						self.__raw_retrigger_with_cursor(url, raw_cur)
						if (commit_each and (loopcnt % 5) == 0) or (loopcnt % 250) == 0:
							self.log.info("Committing!")
							raw_cur.execute("COMMIT;")
					raw_cur.execute("COMMIT;")
					break

			except psycopg2.Error:
				if commit_each is False:
					self.log.warning("psycopg2.Error - Retrying with commit each.")
				else:
					self.log.warning("psycopg2.Error - Retrying.")
					traceback.print_exc()

				raw_cur.execute("ROLLBACK;")
				commit_each = True



	def retriggerUrl(self, url, conditional=None):

		sess = self.db.get_db_session()

		raw_cur = sess.connection().connection.cursor()
		while 1:
			try:
				self.__raw_retrigger_with_cursor(url, raw_cur)
				raw_cur.execute("COMMIT;")
				break

			except psycopg2.Error:
				self.log.warning("psycopg2.Error - Retrying.")
				traceback.print_exc()
				raw_cur.execute("ROLLBACK;")


if __name__ == "__main__":
	import utilities.testBase as tb

	with tb.testSetup(startObservers=True):

		run = Runner()
		run.go()

