

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import WebMirror.rules
import WebMirror.LogBase as LogBase
import runStatus
import time

import sqlalchemy.exc

from sqlalchemy import desc

import WebMirror.util.urlFuncs
import urllib.parse
import traceback
import datetime

import hashlib
import WebMirror.Fetch

MAX_DISTANCE = 1000 * 1000
# CACHE_DURATION = 60 * 5
CACHE_DURATION = 1

# import sql.operators as sqlo

# import TextScrape.urlFuncs
# import inspect
# import collections
# import queue
# import bs4
# from concurrent.futures import ThreadPoolExecutor


# import os.path
# import os

class DownloadException(Exception):
	pass


def getHash(fCont):

	m = hashlib.md5()
	m.update(fCont)
	return m.hexdigest()


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

	threads = 2

	# Fetch items up to 1,000,000 (1 million) links away from the root source
	# This (functionally) equates to no limit.
	# The db defaults to  (e.g. max signed integer value) anyways
	FETCH_DISTANCE = 1000 * 1000

	def __init__(self):
		super().__init__()



		import WebMirror.database as db
		self.db = db

		ruleset = WebMirror.rules.load_rules()
		self.ruleset = ruleset
		self.fetcher = WebMirror.Fetch.ItemFetcher

		self.relinkable = set()
		for item in ruleset:
			[self.relinkable.add(url) for url in item['fileDomains']]         #pylint: disable=W0106
			if item['netlocs'] != None:
				[self.relinkable.add(url) for url in item['netlocs']]             #pylint: disable=W0106



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

	# This is the main function that's called by the task management system.
	# Retreive remote content at `url`, call the appropriate handler for the
	# transferred content (e.g. is it an image/html page/binary file)
	def dispatchRequest(self, job):
		fetcher = self.fetcher(self.ruleset, job)
		response = fetcher.fetch()

		if "file" in response:
			self.upsertFileResponse(job, response)
		else:
			self.upsertResponseLinks(job, response)


	def upsertResponseLinks(self, job, response):
		plain = set(response['plainLinks'])
		resource = set(response['rsrcLinks'])

		items = []
		[items.append((link, True))  for link in plain]
		[items.append((link, False)) for link in resource]

		newlinks = 0
		retriggerLinks = 0
		for link, istext in items:
			assert link.startswith("http")
			while 1:
				try:
					item = self.db.session.query(self.db.WebPages) \
						.filter(self.db.WebPages.url == link)      \
						.scalar()
					if item:
						if item.is_text:
							ago = datetime.datetime.now() - datetime.timedelta(hours = 24)
						else:
							ago = datetime.datetime.now() - datetime.timedelta(hours = 24*14)
						if job.fetchtime < ago:
							retriggerLinks += 1
							job.dlstate = "new"
					else:
						newlinks += 1
						start = urllib.parse.urlsplit(link).netloc
						assert start
						new = self.db.WebPages(
							url       = link,
							starturl  = job.starturl,
							netloc    = start,
							distance  = job.distance+1,
							is_text   = istext,
							priority  = job.priority,
							type      = job.type,
							fetchtime = datetime.datetime.now(),
							)
						self.db.session.add(new)
					break
				except sqlalchemy.exc.IntegrityError:
					self.db.session.rollback()
			self.db.session.commit()
		self.log.info("New links: %s, retriggered links: %s.", newlinks, retriggerLinks)



	def upsertFileResponse(self, job, response):
		# Response dict structure:
		# {"file" : True, "url" : url, "mimeType" : mimeType, "fName" : fName, "content" : content}

		# Yeah, I'm hashing twice in lots of cases. Bite me
		fHash = getHash(response['content'])


		# Look for existing files with the same MD5sum. If there are any, just point the new file at the
		# fsPath of the existing one, rather then creating a new file on-disk.

		have = self.db.session.query(self.db.WebFiles) \
			.filter(self.db.WebFiles.fhash == fHash)   \
			.limit(1)                                  \
			.scalar()
		print("have:", have)

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


	def resetDlstate(self):
		self.db.session.query(self.db.WebPages) \
			.filter((self.db.WebPages.state == "fetching") | (self.db.WebPages.state == "processing"))   \
			.update({self.db.WebPages.state : "new"})
		self.db.session.commit()


	def getTask(self):
		'''
		Get a job row item from the database.

		Also updates the row to be in the "fetching" state.
		'''
		query = self.db.session.query(self.db.WebPages)         \
			.filter(self.db.WebPages.state == "new")            \
			.filter(self.db.WebPages.distance < (MAX_DISTANCE)) \
			.order_by(self.db.WebPages.priority)                \
			.order_by(desc(self.db.WebPages.is_text))           \
			.order_by(desc(self.db.WebPages.addtime))           \
			.order_by(self.db.WebPages.distance)                \
			.order_by(self.db.WebPages.url)                     \
			.limit(1)

		job = query.scalar()
		if not job:
			return False

		job.state = "fetching"
		self.db.session.commit()

		return job


	def taskProcess(self):
		while runStatus.run:
			# runStatus.run = False
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
					self.log.error("`urllib.error.URLError` Exception when downloading.")
				except DownloadException:
					content = "DOWNLOAD FAILED - DownloadException"
					content += "<br>"
					content += traceback.format_exc()
					job.content = content
					job.raw_content = content
					job.state = 'error'
					job.errno = -2
					self.log.error("`DownloadException` Exception when downloading.")
				except KeyboardInterrupt:
					runStatus.run = False
					print("Keyboard Interrupt!")

			else:
				time.sleep(5)

		self.log.info("Task exiting.")

	def synchronousJobRequest(self, url):
		"""
		trigger an immediate, synchronous dispatch of a job for url `url`,
		and return the fetched row upon completion

		"""

		self.log.info("Manually initiated request for content at '%s'", url)
		start = urllib.parse.urlsplit(url).netloc

		row = self.db.WebPages(
			url       = url,
			starturl  = url,
			netloc    = start,
			distance  = MAX_DISTANCE-2,
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
				self.db.session.add(row)
				self.db.session.commit()
				break
			except sqlalchemy.exc.InvalidRequestError:
				self.db.session.rollback()
				self.db.session.add(row)
				self.db.session.commit()
			except sqlalchemy.exc.IntegrityError:
				self.db.session.rollback()
				row =  query = self.db.session.query(self.db.WebPages) \
					.filter(self.db.WebPages.url == url)               \
					.one()
				self.db.session.commit()
				break


		print()
		print("Row:")
		print(row)
		if row.state == "complete" and row.fetchtime > datetime.datetime.now() - datetime.timedelta(seconds=CACHE_DURATION):
			self.log.info("Using cached fetch results as content was retreived within the last %s seconds.", CACHE_DURATION)
			return row
		row.state     = 'new'
		row.distance  = MAX_DISTANCE-2
		row.priority  = self.db.DB_REALTIME_PRIORITY

		# dispatchRequest modifies the row contents directly.
		self.dispatchRequest(row)

		# Commit, because why not
		self.db.session.commit()

		return row


if __name__ == "__main__":

	archiver = SiteArchiver()
	print(archiver)
	print(archiver.resetDlstate())
	print(archiver.getTask())
	print(archiver.getTask())
	print(archiver.getTask())
	print(archiver.taskProcess())


