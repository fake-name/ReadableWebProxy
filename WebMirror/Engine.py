

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import WebMirror.rules
import LogBase
import runStatus
import time

from sqlalchemy import desc

import WebMirror.util.urlFuncs
import urllib.parse
import traceback
import datetime
import sqlalchemy.exc

import WebMirror.Fetch

MAX_DISTANCE = 1000 * 1000

# import sql.operators as sqlo

# import TextScrape.urlFuncs
# import inspect
# import collections
# import queue
# import bs4
# from concurrent.futures import ThreadPoolExecutor


# import os.path
# import os

import TextScrape.gDocParse as gdp

class DownloadException(Exception):
	pass

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

		ruleset = WebMirror.rules.get_rules()
		self.ruleset = ruleset
		self.fetcher = WebMirror.Fetch.ItemFetcher

		self.relinkable = set()
		for item in ruleset:
			[self.relinkable.add(url) for url in item['fileDomains']]         #pylint: disable=W0106
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


# 	def queueLoop(self):
# 		self.log.info("Fetch thread starting")

# 		# Timeouts is used to track when queues are empty
# 		# Since I have multiple threads, and there are known
# 		# situations where we can be certain that there will be
# 		# only one request (such as at startup), we need to
# 		# have a mechanism for retrying fetches from a queue a few
# 		# times before concluding there is nothing left to do
# 		timeouts = 0
# 		while runStatus.run:
# 			try:
# 				newTodo = self.getToDo(self.FETCH_DISTANCE)
# 				if newTodo:
# 					url, distance = newTodo

# 					self.newLinkQueue.put(
# 							{
# 								'url'          : url,
# 								'isText'       : None,
# 								'distance'     : None,
# 								'shouldUpsert' : False
# 							}
# 						)

# 					try:
# 						self.dispatchRequest(url, distance)
# 					except urllib.error.URLError:
# 						content = "DOWNLOAD FAILED"
# 						content += "<br>"
# 						content += traceback.format_exc()
# 						self.upsert(url, dlstate=-1, contents=content, distance=distance)
# 						self.log.error("`urllib.error.URLError` Exception when downloading.")
# 					except DownloadException:
# 						content = "DOWNLOAD FAILED"
# 						content += "<br>"
# 						content += traceback.format_exc()
# 						self.upsert(url, dlstate=-1, contents=content, distance=distance)
# 						self.log.error("`DownloadException` Exception when downloading.")


# 				else:
# 					timeouts += 1
# 					time.sleep(1)
# 					self.log.info("Fetch task waiting for any potential items to flush to the DB.")

# 				if timeouts > 5:
# 					break

# 			except Exception:
# 				traceback.print_exc()
# 		self.log.info("Fetch thread exiting!")

# 	def crawl(self, shallow=False, checkOnly=False):

# 		self.resetStuckItems()

# 		if hasattr(self, 'preFlight'):
# 			self.preFlight()


# 		# Reset the dlstate on the starting URLs, so thing start up.
# 		haveUrls = set()

# 		if not checkOnly:
# 			if isinstance(self.startUrl, (list, set)):
# 				for url in self.startUrl:
# 					self.log.info("Start URL: '%s'", url)
# 					self.upsert(url, dlstate=0, distance=0, walklimit=-1)
# 			else:
# 				self.upsert(self.startUrl, dlstate=0, distance=0, walklimit=-1)

# 		# with self.transaction():
# 		# 	print('transaction test!')

# 		if shallow:
# 			self.FETCH_DISTANCE = 1


# 		with ThreadPoolExecutor(max_workers=self.threads) as executor:

# 			processes = []
# 			for dummy_x in range(self.threads):
# 				self.log.info("Starting child-thread!")
# 				processes.append(executor.submit(self.queueLoop))


# 			todoIntegrator = time.time()
# 			printInterval = 15  # Print items in queue every 10 seconds
# 			while runStatus.run:

# 				# Every 15 seconds, print how many items remain todo.
# 				if time.time() > (todoIntegrator + printInterval):
# 					self.log.info("Items remaining in todo queue: %s", self.getTodoCount())
# 					todoIntegrator += printInterval

# 				try:
# 					got = self.newLinkQueue.get_nowait()
# 					if not got:
# 						continue
# 					if len(got) == 4:
# 						if not got['url'] in haveUrls:

# 							if got['url'].lower().startswith('http'):
# 								self.log.info("New URL: '%s', distance: %s", got['url'], got['distance'])
# 								# Only reset the downloadstate for content, not
# 								# resources
# 								if got['shouldUpsert']:
# 									if got['isText']:
# 										self.upsert(got['url'], istext=got['isText'], dlstate=0, distance=got['distance'])
# 									else:
# 										self.upsert(got['url'], istext=got['isText'], distance=got['distance'])
# 								haveUrls.add(got['url'])
# 							else:
# 								raise ValueError("Invalid URL added: '%s'", got)
# 					else:
# 						raise ValueError("Data from queue is not a 4-dict? '%s'" % got)

# 				except queue.Empty:
# 					time.sleep(0.01)




# 				if not any([proc.running() for proc in processes]):
# 					self.log.info("All threads stopped. Main thread exiting.")
# 					break
# 			if not runStatus.run:
# 				self.log.warn("Execution stopped because of user-interrupt!")

# 		self.log.info("Crawler scanned a total of '%s' pages", len(haveUrls))
# 		self.log.info("Queue Feeder thread exiting!")


if __name__ == "__main__":

	archiver = SiteArchiver()
	print(archiver)
	print(archiver.resetDlstate())
	print(archiver.getTask())
	print(archiver.getTask())
	print(archiver.getTask())
	print(archiver.taskProcess())


