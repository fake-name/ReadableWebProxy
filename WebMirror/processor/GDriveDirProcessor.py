


import runStatus
runStatus.preloadDicts = False

# import Levenshtein as lv

import urllib.parse

import bs4
import copy
import readability.readability
import hashlib
import os.path

# import TextScrape.ProcessorBase
import WebMirror.processor.ProcessorBase as ProcessorBase


from . import gDocParse as gdp
import WebMirror.util.urlFuncs as urlFuncs

# import TextScrape.RELINKABLE as RELINKABLE
# import TextScrape.RelinkLookup


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




GLOBAL_BAD = [
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
			'reddit.com',
			'newsgator.com',
			'technorati.com',
	]

GLOBAL_DECOMPOSE_BEFORE = [
			{'name'     : 'likes-master'},  # Bullshit sharing widgets
			{'id'       : 'jp-post-flair'},
			{'class'    : 'post-share-buttons'},
			{'class'    : 'commentlist'},  # Scrub out the comments so we don't try to fetch links from them
			{'class'    : 'comments'},
			{'id'       : 'comments'},
		]

GLOBAL_DECOMPOSE_AFTER = []

class GDriveDirProcessor(ProcessorBase.PageProcessor):


	wanted_mimetypes = ['text/html']
	want_priority    = 91

	@staticmethod
	def wantsUrl(url):
		return urlFuncs.isGFileUrl(url)[0]

	loggerPath = "Main.Text.GDriveDirProcessor"

	def __init__(self, pageUrl, loggerPath, relinkable):
		self.loggerPath = loggerPath+".GDrvDirExtract"

		self.pageUrl  = pageUrl

		# We can be a bit lazy here, since google drive folders
		# can basically only contain google docs content.
		# As such, the extensive relinking system isn't warranted.

		self._relinkDomains = set()
		for url in relinkable:
			self._relinkDomains.add(url)


		self._scannedDomains = set()

		# Tell the path filtering mechanism that we can fetch google doc files
		# Not switchable, since not fetching google docs content from a google drive
		# item wouldn't work too well.
		self._scannedDomains.add('https://docs.google.com/document/')
		self._scannedDomains.add('https://docs.google.com/spreadsheets/')
		self._scannedDomains.add('https://drive.google.com/folderview')
		self._scannedDomains.add('https://drive.google.com/open')


	########################################################################################################################
	#
	#	 ######    #######   #######   ######   ##       ########         ########  ########  #### ##     ## ########
	#	##    ##  ##     ## ##     ## ##    ##  ##       ##               ##     ## ##     ##  ##  ##     ## ##
	#	##        ##     ## ##     ## ##        ##       ##               ##     ## ##     ##  ##  ##     ## ##
	#	##   #### ##     ## ##     ## ##   #### ##       ######           ##     ## ########   ##  ##     ## ######
	#	##    ##  ##     ## ##     ## ##    ##  ##       ##               ##     ## ##   ##    ##   ##   ##  ##
	#	##    ##  ##     ## ##     ## ##    ##  ##       ##               ##     ## ##    ##   ##    ## ##   ##
	#	 ######    #######   #######   ######   ######## ########         ########  ##     ## ####    ###    ########
	#
	########################################################################################################################



	def extractGoogleDriveFolder(self, driveUrl):
		'''
		Extract all the relevant links from a google drive directory, and push them into
		the queued URL queue.

		'''

		newLinks = []
		self.log.info("Fetching drive container page")
		docReferences, pgTitle = gdp.GDocExtractor.getDriveFileUrls(driveUrl)
		# print('docReferences', docReferences)
		for dummy_title, url in docReferences:
			url = gdp.trimGDocUrl(url)
			if url not in newLinks:
				newLinks.append(url)

		self.log.info("Generating google drive disambiguation page!")
		soup = gdp.makeDriveDisambiguation(docReferences, pgTitle)
		# print(disamb)

		soup = self.relink(soup)

		disamb = soup.prettify()

		ret = {}

		ret['contents']   = disamb
		ret['title']      = pgTitle
		ret['plainLinks'] = newLinks
		ret['rsrcLinks']  = []  # drive folders don't have resources


		self.log.info("Found %s items in google drive directory", len(docReferences))

		return ret



	def extractContent(self):
		return self.extractGoogleDriveFolder(self.pageUrl)




def test():
	print("Test mode!")
	import webFunctions
	import logSetup
	logSetup.initLogging()

	scraper = GDriveDirProcessor('https://drive.google.com/folderview?id=0B_mXfd95yvDfQWQ1ajNWZTJFRkk&usp=drive_web', 'Main.Test')
	print(scraper)
	extr = scraper.extractContent()
	print('Plain Links:')
	for link in extr['plainLinks']:
		print(link)
	print()
	print()
	print('Resource files:')
	for link in extr['rsrcLinks']:
		print(link)
	print(extr['contents'])


if __name__ == "__main__":
	test()

