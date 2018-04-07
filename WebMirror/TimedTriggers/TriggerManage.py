

import logging
import abc
import datetime

import traceback
import urllib.parse
import sqlalchemy.exc
import common.database as db


import WebMirror.TimedTriggers.UrlTriggers
import WebMirror.TimedTriggers.RollingRewalkTriggers

def exposed_rss_trigger():
	'''
	Execute normal RSS triggers.
	'''

	run = WebMirror.TimedTriggers.UrlTriggers.RssTriggerBase()
	run._go()



def exposed_hourly_page_triggers():
	'''
	Re-trigger hourly page triggers.
	'''

	run = WebMirror.TimedTriggers.UrlTriggers.HourlyPageTrigger()
	run._go()

def exposed_daily_page_triggers():
	'''
	Retrigger daily pages. This includes re-walking every series root on rrl.
	'''
	run2 = WebMirror.TimedTriggers.UrlTriggers.EveryOtherDayPageTrigger()
	run2._go()

