

import logging
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

import WebMirror.UrlUpserter
import WebMirror.misc

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



	def __url_to_dict(self, url, ignoreignore):
		url_netloc = urllib.parse.urlsplit(url).netloc

		# Forward-data the next walk, time, rather then using now-value for the thresh.
		data = {
				'url'             : url,
				'starturl'        : url,
				'netloc'          : url_netloc,
				'distance'        : 0,
				'is_text'         : True,
				'priority'        : db.DB_HIGH_PRIORITY if ignoreignore else db.DB_LOW_PRIORITY,
				'type'            : "unknown",
				'state'           : "new",
				'addtime'         : datetime.datetime.now(),

				# Don't retrigger unless the ignore time has elaped or we're in force mode.
				'epoch'           : 0 if ignoreignore else WebMirror.misc.get_epoch_for_url(url),
			}
		return data


	def __retrigger_with_cursor(self, url, cursor, ignoreignore, retrigger_complete=False):

		# self.log.info("Retriggering fetch for URL: %s", url)

		retrigger_conditional = '''web_pages.state = 'complete' OR ''' if retrigger_complete else ""

		#  Fucking huzzah for ON CONFLICT!
		cmd = """
				INSERT INTO
					web_pages
					(url, starturl, netloc, distance, is_text, priority, addtime, state, epoch)
				VALUES
					(%(url)s, %(starturl)s, %(netloc)s, %(distance)s, %(is_text)s, %(priority)s, %(addtime)s, %(state)s, %(epoch)s)
				ON CONFLICT (url) DO
					UPDATE
						SET
							state           = %(state)s,
							distance        = LEAST(EXCLUDED.distance, web_pages.distance),
							-- The lowest priority is 10.
							priority        = LEAST(EXCLUDED.priority, web_pages.priority, 10),
							addtime         = LEAST(EXCLUDED.addtime, web_pages.addtime),
							epoch           = LEAST(EXCLUDED.epoch, web_pages.epoch)
						WHERE
						(
								(
									{retrigger}
									   web_pages.state = 'new'
									OR web_pages.state = 'fetching'
									OR web_pages.state = 'error'
									OR web_pages.state = 'skipped'
									OR web_pages.state = 'manually_deferred'
									OR web_pages.state = 'single_step_deferred'
								)
							AND
								web_pages.url = %(url)s
						)
					;

			""".replace("	", " ").format(retrigger = retrigger_conditional)


		url_netloc = urllib.parse.urlsplit(url).netloc

		assert url.startswith("http")
		assert url_netloc

		data = self.__url_to_dict(url, ignoreignore)
		cursor.execute(cmd, data)
		rowcnt = cursor.rowcount
		return rowcnt

	def retriggerUrlList(self, urlList, ignoreignore=False, retrigger_complete=False):

		self.log.info("Triggering %s URLs from list", len(urlList))

		with common.database.session_context(override_timeout_ms=60 * 1000 * 5) as sess:

			raw_cur = sess.connection().connection.cursor()

			commit_each = False
			changed = 0
			while 1:
				loopcnt = 0
				changed = 0
				try:
					for url in urlList:
						loopcnt += 1
						changed += self.__retrigger_with_cursor(url, raw_cur, ignoreignore=ignoreignore, retrigger_complete=retrigger_complete)
						if commit_each or (loopcnt % 250) == 0:
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

		self.log.info("Retrigger changed %s rows", changed)


	def retriggerUrl(self, url, conditional=None, ignoreignore=False):
		self.retriggerUrlList([url], ignoreignore)


if __name__ == "__main__":
	import utilities.testBase as tb

	with tb.testSetup(startObservers=True):

		run = Runner()
		run.go()

