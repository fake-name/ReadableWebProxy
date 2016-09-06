

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import common.LogBase as LogBase
import runStatus
import queue
import time
import os.path
import os
import sys
import sqlalchemy.exc
import random
import settings
import pprint

import Misc.diff_match_patch as dmp
from sqlalchemy import desc


import common.util.urlFuncs
import urllib.parse
import traceback
import datetime
import psycopg2

from sqlalchemy.sql import text
from sqlalchemy.sql import func
import common.util.webFunctions as webFunctions

import hashlib
import common.database as db
from config import C_RAW_RESOURCE_DIR


from sqlalchemy_continuum.utils import version_table

import common.global_constants


def getHash(fCont):

	m = hashlib.md5()
	m.update(fCont)
	return m.hexdigest()




def saveFile(filecont, url, filename, mimetype):
	# use the first 3 chars of the hash for the folder name.
	# Since it's hex-encoded, that gives us a max of 2^12 bits of
	# directories, or 4096 dirs.

	dirPath = os.path.join(C_RAW_RESOURCE_DIR, dirName)
	if not os.path.exists(dirPath):
		os.makedirs(dirPath)

	ext = os.path.splitext(filename)[-1]
	ext   = ext.lower()

	# The "." is part of the ext.
	filename = '{filename}{ext}'.format(filename=fHash, ext=ext)


	# The "." is part of the ext.
	filename = '{filename}{ext}'.format(filename=fHash, ext=ext)

	# Flask config values have specious "/./" crap in them. Since that gets broken through
	# the abspath canonization, we pre-canonize the config path so it compares
	# properly.
	confpath = os.path.abspath(C_RAW_RESOURCE_DIR)

	fqpath = os.path.join(dirPath, filename)
	fqpath = os.path.abspath(fqpath)

	if not fqpath.startswith(confpath):
		raise ValueError("Generating the file path to save a cover produced a path that did not include the storage directory?")

	locpath = fqpath[len(confpath):]
	if not os.path.exists(fqpath):
		print("Saving file to path: '{fqpath}'!".format(fqpath=fqpath))
		with open(fqpath, "wb") as fp:
			fp.write(filecont)
	else:
		print("File '{fqpath}' already exists!".format(fqpath=fqpath))

	if locpath.startswith("/"):
		locpath = locpath[1:]
	return locpath


########################################################################################################################
#
#	##     ##    ###    #### ##    ##     ######  ##          ###     ######   ######
#	###   ###   ## ##    ##  ###   ##    ##    ## ##         ## ##   ##    ## ##    ##
#	#### ####  ##   ##   ##  ####  ##    ##       ##        ##   ##  ##       ##
#	## ### ## ##     ##  ##  ## ## ##    ##       ##       ##     ##  ######   ######
#	##     ## #########  ##  ##  ####    ##       ##       #########       ##       ##
#	##     ## ##     ##  ##  ##   ###    ##    ## ##       ##     ## ##    ## ##    ##
#	##     ## ##     ## #### ##    ##     ######  ######## ##     ##  ######   ######
#
########################################################################################################################


