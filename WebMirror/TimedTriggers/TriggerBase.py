

import logging
import abc


class TriggerBaseClass(metaclass=abc.ABCMeta):

	# Abstract class (must be subclassed)
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def pluginName(self):
		return None

	@abc.abstractmethod
	def loggerPath(self):
		return None


	def __init__(self):

		self.log = logging.getLogger("Main.Trigger."+self.loggerPath)
		self.log.info("Loading %s Runner", self.pluginName)


	def _go(self):
		self.log.info("Checking %s for updates", self.pluginName)

		self.go()




if __name__ == "__main__":
	import utilities.testBase as tb

	with tb.testSetup(startObservers=True):

		run = Runner()
		run.go()

