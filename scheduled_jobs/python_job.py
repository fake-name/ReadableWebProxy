"""A sample job that prints string."""

import sys
import os.path

os.environ['NDSCHEDULER_SETTINGS_MODULE'] = 'settings_sched'
addpath = os.path.abspath("./ndscheduler")
if addpath not in sys.path:
	sys.path.append(os.path.abspath("./ndscheduler"))

from ndscheduler.corescheduler import job

import WebMirror.TimedTriggers.RollingRewalkTriggers
import WebMirror.TimedTriggers.UrlTriggers
import WebMirror.TimedTriggers.QueueTriggers
import WebMirror.TimedTriggers.LocalFetchTriggers
import WebMirror.OfflineFilters.NewNetlocTracker as nnt
import WebMirror.util.StatusUpdater.Updater
import WebMirror.management.FeedDbManage
import Misc.HistoryAggregator.Consolidate
import common.management.WebMirrorManage
import common.management.RawMirrorManage

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

class PriorityDropper():
	def go(self):
		common.management.WebMirrorManage.exposed_drop_priorities()

class RawPriorityDropper():
	def go(self):
		common.management.RawMirrorManage.exposed_drop_priorities()

class RssHistoryPurgerRunner():
	def go(self):
		common.management.WebMirrorManage.exposed_clear_rss_history()

class NewUrlExtractorRunner():
	def go(self):
		mapdict = nnt.get_nu_head_urls()
		mapdict_1 = nnt.get_wln_release_urls()
		mapdict_2 = nnt.get_high_priority_urls()
		mapdict_3 = nnt.get_distance_of_zero_urls()

		print("NU Header urls: %s, wln URLs: %s, %s high priority items, %s with a distance of zero." % (len(mapdict), len(mapdict_1), len(mapdict_2), len(mapdict_3)))

		for key, value in mapdict_1.items():
			mapdict.setdefault(key, set())
			mapdict[key].update(value)

		for key, value in mapdict_2.items():
			mapdict.setdefault(key, set())
			mapdict[key].update(value)

		for key, value in mapdict_3.items():
			mapdict.setdefault(key, set())
			mapdict[key].update(value)

		print("Total items: %s" % (len(mapdict), ))

		nnt.push_urls_into_table(mapdict)

		nnt.filter_get_have_urls()

		nnt.update_missing_new_with_title()


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

class RollingRawUrlTriggerJob(PythonJob, job.JobBase):
	invokable = RawArchiver.TimedTriggers.RawUrlStartTrigger.RollingRawUrlStartTrigger

class NuHeaderJob(PythonJob, job.JobBase):
	invokable = Misc.NuForwarder.NuHeader.NuHeader

class WebMirrorPriorityDropper(PythonJob, job.JobBase):
	invokable = PriorityDropper

class RawMirrorPriorityDropper(PythonJob, job.JobBase):
	invokable = RawPriorityDropper

class RssHistoryPurger(PythonJob, job.JobBase):
	invokable = RssHistoryPurgerRunner

class NewUrlExtractor(PythonJob, job.JobBase):
	invokable = NewUrlExtractorRunner

