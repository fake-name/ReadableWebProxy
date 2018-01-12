

import bs4

import re
import io
import logging

import zipfile
import common.util.WebRequest
import mimetypes
import urllib.parse
import urllib.error

from . import jsLiteralParse
import common.util.urlFuncs as urlFuncs


class GDocExtractor(object):

	log = logging.getLogger("Main.Text.GDoc")
	wg = common.util.WebRequest.WebGetRobust(logPath="Main.GDoc.Web")

	def __init__(self, targetUrl):

		isGdoc, url = urlFuncs.isGdocUrl(targetUrl)
		if not isGdoc:
			raise ValueError("Passed URL '%s' is not a google document?" % targetUrl)

		url = urlFuncs.trimGDocUrl(url)
		self.url = url+'/export?format=zip'
		self.refererUrl = targetUrl

		self.document = ''

		self.currentChunk = ''

	@classmethod
	def getDriveFileUrls(cls, url):
		ctnt, handle = cls.wg.getpage(url, returnMultiple=True)

		# Pull out the title for the disambiguation page.
		soup = common.util.WebRequest.as_soup(ctnt)
		title = soup.title.string

		# Google drive supports a `read?{google doc path} mode. As such, we look at the actual URL,
		# which tells us if we redirected to a plain google doc, and just return that if the redirect occured.
		handleUrl = handle.geturl()
		if handleUrl != url:
			if urlFuncs.isGdocUrl(handleUrl):
				cls.log.info("Direct read redirect: '%s'", handleUrl)
				handleUrl = urlFuncs.trimGDocUrl(handleUrl)
				return [(title, handleUrl)], title

		jsRe = re.compile('var data = (.*?); _initFolderLandingPageApplication\(config, data\)', re.DOTALL)

		items = jsRe.findall(ctnt)
		assert len(items) == 1

		data = '{cont}'.format(cont=items.pop().strip())
		conf = jsLiteralParse.jsParse(data)

		# The keys+data in the data/conf are:
		# 'folderName'  - Title of the folder, just a string
		# 'viewerItems' - List of lists of the items in the folder, which contains the title, previewimage, and url for each item.
		# 				Other stuff (mime types) for the files, but they're all google internal mime-types and look to be the same for
		# 				Every file, even if they're different docs types.
		# 'folderModel' - List of UID and the view URL. Looks to be completely redundant, as all the information is also in 'viewerItems'

		assert 'viewerItems' in conf
		assert 'folderName' in conf

		title = conf['folderName']

		pages = conf['viewerItems']

		items = []
		for page in pages:
			if len(page) != 18 and len(page) != 22:
				cls.log.error("json entry in page with an invalid length:")
				cls.log.error("%s", page)
				continue


			# Item 2 is the title, item 17 is the doc URL
			# The doc URL is unicode escaped, annoyingly
			itemTitle = page[2]
			itemUrl   = page[17].encode('ascii').decode('unicode_escape')

			itemUrl = urlFuncs.trimGDocUrl(itemUrl)

			items.append((itemTitle, itemUrl))


		return items, title


	def extract(self):
		try:
			arch, fName = self.wg.getFileAndName(self.url, addlHeaders={'Referer': self.refererUrl})
		except IndexError:
			print("ERROR: Failure retrieving page!")
			return None, []

		baseName = fName.split(".")[0]

		if not isinstance(arch, bytes):
			if 'You need permission' in arch or 'Sign in to continue to Docs':
				self.log.critical("Retrieving zip archive failed?")
				self.log.critical("Retreived content type: '%s'", type(arch))
				raise TypeError("Cannot access document? Is it protected?")
			else:
				with open("tmp_page.html", "w") as fp:
					fp.write(arch)
				raise ValueError("Doc not valid?")

		zp = io.BytesIO(arch)
		zfp = zipfile.ZipFile(zp)

		resources = []
		baseFile = None

		for item in zfp.infolist():
			if not "/" in item.filename and not baseFile:
				contents = zfp.open(item).read()
				contents = bs4.UnicodeDammit(contents).unicode_markup

				baseFile = (item.filename, contents)

			elif baseName in item.filename and baseName:
				raise ValueError("Multiple base file items?")

			else:
				resources.append((item.filename, mimetypes.guess_type(item.filename)[0], zfp.open(item).read()))

		if not baseFile:
			raise ValueError("No base file found!")

		return baseFile, resources





