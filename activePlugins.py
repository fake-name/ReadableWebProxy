


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
import WebMirror.util.StatusUpdater.Updater

scrapePlugins = {
	0  : (WebMirror.TimedTriggers.RssTrigger.RssTriggerBase,                     minutes(10)),
	# 1  : (WebMirror.TimedTriggers.RollingRewalkTrigger.RollingRewalkTriggerBase, minutes(90)),
	2  : (WebMirror.TimedTriggers.PageTriggers.HourlyPageTrigger,                minutes(30)),
	2  : (WebMirror.TimedTriggers.PageTriggers.EverySixHoursPageTrigger,            hours(4)),
	3  : (WebMirror.TimedTriggers.PageTriggers.EveryOtherDayPageTrigger,             days(2)),
	4  : (WebMirror.util.StatusUpdater.Updater.MetaUpdater,                      minutes(10)),
}


import WebMirror.processor.HtmlProcessor
import WebMirror.processor.GDriveDirProcessor
import WebMirror.processor.GDocProcessor
import WebMirror.processor.MarkdownProcessor
import WebMirror.processor.BinaryProcessor
import WebMirror.processor.RssProcessor
import WebMirror.processor.WattPadJsonProcessor

import WebMirror.processor.NovelUpdates.Main

PLUGINS = [
	WebMirror.processor.HtmlProcessor.HtmlPageProcessor,
	WebMirror.processor.GDriveDirProcessor.GDriveDirProcessor,
	WebMirror.processor.GDocProcessor.GdocPageProcessor,
	WebMirror.processor.MarkdownProcessor.MarkdownProcessor,
	WebMirror.processor.BinaryProcessor.BinaryResourceProcessor,
	WebMirror.processor.RssProcessor.RssProcessor,
	WebMirror.processor.WattPadJsonProcessor.WattPadJsonProcessor,

	# Specialized stuff for additional scrapers
	WebMirror.processor.NovelUpdates.Main.NovelUpdatesHtmlPageProcessor,
]


import WebMirror.OutputFilters.RoyalRoadL.RRLSeriesPageFilter
import WebMirror.OutputFilters.RoyalRoadL.RRLSeriesUpdateFilter
import WebMirror.OutputFilters.WattPad.WattPadSeriesPageFilter
import WebMirror.OutputFilters.JapTem.JapTemSeriesPageFilter
import WebMirror.OutputFilters.Booksie.BooksieSeriesPageFilter
import WebMirror.OutputFilters.LNDB.LNDBSeriesPageFilter
import WebMirror.OutputFilters.NovelUpdates.NUSeriesUpdateFilter
import WebMirror.OutputFilters.NovelUpdates.NUSeriesPageFilter
import WebMirror.OutputFilters.Twitter.TwitterFilter

FILTERS = [
	WebMirror.OutputFilters.RoyalRoadL.RRLSeriesPageFilter.RRLSeriesPageProcessor,
	WebMirror.OutputFilters.RoyalRoadL.RRLSeriesUpdateFilter.RRLSeriesUpdateFilter,

	WebMirror.OutputFilters.JapTem.JapTemSeriesPageFilter.JapTemSeriesPageProcessor,
	#WebMirror.OutputFilters.WattPad.WattPadSeriesPageFilter.WattPadSeriesPageFilter,
	WebMirror.OutputFilters.Booksie.BooksieSeriesPageFilter.BooksieSeriesPageProcessor,
	WebMirror.OutputFilters.LNDB.LNDBSeriesPageFilter.LNDBSeriesPageFilter,

	WebMirror.OutputFilters.NovelUpdates.NUSeriesUpdateFilter.NUSeriesUpdateFilter,
	WebMirror.OutputFilters.NovelUpdates.NUSeriesPageFilter.NUSeriesPageProcessor,

	WebMirror.OutputFilters.Twitter.TwitterFilter.TwitterProcessor,
]

import WebMirror.PreProcessors.LiveJournalPreprocess
import WebMirror.PreProcessors.RedditPreprocess
import WebMirror.PreProcessors.WattPadPreprocess
import WebMirror.PreProcessors.TgStoryTimePreprocess
import WebMirror.PreProcessors.RRLPreprocess

PREPROCESSORS = [
	WebMirror.PreProcessors.LiveJournalPreprocess.LJPreprocessor,
	WebMirror.PreProcessors.RedditPreprocess.RedditPreprocessor,
	WebMirror.PreProcessors.WattPadPreprocess.WattPadPreprocessor,
	WebMirror.PreProcessors.TgStoryTimePreprocess.TgStoryTimePreprocessor,


	# Disable the RRL Preprocessor since they rolled back the site.
	# WebMirror.PreProcessors.RRLPreprocess.RRLListPagePreprocessor,
	# WebMirror.PreProcessors.RRLPreprocess.RRLSeriesPagePreprocessor,
	# WebMirror.PreProcessors.RRLPreprocess.RRLChapterPagePreprocessor,
]


# import WebMirror.OutputFilters.WattPad.WattPadInit

INIT_CALLS = [
	#WebMirror.OutputFilters.WattPad.WattPadInit.init_call
]

print("Processing plugins: %s, active filters: %s, trigger plugins: %s" % (len(PLUGINS), len(FILTERS), len(scrapePlugins)))
