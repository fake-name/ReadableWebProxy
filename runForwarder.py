#!flask/bin/python

import sys
import time
import traceback
import datetime
import settings

import sqlalchemy.exc

import config
import common.database as db
import common.LogBase as LogBase
from nusync import AmqpInterface


if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()




def go():
	print("go")
	settings_dict = {
		"RABBIT_LOGIN" : settings.NU_RABBIT_LOGIN,
		"RABBIT_PASWD" : settings.NU_RABBIT_PASWD,
		"RABBIT_SRVER" : settings.NU_RABBIT_SRVER,
		"RABBIT_VHOST" : settings.NU_RABBIT_VHOST,
	}
	nureleaseconsumer = AmqpInterface.RabbitQueueHandler(settings_dict, is_master=True)
	print(nureleaseconsumer)
	while 1:
		time.sleep(1)
		try:
			release = nureleaseconsumer.get_item()
			print(release)
		except Exception:
			pass


if __name__ == "__main__":

	go()
