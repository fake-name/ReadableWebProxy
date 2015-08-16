

import FeedScrape.InputScrapers.FictionPress.fpScrape
import ScrapePlugins.RunBase



class Runner(ScrapePlugins.RunBase.ScraperBase):
	loggerPath = "Main.Text.Fp.Run"

	pluginName = "FpReleaseMon"


	def _go(self):

		self.log.info("Checking FictionPress feeds for updates")
		fetch = FeedScrape.InputScrapers.FictionPress.fpScrape.FictionPressTest()
		fetch.getChanges()



if __name__ == "__main__":

	import utilities.testBase as tb

	with tb.testSetup(startObservers=False):
		obj = Runner()
		obj.go()