class GFileExtractor(object):

	log = logging.getLogger("Main.Text.GFile")
	wg = common.util.WebRequest.WebGetRobust(logPath="Main.GFile.Web")

	def __init__(self, targetUrl):

		isGdoc, url = isGFileUrl(targetUrl)
		if not isGdoc:
			raise ValueError("Passed URL '%s' is not a google document?" % targetUrl)

		self.url = url
		self.refererUrl = url

		self.document = ''

		self.currentChunk = ''



	def getItem(self, itemUrl, addlHeaders=None):

		content, handle = self.wg.getpage(itemUrl, returnMultiple=True, addlHeaders={'Referer': self.refererUrl})
		if not content or not handle:
			raise ValueError("Failed to retreive file from page '%s'!" % itemUrl)



		info = handle.info()
		if not 'Content-Disposition' in info:
			info['Content-Disposition'] = ''

		fileN = jsLiteralParse.parseContentDispositon(info['Content-Disposition'], itemUrl)
		fileN = bs4.UnicodeDammit(fileN).unicode_markup

		mType = handle.info()['Content-Type']

		# If there is an encoding in the content-type (or any other info), strip it out.
		# We don't care about the encoding, since WebRequest will already have handled that,
		# and returned a decoded unicode object.

		if mType and ";" in mType:
			mType = mType.split(";")[0].strip()


		self.log.info("Retreived file of type '%s', name of '%s' with a size of %0.3f K", mType, fileN, len(content)/1000.0)
		return content, fileN, mType


	def extract(self):

		try:
			content = self.wg.getpage(self.url)
		except IndexError:
			print("ERROR: Failure retrieving page!")
			return None, None, None




		initRe = re.compile('_initProjector\((.*?)\)', re.DOTALL)

		pageConf = initRe.findall(content)
		if not pageConf:
			self.log.error('Could not find download JSON on google file page "%s"', self.url)
		conf = pageConf.pop()

		conf = jsLiteralParse.jsParse('[{cont}]'.format(cont=conf.strip()))

		# Verify the jsLiteral data structure is what we expect.
		metadata = conf[-1]
		assert len(metadata) == 32
		title = metadata[1]
		dlUrl = metadata[18]

		fileUrl = dlUrl.encode("ascii").decode('unicode-escape')


		try:
			file, fName, mType = self.getItem(fileUrl, addlHeaders={'Referer': self.refererUrl})
		except IndexError:
			self.log.error("ERROR: Failure retrieving page!")
			return None, None, None

		if title not in fName:
			fName = title + " " + fName



		# print(fName, type(file), mType)
		return file, fName, mType


def makeDriveDisambiguation(urls, pageHeader):

	soup = common.util.WebRequest.as_soup("")

	tag = soup.new_tag('h3')
	tag.string = 'Google Drive directory: %s' % pageHeader
	soup.append(tag)
	for title, url in urls:
		tag = soup.new_tag('a', href=url)
		tag.string = title
		soup.append(tag)
		tag = soup.new_tag('br')
		soup.append(tag)
	return soup


