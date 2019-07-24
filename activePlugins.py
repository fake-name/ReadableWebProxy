
# pylint: disable=C0413

# The processing pipeline has three stages.
# Preprocessors have access to the page content before it's fed through the
#     filters (they're located in the remote AutoTreiver instances)
# Filters are for extracting additional information from the in-flight pages.
# Plugins rewrite the page content for more pleasant consumption.

import WebMirror.OutputFilters.RoyalRoadL.RRLSeriesPageFilter
import WebMirror.OutputFilters.RoyalRoadL.RRLSeriesUpdateFilter
import WebMirror.OutputFilters.RoyalRoadL.RRLJsonXmlSeriesUpdateFilter
import WebMirror.OutputFilters.WattPad.WattPadSeriesPageFilter
import WebMirror.OutputFilters.JapTem.JapTemSeriesPageFilter
import WebMirror.OutputFilters.Booksie.BooksieSeriesPageFilter
import WebMirror.OutputFilters.LNDB.LNDBSeriesPageFilter
import WebMirror.OutputFilters.Twitter.TwitterFilter
import WebMirror.OutputFilters.Nu.NUHomepageFilter
import WebMirror.OutputFilters.Nu.NuSeriesPageFilter
import WebMirror.OutputFilters.Qidian.QidianSeriesPageFilter


# Filters are executed against fetched content after preprocessing. They cannot modify content, but they can
# perform operations based on it's content (e.g. generating releases for WLNUpdates, etc...).
FILTERS = [
	WebMirror.OutputFilters.RoyalRoadL.RRLSeriesPageFilter.RRLSeriesPageFilter,
	WebMirror.OutputFilters.RoyalRoadL.RRLSeriesUpdateFilter.RRLSeriesUpdateFilter,
	WebMirror.OutputFilters.RoyalRoadL.RRLJsonXmlSeriesUpdateFilter.RRLJsonXmlSeriesUpdateFilter,

	WebMirror.OutputFilters.Nu.NUHomepageFilter.NuHomepageFilter,
	WebMirror.OutputFilters.Nu.NuSeriesPageFilter.NUSeriesPageFilter,
	WebMirror.OutputFilters.JapTem.JapTemSeriesPageFilter.JapTemSeriesPageFilter,
	#WebMirror.OutputFilters.WattPad.WattPadSeriesPageFilter.WattPadSeriesPageFilter,
	WebMirror.OutputFilters.Booksie.BooksieSeriesPageFilter.BooksieSeriesPageFilter,
	WebMirror.OutputFilters.LNDB.LNDBSeriesPageFilter.LNDBSeriesPageFilter,
	WebMirror.OutputFilters.Twitter.TwitterFilter.TwitterFilter,
	WebMirror.OutputFilters.Qidian.QidianSeriesPageFilter.QidianSeriesPageFilter,
]



import WebMirror.processor.HtmlProcessor
import WebMirror.processor.GDriveDirProcessor
import WebMirror.processor.GDocProcessor
import WebMirror.processor.MarkdownProcessor
import WebMirror.processor.BinaryProcessor
import WebMirror.processor.JsonProcessor
import WebMirror.processor.XmlProcessor
import WebMirror.processor.RssProcessor
import WebMirror.processor.WattPadJsonProcessor
import WebMirror.processor.RoyalRoadLChapterPageProcessor
import WebMirror.processor.RoyalRoadLSeriesPageProcessor

import WebMirror.processor.NuProcessor
import WebMirror.processor.FontRemapProcessors
import WebMirror.processor.GarbageInlineProcessors
import WebMirror.processor.XiAiNovelProcessor

# Finally, plugins handle fully extracting the content from a page. They can also do
# rewriting like how preprocessors work, but they're intended for more general use.
PLUGINS = [
	WebMirror.processor.HtmlProcessor.HtmlPageProcessor,
	WebMirror.processor.GDriveDirProcessor.GDriveDirProcessor,
	WebMirror.processor.GDocProcessor.GdocPageProcessor,
	WebMirror.processor.MarkdownProcessor.MarkdownProcessor,
	WebMirror.processor.BinaryProcessor.BinaryResourceProcessor,
	WebMirror.processor.JsonProcessor.JsonProcessor,
	WebMirror.processor.XmlProcessor.XmlProcessor,
	WebMirror.processor.RssProcessor.RssProcessor,
	WebMirror.processor.WattPadJsonProcessor.WattPadJsonProcessor,
	WebMirror.processor.RoyalRoadLChapterPageProcessor.RoyalRoadLChapterPageProcessor,
	WebMirror.processor.RoyalRoadLSeriesPageProcessor.RoyalRoadLSeriesPageProcessor,
	WebMirror.processor.RoyalRoadLSeriesPageProcessor.RoyalRoadLSeriesPageProcessor,
	#WebMirror.processor.FontRemapProcessors.KobatoChanDaiSukiPageProcessor,
	# WebMirror.processor.FontRemapProcessors.NepustationPageProcessor,
	WebMirror.processor.FontRemapProcessors.EccentricTranslationsFontRemapProcessor,
	WebMirror.processor.NuProcessor.NuProcessor,
	WebMirror.processor.GarbageInlineProcessors.HecatesCornerPageProcessor,
	WebMirror.processor.GarbageInlineProcessors.ZenithNovelsPageProcessor,
	WebMirror.processor.GarbageInlineProcessors.LightNovelsWorldPageProcessor,
	WebMirror.processor.GarbageInlineProcessors.WatashiWaSugoiDesuPageProcessor,
	WebMirror.processor.GarbageInlineProcessors.ShamelessOniisanPageProcessor,
	WebMirror.processor.GarbageInlineProcessors.FantasyBooksLiveProcessor,
	WebMirror.processor.GarbageInlineProcessors.MayonaizeShrimpLiveProcessor,
	WebMirror.processor.GarbageInlineProcessors.RebirthOnlineLiveProcessor,
	WebMirror.processor.GarbageInlineProcessors.ConvallariasLibraryProcessor,
	WebMirror.processor.GarbageInlineProcessors.AfterAugustMakingProcessor,
	WebMirror.processor.GarbageInlineProcessors.CreativeNovelsPageProcessor,

	WebMirror.processor.XiAiNovelProcessor.XiAiNovelPageProcessor,
]


# import WebMirror.OutputFilters.WattPad.WattPadInit

INIT_CALLS = [
	#WebMirror.OutputFilters.WattPad.WattPadInit.init_call
]

print("Processing plugins: %s, active filters: %s" % (len(PLUGINS), len(FILTERS)))
