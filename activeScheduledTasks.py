
#pylint: disable=C0413,C0412

# Convenience functions to make intervals clearer.
def days(num):
	return 60*60*24*num
def hours(num):
	return 60*60*num
def minutes(num):
	return 60*num

'''
	 0  : (WebMirror.TimedTriggers.UrlTriggers.RssTriggerBase,                            minutes(45)),
	 1  : (WebMirror.TimedTriggers.RollingRewalkTriggers.RollingRewalkTriggersBase,          hours(4)),
	 2  : (WebMirror.TimedTriggers.UrlTriggers.HourlyPageTrigger,                         minutes(60)),
	 3  : (WebMirror.TimedTriggers.UrlTriggers.EverySixHoursPageTrigger,                     hours(4)),
	4  : (WebMirror.TimedTriggers.UrlTriggers.EveryOtherDayPageTrigger,                      days(3)),
	# 5  : (WebMirror.util.StatusUpdater.Updater.MetaUpdater,                              minutes(10)),
	 6  : (WebMirror.TimedTriggers.QueueTriggers.NuQueueTrigger,                          minutes(45)),

	 7  : (WebMirror.TimedTriggers.LocalFetchTriggers.HourlyLocalFetchTrigger,               hours(1)),

	 8  : (Misc.HistoryAggregator.Consolidate.DbFlattener,                                    days(3)),
	 9  : (WebMirror.management.FeedDbManage.RssFunctionSaver,                              hours(12)),
	10  : (Misc.HistoryAggregator.Consolidate.TransactionTruncator,                       minutes(20)),
	11  : (RawArchiver.TimedTriggers.RawRollingRewalkTrigger.RollingRawRewalkTrigger,       hours(12)),
'''


# Plugins in this dictionary are the active plugins. Comment out a plugin to disable it.


target_jobs = {

	'scheduled_jobs.python_job.RssTriggerJob' : {
		"name"             : 'AUTO: Rss Feeds Trigger job',
		"interval"         : minutes(45),
		# "minute"           : '*/42',
	},
	'scheduled_jobs.python_job.RollingRewalkTriggersBaseJob' : {
		"name"             : 'AUTO: Rolling Rewalk Trigger job',
		"interval"         : hours(4),
		# "minute"           : '15',
		# "hour"             : '*/4',
	},
	'scheduled_jobs.python_job.HourlyPageTriggerJob' : {
		"name"             : 'AUTO: Hourly Page Trigger job',
		"interval"         : minutes(60),
		# "minute"           : '0',
		# "hour"             : '*',
	},
	'scheduled_jobs.python_job.EverySixHoursPageTriggerJob' : {
		"name"             : 'AUTO: Every Four Hours Trigger job',
		"interval"         : hours(4),
		# "minute"           : '45',
		# "hour"             : '*/6',
	},
	'scheduled_jobs.python_job.EveryOtherDayPageTriggerJob' : {
		"name"             : 'AUTO: Every other day Trigger job',
		"interval"         : days(3),
		# "day"              : '*/2',
		# "minute"           : '30',
		# "hour"             : '15',
	},
	'scheduled_jobs.python_job.HourlyLocalFetchTriggerJob' : {
		"name"             : 'AUTO: Hourly local fetch trigger job',
		"interval"         : hours(1),
		# "minute"           : '0',
	},
	'scheduled_jobs.python_job.DbFlattenerJob' : {
		"name"             : 'AUTO: DB Flattener job',
		"interval"         : days(3),
		# "day"              : '*/3',
		# "minute"           : '30',
		# "hour"             : '5',
	},
	'scheduled_jobs.python_job.RssFunctionSaverJob' : {
		"name"             : 'AUTO: Function Saver job',
		"interval"         : hours(12),
		# "minute"           : '50',
		# "hour"             : '*/12',
	},
	'scheduled_jobs.python_job.TransactionTruncatorJob' : {
		"name"             : 'AUTO: Transaction table truncator job',
		"interval"         : minutes(20),
		# "minute"           : '*/25',
	},
	'scheduled_jobs.python_job.RollingRawRewalkTriggerJob' : {
		"name"             : 'AUTO: Rolling Raw Rewalk Trigger job',
		"interval"         : hours(12),
		# "minute"           : '10',
		# "hour"             : '*/12',
	},
	'scheduled_jobs.python_job.NuHeaderJob' : {
		"name"             : 'AUTO: NuHeader job',
		"interval"         : minutes(20),
		# "minute"           : '*/22',
		# "hour"             : '*',
	},

	'scheduled_jobs.python_job.NuQueueTriggerJob' : {
		"name"             : 'AUTO: NU Homepage Fetch',
		"interval"         : minutes(60),
		# "minute"           : '*/40',
	},
	'scheduled_jobs.python_job.WebMirrorPriorityDropper' : {
		"name"             : 'AUTO: WebMirror Priority Dropper',
		"interval"         : hours(4),
		# "minute"           : '*/40',
	},

}