def test():
	import common.util.WebRequest
	wg = common.util.WebRequest.WebGetRobust()

	# url = 'https://docs.google.com/document/d/1ljoXDy-ti5N7ZYPbzDsj5kvYFl3lEWaJ1l3Lzv1cuuM/preview'
	# url = 'https://docs.google.com/document/d/17__cAhkFCT2rjOrJN1fK2lBdpQDSO0XtZBEvCzN5jH8/preview'
	url = 'https://docs.google.com/document/d/1t4_7X1QuhiH9m3M8sHUlblKsHDAGpEOwymLPTyCfHH0/preview'

	urls = [
		'https://docs.google.com/document/d/1RrLZ-j9uS5dJPXR44VLajWrGPJl34CVfAeJ7pELPMy4',
		'https://docs.google.com/document/d/1_1e7D30N16Q1Pw6q68iCrOGhHZNhXd3C9jDrRXbXCTc',
		'https://docs.google.com/document/d/1ke-eW78CApO0EgfY_X_ZgLyEEcEQ2fH8vK_oGbhROPM',
		'https://docs.google.com/document/d/1Dl5XbPHThX6xCxhIHL9oY0zDbIuQn6fXckXQ16rECps',
		'https://docs.google.com/document/d/12UHbPduKDVjSk99VVdf5OHdaHxzN3nuIcAGrW5oV5E8',
		'https://docs.google.com/document/d/1ebJOszL08TqJw1VvyaVfO72On4rQBPca6CujSYy-McY',
		'https://docs.google.com/document/d/19vXfdmkAyLWcfV2BkgIxNawD2QwCoeFEQtV8wYwTamU',
		'https://docs.google.com/document/d/1RGqoPR6sfjJY_ZxLfQGa4YLNIW5zKj1HTWa6qmFLQfg',
		'https://docs.google.com/document/d/1TDmwoB6Y7XiPJRZ7-OGjAhEqPPbdasazn0vBbCvj8IM',
		'https://docs.google.com/document/d/1o40vXZAW6v81NlNl4o6Jvjch0GO2ETv5JgwKqXfOpOQ',
		'https://docs.google.com/document/d/1STcAhI6J9CEEx7nQFGAt_mnxfgo0fMOrb4Ls0EYWRHk',
		'https://docs.google.com/document/d/1xyyhV5yeoRTZHPCPX6yeL8BbVzybhFM27EyInFtjwZQ',
		'https://docs.google.com/document/d/11RzD2ILc1MKH5VA4jBzCDO7DIFRzUFCjAe7-MnJfDLY',
		'https://docs.google.com/document/d/1AVyCN0nXTTqVrrMaqJRUSkTP1Ksyop9H-UHWvdMB5Ps',
		'https://docs.google.com/document/d/18VaVO2VnFMo5Lv6VFZ4hP-lbX3XxHKnPu6wc2sxxA6U',
		'https://docs.google.com/document/d/1XuD5iloTWdpFAAzuSHpQuPKVwsrQeyAlT0CSFoIYk3A',
		'https://docs.google.com/document/d/1yoKoZq3DBCXLJ__1LNod_d_p6SkKC2VzQ3r-pjlOa4M',
		'https://docs.google.com/document/d/1CIJLV1CN57naLf9gG9Y6C7aZ6ieLM9uL5CGquxCNPQM',
		'https://docs.google.com/document/d/1m9yGcNhNfQRCfdcmwb4mAy2sVG3BXHjM6cBFKjzmvFw',
	]

	fUrls = [
		'https://docs.google.com/file/d/0B8UYgI2TD_nmWG04bG5teFdNZlk',
		'https://docs.google.com/file/d/0B8UYgI2TD_nmTlQ3UXY1WGlOZVk',
		'https://docs.google.com/file/d/0B8UYgI2TD_nmMU1ab3g3MFhIdkk',
		'https://docs.google.com/file/d/0B8UYgI2TD_nmaDQxY1l4VFVQTXc',
		'https://docs.google.com/file/d/0B8UYgI2TD_nmQjB4UE5ZMkdVeDg',
		'https://docs.google.com/file/d/0B8UYgI2TD_nmU0tPeXlRYm00MHM',
		'https://docs.google.com/file/d/0B8UYgI2TD_nmeVBGcjRQUVpDSjA',
		'https://docs.google.com/file/d/0B8UYgI2TD_nmSmtWVVpkZG14RVk',
		'https://docs.google.com/file/d/0B8UYgI2TD_nmanB5ZEZHRHNSNDg',
		'https://docs.google.com/file/d/0B8UYgI2TD_nmNlp0a0RZSmZ3UFk',
		'https://docs.google.com/file/d/0B8UYgI2TD_nmOTRCU3FWSzdYV3M',
		'https://docs.google.com/file/d/0B8UYgI2TD_nmRjhrUDNPZXlCQWs',
		'https://docs.google.com/file/d/0B8UYgI2TD_nmNUMzNWJpZnJkRkU',
		'https://docs.google.com/file/d/0B1aV_gkFqPDdbnh6Q244b1lDN0k/',
		'https://docs.google.com/file/d/0B8UYgI2TD_nmNUMzNWJpZnJkRkU/edit',
		'https://docs.google.com/file/d/0B1aV_gkFqPDdMUUtM3ViaVdzM0E/',
		'https://docs.google.com/file/d/0B1aV_gkFqPDdM181YkRFWlBzUlE/',
		'https://docs.google.com/file/d/0B1aV_gkFqPDdY1RTNWcxcjlURDQ/edit',
	]

	# print(makeDriveDisambiguation(urls))
	# parse = GDocExtractor(url)
	# base, resc = parse.extract()
	# # parse.getTitle()

	# print(GDocExtractor.getDriveFileUrls('https://drive.google.com/folderview?id=0B_mXfd95yvDfQWQ1ajNWZTJFRkk&usp=drive_web'))


	# for fUrl in fUrls:
	# 	extr = GFileExtractor(fUrl)
	# 	print(extr)
	# 	print(extr.extract())

	# with open("test.html", "wb") as fp:
	# 	fp.write(ret.encode("utf-8"))


	# parse = GDocExtractor('https://docs.google.com/document/d/19CLYtylsoFYEQSpp4tJ5trzkiAS0G3w_0ay7l62qy44/pub')

	parse = GDocExtractor('https://docs.google.com/document/d/1atXMtCutHRpcHwSRS5UyMAC58_gQjMPR2dDVn1LCD3E')
	parse.extract()

if __name__ == "__main__":
	import logSetup
	if __name__ == "__main__":
		print("Initializing logging")
		logSetup.initLogging()

	test()


















