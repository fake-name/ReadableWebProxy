

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
			'ignoreuntiltime'    : datetime.datetime.min if ignoreignore else datetime.datetime.now(),
			'ignore_ignore_time' : ignoreignore,
			}
		return data

	def retriggerUrlList(self, urlList, ignoreignore=False):

		if ignoreignore:
			self.log.warning("Doing high-priority URL upsert!")

		with self.db.session_context() as sess:
			priority = db.DB_HIGH_PRIORITY if ignoreignore else db.DB_IDLE_PRIORITY
			dictlinks = [self.__url_to_dict(url, ignoreignore) for url in urlList]
			show_progress = len(dictlinks) > 500
			WebMirror.UrlUpserter.do_link_batch_update_sess(self.log, sess, dictlinks, priority, show_progress=show_progress)


	def retriggerUrl(self, url, conditional=None, ignoreignore=False):
		self.retriggerUrlList([url], ignoreignore)


if __name__ == "__main__":
	import utilities.testBase as tb

	with tb.testSetup(startObservers=True):

		run = Runner()
		run.go()