class RawSiteArchiver(LogBase.LoggerMixin):

	loggerPath = "Main.RawArchiver"

	# Fetch items up to 1,000,000 (1 million) links away from the root source
	# This (functionally) equates to no limit.
	# The db defaults to  (e.g. max signed integer value) anyways
	FETCH_DISTANCE = 1000 * 1000

	def __init__(self, cookie_lock, db_interface, use_socks=False):
		# print("RawSiteArchiver __init__()")
		super().__init__()

		self.cookie_lock = cookie_lock
		self.db_sess = db_interface
		self.db      = db

		self.wg = webFunctions.WebGetRobust(cookie_lock=cookie_lock, use_socks=use_socks)



	def checkHaveHistory(self, url):
		ctbl = version_table(db.RawWebPages)

		count = self.db_sess.query(ctbl) \
			.filter(ctbl.c.url == url)   \
			.count()
		return count


	# Update the row with the item contents
	def upsertReponseContent(self, job, response):

		start = urllib.parse.urlsplit(job.starturl).netloc
		interval = settings.REWALK_INTERVAL_DAYS
		if start in self.netloc_rewalk_times and self.netloc_rewalk_times[start]:
			interval = self.netloc_rewalk_times[start]

		assert interval > 7
		ignoreuntiltime = (datetime.datetime.now() + datetime.timedelta(days=interval))




		while True:
			history_size = self.checkHaveHistory(job.url)
			if history_size > 0:
				break
			try:
				self.log.info("Need to push content into history table (current length: %s).", history_size)
				job.title           = (job.title + " ")    if job.title    else " "
				job.content         = (job.content + " ")  if job.content  else " "
				job.mimetype        = (job.mimetype + " ") if job.mimetype else " "

				job.fetchtime = datetime.datetime.now() - datetime.timedelta(days=7)

				self.db_sess.commit()
				self.log.info("Pushing old job content into history table!")
				break
			except sqlalchemy.exc.OperationalError:
				self.db_sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				self.db_sess.rollback()

		while 1:
			try:

				job.title           = response['title']
				job.content         = response['contents']
				job.mimetype        = response['mimeType']
				job.ignoreuntiltime = ignoreuntiltime


				if "text" in job.mimetype:
					job.is_text  = True
				else:
					job.is_text  = False

				job.state    = 'complete'

				# Disabled for space-reasons.
				# if 'rawcontent' in response:
				# 	job.raw_content = response['rawcontent']

				job.fetchtime = datetime.datetime.now()

				self.db_sess.commit()
				self.log.info("Marked plain job with id %s, url %s as complete!", job.id, job.url)
				break
			except sqlalchemy.exc.OperationalError:
				self.db_sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				self.db_sess.rollback()

	def generalLinkClean(self, link, badwords):
		if link.startswith("data:"):
			return None
		linkl = link.lower()
		if any([badword in linkl for badword in badwords]):
			# print("Filtered:", link)
			return None
		return link


	def filterLinks(self, job, links):
		ret = set()
		for link in links:
			link = self.generalLinkClean(link)
			if not link:
				continue

			ret.add(link)
		return ret


	def upsertResponseLinks(self, job, links):
		self.log.info("Updating database with response links")
		links    = set(links)

		orig = len(links)

		links    = self.filterLinks(job,  links)
		post_filter = len(links)

		self.log.info("Upserting %s links (%s filtered)" % (post_filter, orig-post_filter))


		new_starturl = job.starturl,
		new_distance = job.distance+1
		new_priority = job.priority
		new_type     = job.type

		raw_cur = self.db_sess.connection().connection.cursor()

		if self.resp_q != None:
			for link in links:
				start = urllib.parse.urlsplit(link).netloc

				assert link.startswith("http")
				assert start
				new = {
						'url'             : link,
						'starturl'        : new_starturl,
						'netloc'          : start,
						'distance'        : new_distance,
						'priority'        : new_priority,
						'type'            : new_type,
						'state'           : "new",
						'addtime'         : datetime.datetime.now(),

						# Don't retrigger unless the ignore time has elaped.
						'ignoreuntiltime' : datetime.datetime.now(),
					}
				self.resp_q.put(("new_link", new))

				while self.resp_q.qsize() > 1000:
					time.sleep(0.1)

			self.log.info("Links upserted. Items in processing queue: %s", self.resp_q.qsize())
		else:
			#  Fucking huzzah for ON CONFLICT!
			cmd = """
					INSERT INTO
						web_pages
						(url, starturl, netloc, distance, priority, type, addtime, state)
					VALUES
						(%(url)s, %(starturl)s, %(netloc)s, %(distance)s, %(priority)s, %(type)s, %(addtime)s, %(state)s)
					ON CONFLICT (url) DO
						UPDATE
							SET
								state           = EXCLUDED.state,
								starturl        = EXCLUDED.starturl,
								netloc          = EXCLUDED.netloc,
								distance        = LEAST(EXCLUDED.distance, web_pages.distance),
								priority        = GREATEST(EXCLUDED.priority, web_pages.priority),
								addtime         = LEAST(EXCLUDED.addtime, web_pages.addtime)
							WHERE
							(
									web_pages.ignoreuntiltime < %(ignoreuntiltime)s
								AND
									web_pages.url = EXCLUDED.url
								AND
									(web_pages.state = 'complete' OR web_pages.state = 'error')
							)
						;
					""".replace("	", " ").replace("\n", " ")

			# Only commit per-URL if we're tried to do the update in batch, and failed.
			commit_each = False
			for link in links:
				while 1:
					try:
						start = urllib.parse.urlsplit(link).netloc

						assert link.startswith("http")
						assert start


						# Forward-data the next walk, time, rather then using now-value for the thresh.
						data = {
							'url'             : link,
							'starturl'        : new_starturl,
							'netloc'          : start,
							'distance'        : new_distance,
							'priority'        : new_priority,
							'type'            : new_type,
							'state'           : "new",
							'addtime'         : datetime.datetime.now(),

							# Don't retrigger unless the ignore time has elaped.
							'ignoreuntiltime' : datetime.datetime.now(),
							}
						raw_cur.execute(cmd, data)
						if commit_each:
							raw_cur.execute("COMMIT;")
						break
					except psycopg2.Error:
						if commit_each is False:
							self.log.warn("psycopg2.Error - Retrying with commit each.")
						else:
							self.log.warn("psycopg2.Error - Retrying.")
							traceback.print_exc()

						raw_cur.execute("ROLLBACK;")
						commit_each = True

			raw_cur.execute("COMMIT;")




	########################################################################################################################
	#
	#	########  ########   #######   ######  ########  ######   ######      ######   #######  ##    ## ######## ########   #######  ##
	#	##     ## ##     ## ##     ## ##    ## ##       ##    ## ##    ##    ##    ## ##     ## ###   ##    ##    ##     ## ##     ## ##
	#	##     ## ##     ## ##     ## ##       ##       ##       ##          ##       ##     ## ####  ##    ##    ##     ## ##     ## ##
	#	########  ########  ##     ## ##       ######    ######   ######     ##       ##     ## ## ## ##    ##    ########  ##     ## ##
	#	##        ##   ##   ##     ## ##       ##             ##       ##    ##       ##     ## ##  ####    ##    ##   ##   ##     ## ##
	#	##        ##    ##  ##     ## ##    ## ##       ##    ## ##    ##    ##    ## ##     ## ##   ###    ##    ##    ##  ##     ## ##
	#	##        ##     ##  #######   ######  ########  ######   ######      ######   #######  ##    ##    ##    ##     ##  #######  ########
	#
	########################################################################################################################




	def get_job_from_id(self, jobid):

		self.db_sess.flush()
		job = self.db_sess.query(self.db.RawWebPages) \
			.filter(self.db.RawWebPages.id == jobid)    \
			.scalar()
		self.db_sess.flush()

		if not job:
			self.db_sess.commit()
			return False

		# Don't dump old jobs that have been accidentally reset.
		if job.state == 'new':
			job.state = 'fetching'
			self.db_sess.commit()

		if job.state != 'fetching':
			self.db_sess.commit()
			self.log.info("Job not in expected state (state: %s).", job.state)
			return None

		self.db_sess.commit()
		self.log.info("Job for url: '%s' fetched. State: '%s'", job.url, job.state)

		self.db_sess.flush()


		return job


	def taskProcess(self):
		'''
		Return true if there was something to do, false if not.
		'''
		job = None
		try:

			while runStatus.run_state.value == 1:
				rpcresp = self.getRpcResp()
				if not rpcresp:
					return False
				self.process_rpc_response(rpcresp)


		except Exception:

			for line in traceback.format_exc().split("\n"):
				self.log.critical("%s", line.rstrip())
		return True



