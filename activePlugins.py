


# Convenience functions to make intervals clearer.
def days(num):
	return 60*60*24*num
def hours(num):
	return 60*60*num
def minutes(num):
	return 60*num


# Plugins in this dictionary are the active plugins. Comment out a plugin to disable it.
# plugin keys specify when plugins will start, and cannot be duplicates.
# All they do is specify the order in which plugins
# are run, initially, starting after 1-minue*{key} intervals

import WebMirror.TimedTriggers.RssTrigger
import WebMirror.TimedTriggers.RollingRewalkTrigger
import WebMirror.TimedTriggers.PageTriggers

scrapePlugins = {
	# 0  : (WebMirror.TimedTriggers.RssTrigger.RssTriggerBase,                     minutes(10)),
	# 1  : (WebMirror.TimedTriggers.RollingRewalkTrigger.RollingRewalkTriggerBase, minutes(90)),
	# 2  : (WebMirror.TimedTriggers.PageTriggers.HourlyPageTrigger,                minutes(60)),
	# 3  : (WebMirror.TimedTriggers.PageTriggers.EveryOtherDayPageTrigger,             days(2)),
	# 4  : (WebMirror.util.StatusUpdater.Updater.MetaUpdater,                      minutes(10)),
}


import WebMirror.processor.HtmlProcessor
import WebMirror.processor.MarkdownProcessor
import WebMirror.processor.BinaryProcessor

PLUGINS = [
	WebMirror.processor.HtmlProcessor.HtmlPageProcessor,
	WebMirror.processor.MarkdownProcessor.MarkdownProcessor,
	WebMirror.processor.BinaryProcessor.BinaryResourceProcessor,
]

import WebMirror.PreProcessors.LiveJournalPreprocess
import WebMirror.PreProcessors.RedditPreprocess
import WebMirror.PreProcessors.TgStoryTimePreprocess

PREPROCESSORS = [
	WebMirror.PreProcessors.LiveJournalPreprocess.LJPreprocessor,
	WebMirror.PreProcessors.RedditPreprocess.RedditPreprocessor,
	WebMirror.PreProcessors.TgStoryTimePreprocess.TgStoryTimePreprocessor,


]



print("Processing plugins: %s, trigger plugins: %s" % (len(PLUGINS), len(scrapePlugins)))
