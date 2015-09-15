

from flask import render_template
from flask import make_response
from flask import request

import pickle
import time
import datetime

from sqlalchemy.sql import text
from app import app


import WebMirror.database as db

from app.utilities import paginate
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.expression import func

import WebMirror.API

def get_scheduled_tasks():

	scheduled = db.get_session().execute(text("""SELECT id, next_run_time, job_state FROM apscheduler_jobs;"""))
	ret = list(scheduled)

	ret = [(name, ts-time.time(), pickle.loads(value)) for name, ts, value in ret]

	for name, ts, value in ret:
		then = value['next_run_time']
		now = datetime.datetime.now(datetime.timezone.utc)
		tgt = then - now
		value['time_til_job'] = tgt
	return ret



@app.route('/status/', methods=['GET'])
def status_view():

	tasks = get_scheduled_tasks()

	states = db.get_session().query(db.PluginStatus).all()
	print(states)

	return render_template('status.html',
						   tasks          = tasks,
						   states         = states,
						   )