def test():
	archiver = RawSiteArchiver(None)

	new = {
		'url'       : 'http://www.royalroadl.com/fiction/1484',
		'starturl'  : 'http://www.royalroadl.com/',
		'netloc'    : "www.royalroadl.com",
		'distance'  : 50000,
		'is_text'   : True,
		'priority'  : 500000,
		'type'      : 'unknown',
		'fetchtime' : datetime.datetime.now(),
		}

	cmd = text("""
			INSERT INTO
				web_pages
				(url, starturl, netloc, distance, is_text, priority, type, fetchtime)
			VALUES
				(:url, :starturl, :netloc, :distance, :is_text, :priority, :type, :fetchtime)
			ON CONFLICT DO NOTHING
			""")
	print("doing")
	# ins = archiver.db.get_session().execute(cmd, params=new)
	# print("Doneself. Ret:")
	# print(ins)
	# print(archiver.resetDlstate())
	print(archiver.getRpcResp())
	# print(archiver.getRpcResp())
	# print(archiver.getRpcResp())
	# print(archiver.taskProcess())
	pass

def test2():
	ruleset = WebMirror.rules.load_rules()
	netloc_rewalk_times = build_rewalk_time_lut(ruleset)
	print(netloc_rewalk_times)


if __name__ == "__main__":
	test2()


