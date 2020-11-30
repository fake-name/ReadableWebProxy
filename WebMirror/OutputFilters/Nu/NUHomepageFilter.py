
import time
import random


import WebMirror.OutputFilters.FilterBase

import common.database as db

import WebMirror.OutputFilters.util.MessageConstructors  as msgpackers
from WebMirror.OutputFilters.util.TitleParsers import extractTitle
from WebMirror.OutputFilters.util.TitleParsers import title_from_html

from . import NUBaseFilter

import sqlalchemy.exc
import bs4
import re
import calendar
import traceback
import datetime
import time
import json
import cssutils
import WebRequest
import parsedatetime
import common.util.urlFuncs

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



# Convenience functions to make intervals clearer.
def days(num):
	return 60*60*24*num
def hours(num):
	return 60*60*num
def minutes(num):
	return 60*num


class NuHomepageFilter(NUBaseFilter.NuBaseFilter):


	wanted_mimetypes = ['text/html']
	want_priority    = 95

	loggerPath = "Main.Text.NUHpProc"
	statsd_prefix = 'ReadableWebProxy.Nu.PageProcessor'


	@staticmethod
	def wantsUrl(url):
		if re.search(r"^https?://(?:www\.)?novelupdates\.com/?(?:\?pg=\d+)?$", url):
			print("NovelUpdates Homepage filter Wants url: '%s'" % url)
			return True

		return False


	def __init__(self, **kwargs):

		self.kwargs     = kwargs


		self.pageUrl    = kwargs['pageUrl']

		self.content    = kwargs['pgContent']
		self.type       = kwargs['type']
		self.db_sess    = kwargs['db_sess']

		# Don't do AMQP
		self._needs_amqp = False

		self.log.info("Processing NovelUpdates Homepage!")
		super().__init__(**kwargs)



	def __load_referrer(self, base_url, item):

		if any([tmp.client_id == 'local' for tmp in item.resolved]):
			return


		# Don't dewaf
		old_autowaf = self.kwargs['wg_proxy']().rules['auto_waf']
		self.kwargs['wg_proxy']().rules['auto_waf'] = False
		content, name, mime, url = self.kwargs['wg_proxy']().getFileNameMimeUrl(item.outbound_wrapper, addlHeaders={'Referer': base_url})
		self.kwargs['wg_proxy']().rules['auto_waf'] = old_autowaf

		if url.startswith("https://www.novelupdates.com/extnu/"):
			raise RuntimeError("Failure when extracting NU referrer!")

		item.validated     = True
		item.validated_on  = datetime.datetime.now()
		item.actual_target = url
		item.reviewed      = "manual_validate"

		pg_title = title_from_html(content)

		new = db.NuResolvedOutbound(
				client_id      = "local",
				client_key     = "local",
				actual_target  = url,
				resolved_title = pg_title,
				fetched_on     = datetime.datetime.now(),
			)

		item.resolved.append(new)
		self.db_sess.commit()


		self.log.info("TL Group: %s. Series %s, chap: %s", item.groupinfo, item.seriesname, item.releaseinfo)
		self.log.info("URL '%s' resolved to '%s'", item.outbound_wrapper, item.actual_target)
		self.log.info("Page title: '%s'", pg_title)
		sleep = random.triangular(3,10,30)
		self.log.info("Sleeping %s", sleep)
		time.sleep(sleep)

	def __addNewLinks(self, base_url, link_items):

		'''
		Example release sections:
		{
		    'seriesname': 'Gate of Revelation',
		    'releaseinfo': 'c203',
		    'groupinfo': 'daoseekerblog',
		    'referrer': 'https://www.novelupdates.com/',
		    'outbound_wrapper': 'https://www.novelupdates.com/extnu/327682/',
		    'actual_target': None
		}, {
		    'seriesname': 'Mai Kitsune Waifu',
		    'releaseinfo': 'c174',
		    'groupinfo': 'subudai11',
		    'referrer': 'https://www.novelupdates.com/',
		    'outbound_wrapper': 'https://www.novelupdates.com/extnu/327678/',
		    'actual_target': None
		}, {
		    'seriesname': 'Mai Kitsune Waifu',
		    'releaseinfo': 'c174',
		    'groupinfo': 'subudai11',
		    'referrer': 'https://www.novelupdates.com/',
		    'outbound_wrapper': 'https://www.novelupdates.com/extnu/327674/',
		    'actual_target': None
		}
		'''

		commit_each = False
		while 1:
			try:
				new_count = 0
				for item in link_items:
					have = self.db_sess.query(db.NuReleaseItem)                                     \
						.filter(db.NuReleaseItem.outbound_wrapper==item['outbound_wrapper']) \
						.scalar()

					if not have:
						self.log.info("New: '%s' -> '%s' : '%s'", item['seriesname'], item['releaseinfo'], item['groupinfo'])
						have = db.NuReleaseItem(
								validated            = False,
								reviewed             = 'unverified',
								seriesname           = item['seriesname'].strip(),
								releaseinfo          = item['releaseinfo'].strip(),
								groupinfo            = item['groupinfo'].strip(),
								referrer             = item['referrer'],
								outbound_wrapper     = item['outbound_wrapper'],
								first_seen           = datetime.datetime.now(),
								release_date         = item['release_date'],
								fetch_attempts       = 0,
								local_fetch_attempts = 0,
							)
						self.db_sess.add(have)
						new_count += 1
						if commit_each:
							self.db_sess.commit()

						self.mon_con.incr('new-urls', 1)
					else:
						delta = have.release_date - item['release_date']
						if delta.total_seconds() > days(2):
							self.log.info("Item release date looks invalid. Fixing (%s, %s)", delta, delta.total_seconds())
							have.release_date = item['release_date']
							if commit_each:
								self.db_sess.commit()


					# This shouldn't happen given the default value, but it is. Not sure how.
					try:
						int(have.local_fetch_attempts)
					except:
						have.local_fetch_attempts = 0

					if have.reviewed == 'unverified' and have.fetch_attempts == 0 and have.local_fetch_attempts <= 2:
						try:
							self.__load_referrer(base_url, have)
						except Exception as e:

							self.log.info("Failure resolving item for '%s'", have.outbound_wrapper)
							self.log.info("TL Group: %s. Series %s, chap: %s", have.groupinfo, have.seriesname, have.releaseinfo)
							for line in traceback.format_exc().strip().split("\n"):
								self.log.error("%s", line.rstrip())

							have.local_fetch_attempts += 1

							try:
								self.log.warning("Rolling back")
								self.db_sess.rollback()
							except Exception as e:
								self.log.critical("Failure in rollback for '%s'", have.outbound_wrapper)
								for line in traceback.format_exc().strip().split("\n"):
									self.log.error("%s", line.rstrip())
								pass


				self.db_sess.commit()
				break

			except (sqlalchemy.exc.InvalidRequestError, sqlalchemy.exc.OperationalError, sqlalchemy.exc.IntegrityError):
				if commit_each == False:
					lfunc = self.log.warning
				else:
					lfunc = self.log.error

				lfunc("Error when inserting items!")
				if not commit_each:
					lfunc("Retrying with commit_each")
				if commit_each:
					for line in traceback.format_exc().strip().split("\n"):
						lfunc("%s", line.rstrip())
				self.db_sess.rollback()
				commit_each = True

		self.log.info("Found %s release links on page, %s of which were new!", len(link_items), new_count)



	def extractSeriesReleases(self, currentUrl, soup):

		container = soup.find('div', class_='l-content')

		assert container is not None

		masked_classes = self.getMaskedClasses(soup)

		release_tables = container.find_all('table', class_='tablesorter')

		current_date = datetime.datetime.now()

		ref_pages = set()
		releases = []
		for table_div in release_tables:

			date_tag = table_div.find_previous_sibling("b")
			if date_tag:
				time_struct, status = parsedatetime.Calendar().parse(date_tag.get_text(strip=True))
				if status:
					current_date = datetime.datetime(*time_struct[:6])

			for item in table_div.find_all("tr"):
				tds = item.find_all('td')
				if len(tds) == 3:
					series, release, group = tds
					referrer = series.a['href']

					assert not (referrer == "https://www.novelupdates.com" or
						referrer == "https://www.novelupdates.com" or
						referrer == "https://www.novelupdates.com/" or
						referrer == "https://www.novelupdates.com/")

					linkas = release.find_all('a', class_='chp-release')

					try:
						sname = series.a['title'].strip()
						gname = group.a['title'].strip()
					except Exception:
						sname = series.get_text().strip()
						gname = group.get_text().strip()

					for link in linkas:
						bad = any([tmp in masked_classes for tmp in link['class']])
						if not bad:
							# self.log.info("Using %s for referrer for %s -> %s -> %s, %s, %s", referrer, sname, gname, link.get_text().strip(), link['class'], bad)
							# self.log.info("Intermediate URL: %s", link['href'])

							linkfq = link['href']
							if linkfq.startswith("//"):
								linkfq = "https:"+linkfq
							if "http://" in linkfq:
								linkfq = linkfq.split("http://")[0]

							release = {
								'seriesname'       : sname,
								'releaseinfo'      : link.get_text().strip(),
								'groupinfo'        : gname,
								'referrer'         : referrer,
								'outbound_wrapper' : linkfq,
								'release_date'     : current_date,
								'actual_target'    : None,
							}

							# Don't bother triggering qidian stuff, I track that better externally.
							if 'Qidian International' not in gname and "Webnovel" not in gname:
								releases.append(release)

							ref_pages.add(referrer)


		return ref_pages, releases


	def processPage(self, url, content):
		soup = WebRequest.as_soup(self.content)
		ref_pages, releases = self.extractSeriesReleases(self.pageUrl, soup)

		if ref_pages:
			self.high_priority_links_trigger(ref_pages)

		if releases:
			self.__addNewLinks(url, releases)
			# self.retrigger_pages(releases)



	def extractContent(self):
		# print("Call to extract!")
		# print(self.amqpint)

		self.processPage(self.pageUrl, self.content)


def reset_homepages():
	import tqdm
	import common.database as db

	sess = db.get_db_session()
	for pageno in tqdm.trange(1, 1001):
		url = "https://www.novelupdates.com/?pg=%d" % pageno
		have = sess.query(db.WebPages)                                     \
			.filter(db.WebPages.url==url) \
			.scalar()

		if have:
			have.state = 'new'
			have.epoch = 0
			sess.commit()




if __name__ == "__main__":
	print("Test mode!")
	import logSetup
	import multiprocessing
	logSetup.initLogging()
	reset_homepages()

