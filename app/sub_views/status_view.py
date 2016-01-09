
from flask import g
from flask import render_template
from flask import make_response
from flask import request

import pickle
import time
import datetime
from calendar import timegm

from sqlalchemy.sql import text
from app import app


import WebMirror.database as db

from app.utilities import paginate
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.expression import func
from tzlocal import get_localzone
import WebMirror.API

def datetime_to_utc_timestamp(timeval):
	"""
	Converts a datetime instance to a timestamp.

	:type timeval: datetime
	:rtype: float
	"""

	if timeval is not None:
		return timegm(timeval.utctimetuple()) + timeval.microsecond / 1000000

def get_scheduled_tasks(session):

	scheduled = session.execute(text("""SELECT id, next_run_time, job_state FROM apscheduler_jobs;"""))
	ret = list(scheduled)


	now = datetime.datetime.now(get_localzone())
	now_utc = datetime_to_utc_timestamp(now)

	ret = [(name, ts-now_utc, pickle.loads(value)) for name, ts, value in ret]


	for name, ts, value in ret:
		then = value['next_run_time'].astimezone(tz=None)
		# print((ts, now_utc, then, type(then)))
		now = datetime.datetime.now(datetime.timezone.utc)
		tgt = then - now
		value['time_til_job'] = tgt
	return ret



@app.route('/status/', methods=['GET'])
def status_view():

	session = g.session
	# session.expire()
	tasks = get_scheduled_tasks(session)
	states = session.query(db.PluginStatus).all()
	session.commit()
	return render_template('status.html',
						   tasks          = tasks,
						   states         = states,
						   )


