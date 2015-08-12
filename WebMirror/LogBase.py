
import logging
import threading
import multiprocessing
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
		procName   = multiprocessing.current_process().name

		if "Thread-" in threadName:
			if threadName not in self.loggers:
				self.loggers[threadName] = logging.getLogger("%s.%s" % (self.loggerPath, threadName))
				self.lastLoggerIndex += 1
			return self.loggers[threadName]
		elif "Process-" in procName:
			if procName not in self.loggers:
				self.loggers[procName] = logging.getLogger("%s.%s" % (self.loggerPath, procName))
				self.lastLoggerIndex += 1
			return self.loggers[procName]

		else:
			# If we're not called in the context of a thread, just return the base log-path
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

