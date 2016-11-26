

import logging
import abc
import datetime
import psycopg2
import traceback
import urllib.parse
import sqlalchemy.exc
import common.database as db


import WebMirror.TimedTriggers.RssTrigger
import WebMirror.TimedTriggers.RollingRewalkTrigger
import WebMirror.TimedTriggers.PageTriggers

def exposed_rss_trigger():
	'''
	Execute normal RSS triggers.
	'''

	run = WebMirror.TimedTriggers.RssTrigger.RssTriggerBase()
	run._go()



def exposed_hourly_page_triggers():
	'''
	Re-trigger hourly page triggers.
	'''

	run = WebMirror.TimedTriggers.PageTriggers.HourlyPageTrigger()
	run._go()

def exposed_daily_page_triggers():
	'''
	Retrigger daily pages. This includes re-walking every series root on rrl.
	'''
	run2 = WebMirror.TimedTriggers.PageTriggers.EveryOtherDayPageTrigger()
	run2._go()

