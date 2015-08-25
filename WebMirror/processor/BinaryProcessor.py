
from . import ProcessorBase





class BinaryResourceProcessor(ProcessorBase.PageProcessor):

	# This is the last-resort option.
	want_priority    = 1

	wanted_mimetypes = [
						"image/gif",
						"image/jpeg",
						"image/pjpeg",
						"image/png",
						"image/svg+xml",
						"image/vnd.djvu",
						"application/octet-stream"
						]


	loggerPath = "Main.Text.FileProc"

	def __init__(self, pageUrl, pgContent, mimeType, loggerPath, **kwargs):
		self.loggerPath = loggerPath+".BinSaver"

		self._tld           = set()
		self._fileDomains   = set()

		self.content  = pgContent
		self.pageUrl  = pageUrl
		self.mimeType = mimeType



	# Dummy wrapper call to shove
	# files through the plugin system.
	def extractContent(self):
		self.log.info("Processing '%s' as binary file.", self.pageUrl)




		ret = {
			'file'     : True,
			'content'  : self.content,
			'fName'    : self.pageUrl,
			'mimeType' : self.mimeType,

		}


		return ret

		# self.updateDbEntry(url=url, title=pgTitle, contents=pgBody, mimetype=mimeType, dlstate=2)


