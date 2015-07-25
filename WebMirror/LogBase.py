
import logging
import threading
import abc

class LoggerMixin(metaclass=abc.ABCMeta):

	@abc.abstractproperty
	def loggerPath(self):
		pass

	@property
	def log(self):
		if not hasattr(self, 'loggers'):
			self.loggers = {}
		if not hasattr(self, 'lastLoggerIndex'):
			self.lastLoggerIndex = 1

		threadName = threading.current_thread().name
		if "Thread-" in threadName:
			if threadName not in self.loggers:
				self.loggers[threadName] = logging.getLogger("%s.Thread-%d" % (self.loggerPath, self.lastLoggerIndex))
				self.lastLoggerIndex += 1

		# If we're not called in the context of a thread, just return the base log-path
		else:
			self.loggers[threadName] = logging.getLogger("%s" % (self.loggerPath,))
		return self.loggers[threadName]


class TestClass(LoggerMixin):
	loggerPath = 'Main.Wat'

	def test(self):
		self.log.info("Wat?")



if __name__ == "__main__":
	print("Test mode!")
	import logSetup
	logSetup.initLogging()


	scraper = TestClass()
	print(scraper)
	extr = scraper.test()
	# print(extr['fLinks'])

