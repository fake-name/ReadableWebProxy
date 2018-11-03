


import queue
import mimetypes
import time
import os.path
import os
import sys
import urllib.parse
import traceback
import datetime
import hashlib

import sqlalchemy.exc
import WebRequest
from sqlalchemy_continuum_vendored.utils import version_table

import common.database
import common.global_constants
import common.LogBase as LogBase
import common.util.DbCookieJar as dbCj
import common.util.urlFuncs
import RawArchiver.misc
import RawArchiver.RawActiveModules
import RawArchiver.RawJobDispatcher
import RawArchiver.RawUrlUpserter
import common.StatsdMixin as StatsdMixin
import runStatus
from config import C_RAW_RESOURCE_DIR

if '__pypy__' in sys.builtin_module_names:
	import psycopg2cffi as psycopg2
else:
	import psycopg2


def getHash(fCont):

	m = hashlib.md5()
	m.update(fCont)
	return m.hexdigest()


def hours(num):
	return 60*60*num

def splitall(path):
	allparts = []
	while 1:
		parts = os.path.split(path)
		if parts[0] == path:  # sentinel for absolute paths
			allparts.insert(0, parts[0])
			break
		elif parts[1] == path: # sentinel for relative paths
			allparts.insert(0, parts[1])
			break
		else:
			path = parts[0]
			allparts.insert(0, parts[1])
	return allparts

RESOURCE_SPLIT = splitall(C_RAW_RESOURCE_DIR)

def create_dir_ignoring_files(fqpath, dir_suffix = "_d"):

	dirPath, fName = os.path.split(fqpath)

	full_split = splitall(dirPath)

	root_segment = full_split[:len(RESOURCE_SPLIT)]

	for x in range(len(RESOURCE_SPLIT), len(full_split)):

		inc_path = os.path.join(*(root_segment + [full_split[x], ]))
		if os.path.exists(inc_path) and os.path.isdir(inc_path):
			root_segment.append(full_split[x])
		elif os.path.exists(inc_path) and os.path.isfile(inc_path):
			root_segment.append(full_split[x] + dir_suffix)
		else:
			# This could probably short-circuit since the first non
			# existent item means the rest of the path is safe, but w/e
			root_segment.append(full_split[x])


	dirPath = os.path.join(*root_segment)
	os.makedirs(dirPath, exist_ok=True)

	fqpath = os.path.join(dirPath, fName)

	return fqpath


def saveFile(filecont, url, filename):

	split = urllib.parse.urlsplit(url)


	urlpath, urlfname = os.path.split(split.path)
	if not urlpath.startswith("/"):
		urlpath = "/"+urlpath

	nlpath = split.netloc.split(".")
	nlpath.reverse()
	nlpath = "/".join(nlpath)

	urlpath = "./"+nlpath+urlpath

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
	fqpath = create_dir_ignoring_files(fqpath)
	fqpath = os.path.abspath(fqpath)

	dirPath = os.path.abspath(dirPath)

	assert fqpath.startswith(C_RAW_RESOURCE_DIR)
	assert dirPath.startswith(C_RAW_RESOURCE_DIR)

	if os.path.exists(fqpath):
		fname, ext = os.path.splitext(fqpath)
		fhash = getHash(filecont)
		# The "." is part of the ext.
		fqpath = '{fname} - {fhash}{ext}'.format(fname=fname, fhash=fhash, ext=ext)

	assert fqpath.startswith(C_RAW_RESOURCE_DIR)

	# print("Saving file to path: '{fqpath}'!".format(fqpath=fqpath))
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



