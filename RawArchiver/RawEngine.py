

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import common.LogBase as LogBase
import runStatus
import queue
import mimetypes
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
from config import C_RAW_RESOURCE_DIR


from sqlalchemy_continuum.utils import version_table

import common.global_constants
import RawArchiver.RawActiveModules


def getHash(fCont):

	m = hashlib.md5()
	m.update(fCont)
	return m.hexdigest()


def saveFile(filecont, url, filename):
	# use the first 3 chars of the hash for the folder name.
	# Since it's hex-encoded, that gives us a max of 2^12 bits of
	# directories, or 4096 dirs.

	split = urllib.parse.urlsplit(url)


	urlpath, urlfname = os.path.split(split.path)
	if not urlpath.startswith("/"):
		urlpath = "/"+urlpath
	urlpath = "./"+split.netloc+urlpath
	print(urlpath)

	dirPath = os.path.join(C_RAW_RESOURCE_DIR, urlpath)
	assert dirPath.startswith(C_RAW_RESOURCE_DIR)

	# Pick the longer name that contains the other, or
	# concatenate the two together.
	if filename.lower() in urlfname.lower():
		outname = urlfname
	elif urlfname.lower() in filename.lower():
		outname = filename
	else:
		outname = urlfname + " - " + filename

	fqpath = os.path.join(dirPath, outname)
	fqpath = os.path.abspath(fqpath)
	dirPath = os.path.abspath(dirPath)
	assert fqpath.startswith(C_RAW_RESOURCE_DIR)
	assert dirPath.startswith(C_RAW_RESOURCE_DIR)

	if not os.path.exists(dirPath):
		os.makedirs(dirPath)

	if os.path.exists(fqpath):
		fname, ext = os.path.splitext(fqpath)
		fhash = getHash(filecont)
		# The "." is part of the ext.
		fqpath = '{fname} - {fhash}{ext}'.format(fname=fname, fhash=fhash, ext=ext)

	assert fqpath.startswith(C_RAW_RESOURCE_DIR)

	print("Saving file to path: '{fqpath}'!".format(fqpath=fqpath))
	with open(fqpath, "wb") as fp:
		fp.write(filecont)

	locpath = fqpath[len(C_RAW_RESOURCE_DIR):]
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

	def __init__(self, cookie_lock, db_interface, db, use_socks=False):
		# print("RawSiteArchiver __init__()")
		super().__init__()

		self.cookie_lock = cookie_lock
		self.db_sess = db_interface
		self.db      = db

		self.wg = webFunctions.WebGetRobust(cookie_lock=cookie_lock, use_socks=use_socks)


	def get_file_name_mime(self, url):
		pgctnt, hName, mime = self.wg.getFileNameMime(url)

		parsed = urllib.parse.urlparse(url)
		pathname = os.path.split(parsed.path)[-1]
		if not hName and not mime and not pathname:
			self.log.error("cannot figure out content type for url: %s", url)
			return pgctnt, "unknown.unknown", "application/octet-stream"

		# empty path with mimetype of text/html generally means it's a directory index (or some horrible dynamic shit).
		if not hName and not pathname and mime == "text/html":
			self.log.info("No path and root location. Assuming index.html")
			return pgctnt, "index.html", "text/html"

		ftype, guessed_mime = mimetypes.guess_type(hName)
		if ftype:
			return pgctnt, hName, guessed_mime if not mime else mime

		ftype, guessed_mime = mimetypes.guess_type(pathname)
		if ftype:
			return pgctnt, pathname, guessed_mime if not mime else mime

		chunks = [hName, pathname]
		chunks = [chunk for chunk in chunks if chunk]

		outname = " - ".join(chunks)
		if mime and mimetypes.guess_extension(mime):
			newext = mimetypes.guess_extension(mime)
		else:
			newext = ".unknown"

		if not outname:
			outname = "unknown"
		return pgctnt, outname+newext, mime if mime else "application/octet-stream"




	def checkHaveHistory(self, url):
		ctbl = version_table(self.db.RawWebPages)

		count = self.db_sess.query(ctbl) \
			.filter(ctbl.c.url == url)   \
			.count()
		return count

	def getModuleForUrl(self, url):

		for module in RawArchiver.RawActiveModules.ACTIVE_MODULES:
			print("Module:", module, module.cares_about_url)
			if module.cares_about_url(url):
				return module
		raise RuntimeError("Unwanted URL: %s" % url)

	# Update the row with the item contents
	def do_job(self, job):
		self.getModuleForUrl(job.url)
		self.log.info("Fetching %s", job.url)
		ctnt, fname, mimetype = self.get_file_name_mime(job.url)
		if isinstance(ctnt, str):
			ctnt = ctnt.encode("utf-8")
		saved_to = saveFile(ctnt, job.url, fname)

		interval = self.getModuleForUrl(job.url).rewalk_interval

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
				job.state           = 'complete'
				job.fetchtime       = datetime.datetime.now()
				job.ignoreuntiltime = ignoreuntiltime
				job.fspath          = saved_to
				job.mimetype        = mimetype

				self.db_sess.commit()
				self.log.info("Marked plain job with id %s, url %s as complete!", job.id, job.url)
				break
			except sqlalchemy.exc.OperationalError:
				self.db_sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				self.db_sess.rollback()

	def generalLinkClean(self, link):
		if link.startswith("data:"):
			return None
		linkl = link.lower()
		if any([badword in linkl for badword in common.global_constants.GLOBAL_BAD_URLS]):
			return None

		for module in RawArchiver.RawActiveModules.ACTIVE_MODULES:
			if module.cares_about_url(link):
				return link

		return None


	def filterLinks(self, links):
		ret = set()
		for link in links:
			link = self.generalLinkClean(link)
			if not link:
				continue

			ret.add(link)
		return ret




	def upsertResponseLinks(self, job, links):
		self.log.info("Updating database with response links")
		links       = set(links)
		orig        = len(links)
		links       = self.filterLinks(links)
		post_filter = len(links)

		self.log.info("Upserting %s links (%s filtered)" % (post_filter, orig-post_filter))


		new_starturl = job.starturl,
		new_distance = job.distance+1
		new_priority = job.priority

		raw_cur = self.db_sess.connection().connection.cursor()

		#  Fucking huzzah for ON CONFLICT!
		cmd = """
				INSERT INTO
					web_pages
					(url, starturl, netloc, distance, priority, addtime, state)
				VALUES
					(%(url)s, %(starturl)s, %(netloc)s, %(distance)s, %(priority)s, %(addtime)s, %(state)s)
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
		while 1:
			try:
				for link in links:
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
						'state'           : "new",
						'addtime'         : datetime.datetime.now(),

						# Don't retrigger unless the ignore time has elaped.
						'ignoreuntiltime' : datetime.datetime.now(),
						}
					raw_cur.execute(cmd, data)
					if commit_each:
						raw_cur.execute("COMMIT;")
					break
				raw_cur.execute("COMMIT;")
			except psycopg2.Error:
				if commit_each is False:
					self.log.warn("psycopg2.Error - Retrying with commit each.")
				else:
					self.log.warn("psycopg2.Error - Retrying.")
					traceback.print_exc()

				raw_cur.execute("ROLLBACK;")
				commit_each = True





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
				self.new
				rpcresp = self.getRpcResp()
				if not rpcresp:
					return False
				self.process_rpc_response(rpcresp)


		except Exception:

			for line in traceback.format_exc().split("\n"):
				self.log.critical("%s", line.rstrip())
		return True



def test():

	import common.database
	sess = common.database.get_db_session()

	job = common.database.RawWebPages(
		state    = 'new',
		url      = 'http://ux.stackexchange.com/questions/98914/the-perfect-credit-card-number-field',
		starturl = 'http://somethingpositive.net',
		netloc   = 'somethingpositive.net',
		priority = common.database.DB_LOW_PRIORITY,
		distance = 0,
		)

	archiver = RawSiteArchiver(None, db_interface=sess, db=common.database)

	print(job)
	archiver.do_job(job)
	print("doing")

	pass

def test2():
	ruleset = WebMirror.rules.load_rules()
	netloc_rewalk_times = build_rewalk_time_lut(ruleset)
	print(netloc_rewalk_times)


if __name__ == "__main__":
	test()


