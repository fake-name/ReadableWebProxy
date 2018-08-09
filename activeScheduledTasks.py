
#pylint: disable=C0413,C0412

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

import WebMirror.TimedTriggers.RollingRewalkTriggers
import WebMirror.TimedTriggers.UrlTriggers
import WebMirror.TimedTriggers.QueueTriggers
import Misc.HistoryAggregator.Consolidate
import WebMirror.util.StatusUpdater.Updater
import WebMirror.management.FeedDbManage

import RawArchiver.TimedTriggers.RawRollingRewalkTrigger


scrapePlugins = {
	0  : (WebMirror.TimedTriggers.UrlTriggers.RssTriggerBase,                            minutes(45)),
	1  : (WebMirror.TimedTriggers.RollingRewalkTriggers.RollingRewalkTriggersBase,          hours(4)),
	2  : (WebMirror.TimedTriggers.UrlTriggers.HourlyPageTrigger,                         minutes(90)),
	3  : (WebMirror.TimedTriggers.UrlTriggers.EverySixHoursPageTrigger,                     hours(4)),
	# 4  : (WebMirror.TimedTriggers.UrlTriggers.EveryOtherDayPageTrigger,                      days(3)),
	# 5  : (WebMirror.util.StatusUpdater.Updater.MetaUpdater,                              minutes(10)),
	6  : (WebMirror.TimedTriggers.QueueTriggers.NuQueueTrigger,                          minutes(45)),

	5  : (Misc.HistoryAggregator.Consolidate.DbFlattener,                                    days(3)),
	7  : (WebMirror.management.FeedDbManage.RssFunctionSaver,                              hours(12)),
	8  : (Misc.HistoryAggregator.Consolidate.TransactionTruncator,                       minutes(20)),
	9  : (RawArchiver.TimedTriggers.RawRollingRewalkTrigger.RollingRawRewalkTrigger,       hours(12)),

}


import Misc.NuForwarder.NuHeader

autoscheduler_plugins = {
	Misc.NuForwarder.NuHeader.do_schedule,

}

print("Trigger plugins: %s, autoscheduler plugins: %s" % (len(scrapePlugins), len(autoscheduler_plugins)))


