


import runStatus
runStatus.preloadDicts = False

import common.LogBase as LogBase
import abc



class ContentPreprocessor(LogBase.LoggerMixin, metaclass=abc.ABCMeta):

	def __init__(self, wg_proxy):
		super().__init__()
		self.wg_proxy = wg_proxy

	@abc.abstractmethod
	def preprocessContent(self, url, mimetype, contentstr):
		pass

	@staticmethod
	def wantsUrl(url):
		print("Preprocessor wat?")
		return True


	# Proxy call for enforcing call-correctness
	@classmethod
	def preprocess(cls, url, mimeType, content, wg_proxy):
		instance = cls(wg_proxy)
		return instance.preprocessContent(url, mimeType, content)
