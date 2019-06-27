"""A sample job that prints string."""

from ndscheduler import job

import WebMirror.TimedTriggers.RollingRewalkTriggers
import WebMirror.TimedTriggers.UrlTriggers
import WebMirror.TimedTriggers.QueueTriggers
import WebMirror.TimedTriggers.LocalFetchTriggers
import Misc.HistoryAggregator.Consolidate
import WebMirror.util.StatusUpdater.Updater
import WebMirror.management.FeedDbManage

import Misc.NuForwarder.NuHeader
import RawArchiver.TimedTriggers.RawRollingRewalkTrigger

class PythonJob():
	invokable = "None"

	@classmethod
	def meta_info(cls):
		return {
			'job_class_string': '%s.%s' % (cls.__module__, cls.__name__),
			'notes': 'Execute the scheduled job for %s' % cls.invokable,
			'arguments': [],
			'example_arguments': 'None',
		}

	def run(self):
		assert self.invokable


		instance = self.invokable()
		instance.go()
		print("Job %s has finished executing %s" % (self.__class__, self.invokable))
		return


class RssTriggerJob(PythonJob, job.JobBase):
	invokable = WebMirror.TimedTriggers.UrlTriggers.RssTriggerBase

class RollingRewalkTriggersBaseJob(PythonJob, job.JobBase):
	invokable = WebMirror.TimedTriggers.RollingRewalkTriggers.RollingRewalkTriggersBase

class HourlyPageTriggerJob(PythonJob, job.JobBase):
	invokable = WebMirror.TimedTriggers.UrlTriggers.HourlyPageTrigger

class EverySixHoursPageTriggerJob(PythonJob, job.JobBase):
	invokable = WebMirror.TimedTriggers.UrlTriggers.EverySixHoursPageTrigger

class EveryOtherDayPageTriggerJob(PythonJob, job.JobBase):
	invokable = WebMirror.TimedTriggers.UrlTriggers.EveryOtherDayPageTrigger

class NuQueueTriggerJob(PythonJob, job.JobBase):
	invokable = WebMirror.TimedTriggers.QueueTriggers.NuQueueTrigger

class HourlyLocalFetchTriggerJob(PythonJob, job.JobBase):
	invokable = WebMirror.TimedTriggers.LocalFetchTriggers.HourlyLocalFetchTrigger

class DbFlattenerJob(PythonJob, job.JobBase):
	invokable = Misc.HistoryAggregator.Consolidate.DbFlattener

class RssFunctionSaverJob(PythonJob, job.JobBase):
	invokable = WebMirror.management.FeedDbManage.RssFunctionSaver

class TransactionTruncatorJob(PythonJob, job.JobBase):
	invokable = Misc.HistoryAggregator.Consolidate.TransactionTruncator

class RollingRawRewalkTriggerJob(PythonJob, job.JobBase):
	invokable = RawArchiver.TimedTriggers.RawRollingRewalkTrigger.RollingRawRewalkTrigger

class NuHeaderJob(PythonJob, job.JobBase):
	invokable = Misc.NuForwarder.NuHeader.NuHeader