class RawSiteArchiver(LogBase.LoggerMixin, StatsdMixin.StatsdMixin):

	statsd_prefix = 'ReadableWebProxy.Proc.SiteArchiver'
	loggerPath = "Main.RawArchiver"

	# Fetch items up to 1,000,000 (1 million) links away from the root source
	# This (functionally) equates to no limit.
	# The db defaults to  (e.g. max signed integer value) anyways
	FETCH_DISTANCE = 1000 * 1000


	@property
	def wg(self):
		if getattr(self, '_RawSiteArchiver__wg', None) is None:
			print("Creating WG Interface!")
			alt_cj = dbCj.DatabaseCookieJar(db=self.db, session=self.db.get_db_session(postfix="_cookie_interface"))
			self.__wg = WebRequest.WebGetRobust(
					use_socks     = self.__wr_use_socks,
					alt_cookiejar = alt_cj,
				)
		return self.__wg

	def __init__(self,
					total_worker_count,
					worker_num,
					new_job_queue,
					cookie_lock,
					db_interface,
					response_queue,
					db        = None,
					use_socks = False):
		# print("RawSiteArchiver __init__()")
		super().__init__()

		if db is None:
			db = common.database

		self.total_worker_count = total_worker_count
		self.worker_num   = worker_num
		self.new_job_queue = new_job_queue


		self.__wr_cookie_lock = cookie_lock
		self.__wr_use_socks   = use_socks


		self.cookie_lock = cookie_lock
		self.db_sess = db_interface
		self.db      = db



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
		ctbl = version_table(self.db.RawWebPages.__table__)

		count = self.db_sess.query(ctbl) \
			.filter(ctbl.c.url == url)   \
			.count()
		return count

	def extractLinks(self, ctnt, mimetype, url):

		# No links in non-textual content.
		if not isinstance(ctnt, str):
			return
		if mimetype == "text/html":
			return self.extractHtml(ctnt, url)

		# Other file types?
		return []

	def extractHtml(self, content, url):
		soup = WebRequest.as_soup(content)
		links = common.util.urlFuncs.extractUrls(soup, url, truncate_fragment=True)

		# for link in links:
			# print(link)
		clinks = self.filterLinks(links)
		# print("Filtered:")
		# for link in clinks:
			# print(link)


		self.log.info("Found %s links, %s after filtering.", len(links), len(clinks))


		return clinks

	def generalLinkClean(self, link):
		if link.startswith("data:"):
			return None
		if link.startswith("clsid:"):
			return None
		if link.startswith("mailto:"):
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

			if common.util.urlFuncs.hasDuplicateSegments(link):
				continue

			ret.add(link)
		return ret

	def upsertResponseLinks(self, job, links):
		self.log.info("Updating database with response links")
		links           = set(links)
		orig_link_cnt   = len(links)
		links           = self.filterLinks(links)
		filter_link_cnt = len(links)

		self.log.info("Upserting %s links (%s filtered)" % (filter_link_cnt, orig_link_cnt-filter_link_cnt))

		new_starturl = job.starturl
		new_distance = job.distance+1

		# Priority decays with distance.
		# That basically results in breadth-first fetches.
		new_priority = job.priority+1


		if links:
			with self.db.redis_session_context() as redis:

				# Lookup all the URLs in redis
				havel = redis.mget(["raw_" + url for url in links])
				# for item, have in zip(links, havel):
				# 	print((item, have))

				old_cnt = len(links)

				links = [
						item
					for
						item, have
					in
						zip(links, havel)
					if
						(
								have
							and
								float(have) < (time.time() - hours(12))
						)
						or
							have is None
						]

				new_cnt = len(links)

				# Set all the new URLs
				with redis.pipeline(transaction=False) as pipe:
					for url in links:
						pipe.set("raw_" + url, time.time())
					pipe.execute()


				self.log.info("Redis upsert limit queue removed %s items (%s, %s)", old_cnt - new_cnt, old_cnt, new_cnt)



		linksd = RawArchiver.RawUrlUpserter.links_to_dicts(links, new_starturl, new_distance, new_priority)

		try:
			RawArchiver.RawUrlUpserter.do_link_batch_update_sess(self.log, self.db_sess, linksd)
		except Exception:
			# A barf here getting all the way out is a BIG ISSUE.
			print("ERROR")
			print("ERROR")
			print("ERROR")
			print("ERROR")
			print("ERROR")
			print("ERROR")
			print("ERROR")
			print("ERROR")
			print("ERROR")
			print("ERROR")
			print("ERROR")
			print("ERROR")
			print("ERROR")
			traceback.print_exc()
			print("ERROR")
			print("ERROR")
			raise

		with self.mon_con.pipeline() as pipe:
			pipe.incr('raw_plain_in_links',      count=orig_link_cnt)
			pipe.incr('raw_plain_filt_links',    count=filter_link_cnt)
			pipe.incr('raw_filtered_links',      count=len(links))
			pipe.incr('raw_upserted_links',      count=len(linksd))


	def fetch_job(self, job):

		# Don't dump old jobs that have been accidentally reset.
		if job.state == 'new':
			job.state = 'fetching'
			self.db_sess.commit()

		if job.state != 'fetching':
			self.db_sess.commit()
			self.log.info("Job not in expected state (state: %s).", job.state)
			return None


		module = RawArchiver.misc.getModuleForUrl(job.url)
		self.log.info("Fetching %s", job.url)
		should_continue = module.check_prefetch(job.url, self.wg)
		if not should_continue:
			self.log.error("Prefetch check returned unable to continue!")
			return None

		ctnt, fname, mimetype = self.get_file_name_mime(job.url)
		return ctnt, fname, mimetype

	def process_job(self, job, ctnt, fname, mimetype):

		module = RawArchiver.misc.getModuleForUrl(job.url)
		fname, ctnt, mimetype = module.check_postfetch(job.url, self.wg, fname, ctnt, mimetype)
		links = self.extractLinks(ctnt, mimetype, job.url)

		if isinstance(ctnt, str):
			ctnt = ctnt.encode("utf-8")
		saved_to = saveFile(ctnt, job.url, fname)

		self.log.info("Saved file to path: %s", saved_to)

		interval = RawArchiver.misc.getModuleForUrl(job.url).rewalk_interval

		assert interval > 7
		ignoreuntiltime = (datetime.datetime.now() + datetime.timedelta(days=interval))


		while True:
			history_size = self.checkHaveHistory(job.url)
			if history_size > 0:
				break
			try:
				self.log.info("Need to push content into history table (current length: %s).", history_size)
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

		if links:
			self.upsertResponseLinks(job, links)

	# Update the row with the item contents
	def do_local_job(self, job):
		ctnt, fname, mimetype = self.fetch_job(job)
		self.process_job(job, ctnt, fname, mimetype)

	def do_remote_job(self, response):
		jid = response['jobid']
		job = self.get_job_from_id(jid)
		if not job:
			self.log.error("Missing job for jobid!")
			self.log.error("Job data: '%s'", response)
			self.log.info("Missing jobid: '%s'", jid)
			return



		if 'ret' in response and 'success' in response and response['success'] is True:
			assert 'module' in response, "No module in response message? Response: %s" % response
			assert 'call' in response, "No call in response message? Response: %s" % response

			assert response['module'] == 'WebRequest', "Incorrect module? Module: '%s'" % response['module']
			assert response['call'] == 'getItem', "Incorrect call? Call: '%s'" % response['call']
			content, fileN, mType = response['ret']
			self.process_job(job, content, fileN, mType)

		else:
			job.ignoreuntiltime = datetime.datetime.now() + datetime.timedelta(days=7)
			job.state = 'error'
			job.errno = -4

			content = "DOWNLOAD FAILED"
			content += "<br>"
			if 'traceback' in response:
				content += "<pre>"
				content += "<br>".join(response['traceback'])
				content += "</pre>"

				log_func = self.log.error

				if '<FetchFailureError 410 -> ' in content:
					job.ignoreuntiltime = datetime.datetime.now() + datetime.timedelta(days=365)
					log_func = self.log.warning
					job.errno = 410
				elif '<FetchFailureError 404 -> ' in content:
					job.ignoreuntiltime = datetime.datetime.now() + datetime.timedelta(days=365)
					log_func = self.log.warning
					job.errno = 404
				elif '<FetchFailureError 403 -> ' in content:
					job.ignoreuntiltime = datetime.datetime.now() + datetime.timedelta(days=60)
					job.errno = 403
				elif '<FetchFailureError 500 -> ' in content:
					job.ignoreuntiltime = datetime.datetime.now() + datetime.timedelta(days=60)
					job.errno = 500
				else:
					job.ignoreuntiltime = datetime.datetime.now() + datetime.timedelta(days=30)
					job.errno = -1

				max_len_trunc = 450

				for line in response['traceback']:
					if len(line) > max_len_trunc:
						log_func("Remote traceback: %s [...snip...]", line[:max_len_trunc])
					else:
						log_func("Remote traceback: %s", line)
			else:
				self.log.error("No traceback in response?")
				self.log.error("Response: %s", response)

			self.db_sess.commit()
			self.log.error("Error in remote fetch.")







		# {
		#     'jobmeta': {
		#         'sort_key': 'c236292689e611e6b17900163ef6fe07'
		#     },
		#     'extradat': {
		#         'mode': 'fetch'
		#     },
		#     'ret': ['<html>', '', 'text/html'],
		#     'dispatch_key': 'fetcher',
		#     'jobid': 16632,
		#     'cancontinue': True,
		#     'user': 'scrape-worker-2',
		#     'success': True,
		#     'module': 'WebRequest',
		#     'call': 'getItem'
		# }

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
		self.db_sess.commit()
		job = self.db_sess.query(self.db.RawWebPages) \
			.filter(self.db.RawWebPages.id == jobid)    \
			.scalar()
		self.db_sess.commit()

		if not job:
			return False

		return job


	def taskProcess(self):
		'''
		Return true if there was something to do, false if not.
		'''
		job = None
		try:

			if runStatus.run_state.value == 1:
				try:
					mode, data = self.new_job_queue.get_nowait()

					if mode == 'processed':
						self.do_remote_job(data)
					elif mode == 'unfetched':
						jobid = data
						job = self.get_job_from_id(jobid)
						if job and RawArchiver.misc.thread_affinity(job.url, self.total_worker_count) == self.worker_num:
							try:
								self.do_local_job(job)
							except Exception:
								while True:
									try:
										job.state = 'error'
										self.db_sess.commit()
										self.log.info("Pushing old job content into history table!")
										break
									except sqlalchemy.exc.OperationalError:
										self.db_sess.rollback()
									except sqlalchemy.exc.InvalidRequestError:
										self.db_sess.rollback()
								raise

							return True
						else:
							self.new_job_queue.put((mode, jobid))
							return False
				except queue.Empty:
					return False

		except Exception:
			for line in traceback.format_exc().split("\n"):
				self.log.critical("%s", line.rstrip())
		return True



