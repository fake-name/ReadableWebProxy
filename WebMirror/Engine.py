

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import WebMirror.rules
import WebMirror.LogBase as LogBase
import runStatus
import time
import os.path
import os
import sys
import sqlalchemy.exc

from sqlalchemy import desc

import WebMirror.util.urlFuncs
import urllib.parse
import traceback
import datetime

from sqlalchemy.sql import text
import WebMirror.util.webFunctions as webFunctions

import hashlib
from WebMirror.Fetch import DownloadException
import WebMirror.Fetch
import WebMirror.database as db
from config import C_RESOURCE_DIR

if "debug" in sys.argv:
	CACHE_DURATION = 1
	RSC_CACHE_DURATION = 1
	# CACHE_DURATION = 60 * 5
	# RSC_CACHE_DURATION = 60 * 60 * 5
else:
	CACHE_DURATION = 60 * 60 * 24 * 7
	RSC_CACHE_DURATION = 60 * 60 * 24 * 14



GLOBAL_BAD = [
			'/xmlrpc.php',
			'gprofiles.js',
			'netvibes.com',
			'accounts.google.com',
			'edit.yahoo.com',
			'add.my.yahoo.com',
			'public-api.wordpress.com',
			'r-login.wordpress.com',
			'twitter.com',
			'facebook.com',
			'public-api.wordpress.com',
			'wretch.cc',
			'ws-na.amazon-adsystem.com',
			'delicious.com',
			'paypal.com',
			'digg.com',
			'topwebfiction.com',
			'/page/page/',
			'addtoany.com',
			'stumbleupon.com',
			'delicious.com',
			'/comments/feed/',
			'fbcdn-',
			'reddit.com',
			'/osd.xml',
			'/wp-login.php',
			'?openidserver=1',
			'newsgator.com',
			'technorati.com',
			'pixel.wp.com',
			'a.wikia-beacon.com',
			'b.scorecardresearch.com',
			'//mail.google.com',
			'javascript:void',
	]



def getHash(fCont):

	m = hashlib.md5()
	m.update(fCont)
	return m.hexdigest()




def saveCoverFile(filecont, fHash, filename):
	# use the first 3 chars of the hash for the folder name.
	# Since it's hex-encoded, that gives us a max of 2^12 bits of
	# directories, or 4096 dirs.
	fHash = fHash.upper()
	dirName = fHash[:3]

	dirPath = os.path.join(C_RESOURCE_DIR, dirName)
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
	confpath = os.path.abspath(C_RESOURCE_DIR)

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


