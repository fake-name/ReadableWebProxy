


import runStatus
runStatus.preloadDicts = False

import WebMirror.LogBase as LogBase
import abc



class ContentPreprocessor(LogBase.LoggerMixin, metaclass=abc.ABCMeta):

	def __init__(self, webgetter):
		super().__init__()
		self.wg = webgetter

	@abc.abstractmethod
	def preprocessContent(self, url, mimetype, contentstr):
		pass

	@staticmethod
	def wantsUrl(url):
		print("Preprocessor wat?")
		return True


	# Proxy call for enforcing call-correctness
	@classmethod
	def preprocess(cls, url, mimeType, content, wg):
		instance = cls(wg)
		return instance.preprocessContent(url, mimeType, content)