def test():

	import common.database
	sess = common.database.get_db_session()


	try:

		job = common.database.RawWebPages(
			state    = 'new',
			url      = 'http://somethingpositive.net',
			starturl = 'http://somethingpositive.net',
			netloc   = 'somethingpositive.net',
			priority = common.database.DB_LOW_PRIORITY,
			distance = 0,
			)
		sess.add(job)
		sess.commit()

	except sqlalchemy.exc.IntegrityError:
		sess.rollback()
		r = sess.query(common.database.RawWebPages) \
			.filter(common.database.RawWebPages.url == 'http://somethingpositive.net') \
			.update({'state' : 'new', 'ignoreuntiltime' : datetime.datetime.min })
		sess.commit()
		print("Did update?")
		print(r)

		job = sess.query(common.database.RawWebPages) \
			.filter(common.database.RawWebPages.url == 'http://somethingpositive.net').one()


	archiver = RawSiteArchiver(total_worker_count=1, worker_num=0, new_job_queue=None, cookie_lock=None, response_queue=None, db_interface=sess, db=common.database)

	print(job)
	archiver.do_local_job(job)
	print("doing")

	pass


def test2():
	fetcher = RawArchiver.RawJobDispatcher.RawJobFetcher()
	sess = common.database.get_db_session()

	try:

		job = common.database.RawWebPages(
			state    = 'new',
			url      = 'http://somethingpositive.net',
			starturl = 'http://somethingpositive.net',
			netloc   = 'somethingpositive.net',
			priority = common.database.DB_LOW_PRIORITY,
			distance = 0,
			)
		sess.add(job)
		sess.commit()

	except sqlalchemy.exc.IntegrityError:
		sess.rollback()
		r = sess.query(common.database.RawWebPages) \
			.filter(common.database.RawWebPages.url == 'http://somethingpositive.net') \
			.update({'state' : 'new', 'ignoreuntiltime' : datetime.datetime.min })
		sess.commit()
		print("Did update?")
		print(r)


	archiver = RawSiteArchiver(total_worker_count=1, worker_num=0, new_job_queue=fetcher.get_queue(), cookie_lock=None, response_queue=None, db_interface=sess, db=common.database)
	archiver.taskProcess()


def test3():
	in_paths = [
		]
	for in_path in in_paths:
		ret = create_dir_ignoring_files(in_path)

		print("Resolved out to path %s" % ret)

if __name__ == "__main__":
	# resetInProgress()
	# test()
	# test2()
	test3()



