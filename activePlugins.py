
# pylint: disable=C0413

# The processing pipeline has three stages.
# Preprocessors have access to the page content before it's fed through the filters
# Filters are for extracting additional information from the in-flight pages.
# Plugins rewrite the page content for more pleasant consumption.

import WebMirror.PreProcessors.LiveJournalPreprocess
import WebMirror.PreProcessors.RedditPreprocess
import WebMirror.PreProcessors.WattPadPreprocess
import WebMirror.PreProcessors.TgStoryTimePreprocess
import WebMirror.PreProcessors.RRLPreprocess
import WebMirror.PreProcessors.QidianPreprocess
import WebMirror.PreProcessors.GravityTalesPreprocess
import WebMirror.PreProcessors.WixsitePreprocess
import WebMirror.PreProcessors.LiteroticaPreprocess
import WebMirror.PreProcessors.CreativeNovelsPreprocess

# Preprocessors are executed against fetched content first.
# They're principally useful for doing page-rewriting for
# sites with annoying shit like click-wrappers or injecting
# better navigation components into a page before processing.
PREPROCESSORS = [
	WebMirror.PreProcessors.LiveJournalPreprocess.LJPreprocessor,
	WebMirror.PreProcessors.RedditPreprocess.RedditPreprocessor,
	WebMirror.PreProcessors.WattPadPreprocess.WattPadPreprocessor,
	WebMirror.PreProcessors.TgStoryTimePreprocess.TgStoryTimePreprocessor,
	WebMirror.PreProcessors.QidianPreprocess.QidianPreprocessor,
	WebMirror.PreProcessors.GravityTalesPreprocess.GravityTalesPreprocessor,
	WebMirror.PreProcessors.WixsitePreprocess.JsRendererPreprocessor,
	WebMirror.PreProcessors.CreativeNovelsPreprocess.CreativeNovelsPreprocessor,

	WebMirror.PreProcessors.LiteroticaPreprocess.LiteroticaFavouritePreprocessor,

	# Disable the RRL Preprocessor since they rolled back the site.
	# WebMirror.PreProcessors.RRLPreprocess.RRLListPagePreprocessor,
	# WebMirror.PreProcessors.RRLPreprocess.RRLSeriesPagePreprocessor,
	# WebMirror.PreProcessors.RRLPreprocess.RRLChapterPagePreprocessor,
]


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
