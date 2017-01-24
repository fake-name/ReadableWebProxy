


import Misc.NuForwarder.NuHeader

autoscheduler_plugins = {
	Misc.NuForwarder.NuHeader.do_schedule,

}


# The processing pipeline has three stages.
# Preprocessors have access to the page content before it's fed through the filters
# Filters are for extracting additional information from the in-flight pages.
# Plugins rewrite the page content for more pleasant consumption.

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


import WebMirror.OutputFilters.RoyalRoadL.RRLSeriesPageFilter
import WebMirror.OutputFilters.RoyalRoadL.RRLSeriesUpdateFilter
import WebMirror.OutputFilters.WattPad.WattPadSeriesPageFilter
import WebMirror.OutputFilters.JapTem.JapTemSeriesPageFilter
import WebMirror.OutputFilters.Booksie.BooksieSeriesPageFilter
import WebMirror.OutputFilters.LNDB.LNDBSeriesPageFilter
import WebMirror.OutputFilters.Twitter.TwitterFilter
import WebMirror.OutputFilters.Nu.NUHomepageFilter


# Filters are executed against fetched content first.
FILTERS = [
	WebMirror.OutputFilters.RoyalRoadL.RRLSeriesPageFilter.RRLSeriesPageProcessor,
	WebMirror.OutputFilters.RoyalRoadL.RRLSeriesUpdateFilter.RRLSeriesUpdateFilter,

	WebMirror.OutputFilters.Nu.NUHomepageFilter.NuHomepageFilter,
	WebMirror.OutputFilters.JapTem.JapTemSeriesPageFilter.JapTemSeriesPageProcessor,
	#WebMirror.OutputFilters.WattPad.WattPadSeriesPageFilter.WattPadSeriesPageFilter,
	WebMirror.OutputFilters.Booksie.BooksieSeriesPageFilter.BooksieSeriesPageProcessor,
	WebMirror.OutputFilters.LNDB.LNDBSeriesPageFilter.LNDBSeriesPageFilter,

	WebMirror.OutputFilters.Twitter.TwitterFilter.TwitterProcessor,
]



import WebMirror.processor.HtmlProcessor
import WebMirror.processor.GDriveDirProcessor
import WebMirror.processor.GDocProcessor
import WebMirror.processor.MarkdownProcessor
import WebMirror.processor.BinaryProcessor
import WebMirror.processor.RssProcessor
import WebMirror.processor.WattPadJsonProcessor
import WebMirror.processor.RoyalRoadLChapterPageProcessor
import WebMirror.processor.RoyalRoadLSeriesPageProcessor
import WebMirror.processor.NuProcessor
import WebMirror.processor.KobatoChanDaiSukiPreprocessor


PLUGINS = [
	WebMirror.processor.HtmlProcessor.HtmlPageProcessor,
	WebMirror.processor.GDriveDirProcessor.GDriveDirProcessor,
	WebMirror.processor.GDocProcessor.GdocPageProcessor,
	WebMirror.processor.MarkdownProcessor.MarkdownProcessor,
	WebMirror.processor.BinaryProcessor.BinaryResourceProcessor,
	WebMirror.processor.RssProcessor.RssProcessor,
	WebMirror.processor.WattPadJsonProcessor.WattPadJsonProcessor,
	WebMirror.processor.RoyalRoadLChapterPageProcessor.RoyalRoadLChapterPageProcessor,
	WebMirror.processor.RoyalRoadLSeriesPageProcessor.RoyalRoadLSeriesPageProcessor,
	WebMirror.processor.KobatoChanDaiSukiPreprocessor.KobatoChanDaiSukiPageProcessor,
	WebMirror.processor.NuProcessor.NuProcessor,
]


# import WebMirror.OutputFilters.WattPad.WattPadInit

INIT_CALLS = [
	#WebMirror.OutputFilters.WattPad.WattPadInit.init_call
]

print("Processing plugins: %s, active filters: %s, trigger plugins: %s" % (len(PLUGINS), len(FILTERS), len(scrapePlugins)))
