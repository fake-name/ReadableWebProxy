

import logging
import abc
import datetime

import traceback
import urllib.parse
import sqlalchemy.exc
import common.database as db


import RawArchiver.TimedTriggers.RawRollingRewalkTrigger

def exposed_raw_rewalk_old():
	'''
	Trigger the rewalking system on the rawarchiver
	'''

	run = RawArchiver.TimedTriggers.RawRollingRewalkTrigger.RollingRawRewalkTrigger()
	run.go()