class SiteArchiver(LogBase.LoggerMixin):


	loggerPath = "Main.SiteArchiver"



	# Fetch items up to 1,000,000 (1 million) links away from the root source
	# This (functionally) equates to no limit.
	# The db defaults to  (e.g. max signed integer value) anyways
	FETCH_DISTANCE = 1000 * 1000

	def __init__(self, cookie_lock, run_filters=True):
		print("SiteArchiver __init__()")
		super().__init__()

		self.db = db

		self.cookie_lock = cookie_lock

		# print("SiteArchiver database imported")
		ruleset = WebMirror.rules.load_rules()
		self.ruleset = ruleset
		self.fetcher = WebMirror.Fetch.ItemFetcher
		self.wg = webFunctions.WebGetRobust(cookie_lock=cookie_lock)
		# print("SiteArchiver rules loaded")
		self.relinkable = set()
		for item in ruleset:
			[self.relinkable.add(url) for url in item['fileDomains']]         #pylint: disable=W0106
			if item['netlocs'] != None:
				[self.relinkable.add(url) for url in item['netlocs']]             #pylint: disable=W0106


		self.ctnt_filters = {}
		self.rsc_filters  = {}


		for item in ruleset:

			if not item['netlocs']:
				continue

			for netloc in item['netlocs']:
				self.ctnt_filters[netloc] = item['netlocs']

			for netloc in item['fileDomains']:
				self.rsc_filters[netloc]  = item['fileDomains']

			# print("processing rsc")
			# print(item['fileDomains'])
			# rsc_vals  = self.buildUrlPermutations(item['fileDomains'], item['netlocs'])

		self.log.info("Content filter size: %s. Resource filter size %s.", len(self.ctnt_filters), len(self.rsc_filters))
		# print("SiteArchiver initializer complete")

	########################################################################################################################
	#
	#	########    ###     ######  ##    ##    ########  ####  ######  ########     ###    ########  ######  ##     ## ######## ########
	#	   ##      ## ##   ##    ## ##   ##     ##     ##  ##  ##    ## ##     ##   ## ##      ##    ##    ## ##     ## ##       ##     ##
	#	   ##     ##   ##  ##       ##  ##      ##     ##  ##  ##       ##     ##  ##   ##     ##    ##       ##     ## ##       ##     ##
	#	   ##    ##     ##  ######  #####       ##     ##  ##   ######  ########  ##     ##    ##    ##       ######### ######   ########
	#	   ##    #########       ## ##  ##      ##     ##  ##        ## ##        #########    ##    ##       ##     ## ##       ##   ##
	#	   ##    ##     ## ##    ## ##   ##     ##     ##  ##  ##    ## ##        ##     ##    ##    ##    ## ##     ## ##       ##    ##
	#	   ##    ##     ##  ######  ##    ##    ########  ####  ######  ##        ##     ##    ##     ######  ##     ## ######## ##     ##
	#
	########################################################################################################################

	# Minimal proxy because I want to be able to call the fetcher without affecting the DB.
	def fetch(self, job):
		fetcher = self.fetcher(self.ruleset, job.url, job.starturl, self.cookie_lock, wg_handle=self.wg)
		response = fetcher.fetch()
		return response

	# This is the main function that's called by the task management system.
	# Retreive remote content at `url`, call the appropriate handler for the
	# transferred content (e.g. is it an image/html page/binary file)
	def dispatchRequest(self, job):
		response = self.fetch(job)
		if "file" in response:
			# No title is present in a file response
			self.upsertFileResponse(job, response)
		elif 'rss-content' in response:
			self.upsertRssItems(response['rss-content'], job.url)
			self.upsertResponseLinks(job, plain=[entry['linkUrl'] for entry in response['rss-content']])

		else:
			self.upsertReponseContent(job, response)
			self.upsertResponseLinks(job, plain=response['plainLinks'], resource=response['rsrcLinks'])

		# Reset the fetch time download


	# Update the row with the item contents
	def upsertReponseContent(self, job, response):
		while 1:
			try:
				job.title    = response['title']
				job.content  = response['contents']
				job.mimetype = response['mimeType']
				if "text" in job.mimetype:
					job.is_text  = True
				else:
					job.is_text  = False

				job.state    = 'complete'

				if 'rawcontent' in response:
					job.raw_content = response['rawcontent']

				job.fetchtime = datetime.datetime.now()

				self.db.get_session().flush()
				self.db.get_session().commit()
				break
			except sqlalchemy.exc.OperationalError:
				self.db.get_session().rollback()
			except sqlalchemy.exc.InvalidRequestError:
				self.db.get_session().rollback()

	def insertRssItem(self, entry, feedurl):

		have = self.db.get_session().query(self.db.FeedItems) \
			.filter(self.db.FeedItems.contentid == entry['guid'])   \
			.limit(1)                                  \
			.scalar()



		if have:
			return
		else:
			assert ("srcname" in entry), "'srcname' not in entry for item from '%s' (contenturl: '%s', title: '%s', guid: '%s')" % (feedurl, entry['linkUrl'], entry['title'], entry['guid'])

			authors     = [tmp['name'] for tmp in entry['authors'] if 'name' in tmp]

			# Deduplicate repeat tags of the differing case.
			tags = {}
			for tag in entry['tags']:
				tags[tag.lower()] = tag

			new = self.db.FeedItems(
					contentid  = entry['guid'],
					title      = entry['title'],
					srcname    = entry['srcname'],
					feedurl    = feedurl,
					contenturl = entry['linkUrl'],

					type       = entry['feedtype'],
					contents   = entry['contents'],

					author     = authors,
					tags       = list(tags.values()),

					updated    = datetime.datetime.fromtimestamp(entry['updated']),
					published  = datetime.datetime.fromtimestamp(entry['published'])
				)

			self.db.get_session().add(new)
			self.db.get_session().commit()




	def upsertRssItems(self, entrylist, feedurl):
		# print("InsertFeed!")
		for feedentry in entrylist:
			# print(feedentry)
			# print(feedentry.keys())
			# print(feedentry['contents'])
			# print(feedentry['published'])


			while 1:
				try:
					self.insertRssItem(feedentry, feedurl)
					break

				except sqlalchemy.exc.InvalidRequestError:
					print("InvalidRequest error!")
					self.db.get_session().rollback()
					traceback.print_exc()
				except sqlalchemy.exc.OperationalError:
					print("InvalidRequest error!")
					self.db.get_session().rollback()
				except sqlalchemy.exc.IntegrityError:
					print("[upsertRssItems] -> Integrity error!")
					traceback.print_exc()
					self.db.get_session().rollback()


	# Todo: FIXME
	def filterContentLinks(self, job, links, badwords):
		ret = set()
		for link in links:
			if link.startswith("data:"):
				continue
			if any([item in link for item in badwords]):
				# print("Filtered:", link)
				continue
			netloc = urllib.parse.urlsplit(link).netloc
			if netloc in self.ctnt_filters and job.netloc in self.ctnt_filters[netloc]:
				# print("Valid content link: ", link)
				ret.add(link)

		return ret

	def filterResourceLinks(self, job, links, badwords):
		ret = set()
		for link in links:
			if link.startswith("data:"):
				continue
			if any([item in link for item in badwords]):
				# print("Filtered:", link)
				continue
			netloc = urllib.parse.urlsplit(link).netloc
			if netloc in self.rsc_filters:
				# print("Valid resource link: ", link)
				ret.add(link)
		return ret

	def getBadWords(self, job):
		badwords = GLOBAL_BAD
		for item in [rules for rules in self.ruleset if rules['netlocs'] and job.netloc in rules['netlocs']]:
			badwords += item['badwords']

		# A "None" can occationally crop up. Filter it.
		badwords = [badword for badword in badwords if badword]
		return badwords

	def upsertResponseLinks(self, job, plain=[], resource=[]):
		plain    = set(plain)
		resource = set(resource)

		unfiltered = len(plain)+len(resource)

		badwords = self.getBadWords(job)

		plain    = self.filterContentLinks(job,  plain,    badwords)
		resource = self.filterResourceLinks(job, resource, badwords)

		filtered = len(plain)+len(resource)
		self.log.info("Upserting %s links (%s filtered)" % (filtered, unfiltered))

		items = []
		[items.append((link, True))  for link in plain]
		[items.append((link, False)) for link in resource]

		self.log.info("Page had %s unfiltered content links, %s unfiltered resource links.", len(plain), len(resource))

		while 1:
			try:
				for link, istext in items:
					start = urllib.parse.urlsplit(link).netloc

					assert link.startswith("http")
					assert start

					new = {
						'url'       : link,
						'starturl'  : job.starturl,
						'netloc'    : start,
						'distance'  : job.distance+1,
						'is_text'   : istext,
						'priority'  : job.priority,
						'type'      : job.type,
						'state'     : "new",
						'fetchtime' : datetime.datetime.now(),
						}

					# Fucking huzzah for ON CONFLICT!
					cmd = text("""
							INSERT INTO
								web_pages
								(url, starturl, netloc, distance, is_text, priority, type, fetchtime, state)
							VALUES
								(:url, :starturl, :netloc, :distance, :is_text, :priority, :type, :fetchtime, :state)
							ON CONFLICT DO NOTHING
							""")
					self.db.get_session().execute(cmd, params=new)

				self.db.get_session().commit()
				break
			except sqlalchemy.exc.InternalError:
				self.log.info("Transaction error. Retrying.")
				self.db.get_session().rollback()
			except sqlalchemy.exc.OperationalError:
				self.log.info("Transaction error. Retrying.")
				self.db.get_session().rollback()

		self.log.info("Links upserted.")



	def upsertFileResponse(self, job, response):
		# Response dict structure:
		# {"file" : True, "url" : url, "mimeType" : mimeType, "fName" : fName, "content" : content}
		# print("File response!")
		# Yeah, I'm hashing twice in lots of cases. Bite me
		fHash = getHash(response['content'])


		# Look for existing files with the same MD5sum. If there are any, just point the new file at the
		# fsPath of the existing one, rather then creating a new file on-disk.

		have = self.db.get_session().query(self.db.WebFiles) \
			.filter(self.db.WebFiles.fhash == fHash)   \
			.limit(1)                                  \
			.scalar()

		if have:
			match = self.db.get_session().query(self.db.WebFiles)              \
				.filter(self.db.WebFiles.fhash == fHash)                \
				.filter(self.db.WebFiles.filename == response['fName']) \
				.limit(1)                                               \
				.scalar()
			if match:
				job.file = match.id
			else:
				new = self.db.WebFiles(
					filename = response['fName'],
					fhash    = fHash,
					fspath   = have.fspath,
					)
				self.db.get_session().add(new)
				self.db.get_session().commit()
				job.file = new.id
		else:
			savedpath = saveCoverFile(response['content'], fHash, response['fName'])
			new = self.db.WebFiles(
				filename = response['fName'],
				fhash    = fHash,
				fspath   = savedpath,
				)
			self.db.get_session().add(new)
			self.db.get_session().commit()
			job.file = new.id

		job.state     = 'complete'
		job.is_text   = False
		job.fetchtime = datetime.datetime.now()

		job.mimetype = response['mimeType']
		self.db.get_session().commit()

		# print("have:", have)




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




	def getTask(self):
		'''
		Get a job row item from the database.

		Also updates the row to be in the "fetching" state.
		'''
		# self.db.get_session().begin()

		# Try to get a task untill we are explicitly out of tasks,
		# or we succeed.
		while 1:
			try:
				query = self.db.get_session().query(self.db.WebPages)         \
					.filter(self.db.WebPages.state == "new")            \
					.filter(self.db.WebPages.distance < (self.db.MAX_DISTANCE)) \
					.order_by(self.db.WebPages.priority)                \
					.limit(1)

					# This compound order_by completely, COMPLETELY tanked the
					# time of this query. As it was, it took > 2 seconds per query!
					# .order_by(desc(self.db.WebPages.is_text))           \
					# .order_by(desc(self.db.WebPages.addtime))           \
					# .order_by(self.db.WebPages.distance)                \
					# .order_by(self.db.WebPages.url)                     \

				job = query.scalar()
				if not job:
					self.db.get_session().flush()
					self.db.get_session().commit()
					return False

				if job.state != "new":
					raise ValueError("Wat?")
				job.state = "fetching"

				self.db.get_session().flush()
				self.db.get_session().commit()
				return job
			except sqlalchemy.exc.OperationalError:
				self.db.get_session().rollback()
			except sqlalchemy.exc.InvalidRequestError:
				self.db.get_session().rollback()



	def taskProcess(self):

		job = self.getTask()
		if job:
			try:
				self.dispatchRequest(job)
			except urllib.error.URLError:
				content = "DOWNLOAD FAILED - urllib URLError"
				content += "<br>"
				content += traceback.format_exc()
				job.content = content
				job.raw_content = content
				job.state = 'error'
				job.errno = -1
				self.db.get_session().commit()
				self.log.error("`urllib.error.URLError` Exception when downloading.")
			except ValueError:
				content = "DOWNLOAD FAILED - ValueError"
				content += "<br>"
				content += traceback.format_exc()
				job.content = content
				job.raw_content = content
				job.state = 'error'
				job.errno = -3
				self.db.get_session().commit()
			except DownloadException:
				content = "DOWNLOAD FAILED - DownloadException"
				content += "<br>"
				content += traceback.format_exc()
				job.content = content
				job.raw_content = content
				job.state = 'error'
				job.errno = -2
				self.db.get_session().commit()
				self.log.error("`DownloadException` Exception when downloading.")
			except KeyboardInterrupt:
				runStatus.run = False
				runStatus.run_state.value = 0
				print("Keyboard Interrupt!")

		else:
			time.sleep(5)


	def synchronousJobRequest(self, url, ignore_cache=False):
		"""
		trigger an immediate, synchronous dispatch of a job for url `url`,
		and return the fetched row upon completion

		"""
		self.log.info("Manually initiated request for content at '%s'", url)

		# Rather then trying to add, and rolling back if it exists,
		# just do a simple check for the row first. That'll
		# probably be faster in the /great/ majority of cases.
		while 1:
			# self.db.get_session().begin()
			try:
				row =  self.db.get_session().query(self.db.WebPages) \
					.filter(self.db.WebPages.url == url)       \
					.scalar()

				self.db.get_session().commit()
				break
			except sqlalchemy.exc.InvalidRequestError:
				self.db.get_session().rollback()


		if row:
			self.log.info("Item already exists in database.")
		else:
			self.log.info("Row does not exist in DB")
			start = urllib.parse.urlsplit(url).netloc

			# New jobs are inserted in the "fetching" state since we
			# don't want them to be picked up by the fetch engine
			# while they're still in-progress
			row = self.db.WebPages(
				state     = 'fetching',
				url       = url,
				starturl  = url,
				netloc    = start,
				distance  = self.db.MAX_DISTANCE-2,
				is_text   = True,
				priority  = self.db.DB_REALTIME_PRIORITY,
				type      = "unknown",
				fetchtime = datetime.datetime.now(),
				)

			# Because we can have parallel operations happening here, we spin on adding&committing the new
			# row untill the commit either succeeds, or we get an integrity error, and then successfully
			# fetch the row inserted by another thread at the same time.
			while 1:
				try:
					# self.db.get_session().begin()
					self.db.get_session().add(row)
					self.db.get_session().commit()
					print("Row added?")
					break
				except sqlalchemy.exc.InvalidRequestError:
					print("InvalidRequest error!")
					self.db.get_session().rollback()
					traceback.print_exc()
				except sqlalchemy.exc.OperationalError:
					print("InvalidRequest error!")
					self.db.get_session().rollback()
				except sqlalchemy.exc.IntegrityError:
					print("[synchronousJobRequest] -> Integrity error!")
					self.db.get_session().rollback()
					row =  query = self.db.get_session().query(self.db.WebPages) \
						.filter(self.db.WebPages.url == url)               \
						.one()
					self.db.get_session().commit()
					break

		thresh_text_ago = datetime.datetime.now() - datetime.timedelta(seconds=CACHE_DURATION)
		thresh_bin_ago  = datetime.datetime.now() - datetime.timedelta(seconds=RSC_CACHE_DURATION)

		# print("now                             ", datetime.datetime.now())
		# print("row.fetchtime                   ", row.fetchtime)
		# print("thresh_text_ago                 ", thresh_text_ago)
		# print("thresh_bin_ago                  ", thresh_bin_ago)
		# print("row.fetchtime > thresh_text_ago ", row.fetchtime > thresh_text_ago)
		# print("row.fetchtime > thresh_bin_ago  ", row.fetchtime > thresh_bin_ago)

		if ignore_cache:
			self.log.info("Cache ignored due to override")
		else:
			if row.state == "complete" and row.fetchtime > thresh_text_ago:
				self.log.info("Using cached fetch results as content was retreived within the last %s seconds.", RSC_CACHE_DURATION)
				return row
			elif row.state == "complete" and row.fetchtime > thresh_bin_ago and "text" not in row.mimetype.lower():
				self.log.info("Using cached fetch results as content was retreived within the last %s seconds.", CACHE_DURATION)
				return row
			else:
				self.log.info("Item has exceeded cache time by text: %s, rsc: %s. (fetchtime: %s) Re-acquiring.", thresh_text_ago, thresh_bin_ago, row.fetchtime)

		row.state     = 'new'
		row.distance  = self.db.MAX_DISTANCE-2
		row.priority  = self.db.DB_REALTIME_PRIORITY

		# dispatchRequest modifies the row contents directly.
		self.dispatchRequest(row)

		# Commit, because why not
		self.db.get_session().commit()

		return row


def test():
	archiver = SiteArchiver(None)

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
	ins = archiver.db.get_session().execute(cmd, params=new)
	print("Done. Ret:")
	print(ins)
	# print(archiver.resetDlstate())
	# print(archiver.getTask())
	# print(archiver.getTask())
	# print(archiver.getTask())
	# print(archiver.taskProcess())
	pass

if __name__ == "__main__":
	test()


