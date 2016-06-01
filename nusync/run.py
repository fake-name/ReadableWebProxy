
import json
import datetime

from apscheduler.jobstores.memory     import MemoryJobStore
from apscheduler.schedulers.blocking  import BlockingScheduler
from apscheduler.executors.pool       import ThreadPoolExecutor

import AmqpInterface
import database as db
import logSetup

import NUSeriesUpdateFilter

def load_settings():
	with open("settings.json") as fp:
		filec = fp.read()
	return json.loads(filec)


def go():
	settings = load_settings()

	fetcher = NUSeriesUpdateFilter.NUSeriesUpdateFilter(db.session(), settings)
	print(fetcher.handlePage("https://www.novelupdates.com"))


executors = {
	'main_jobstore': ThreadPoolExecutor(5),
}
job_defaults = {
	'coalesce': True,
	'max_instances': 1,
}

jobstores = {
	'main_jobstore'      : MemoryJobStore()

}

def run():

	sched = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

	startTime = datetime.datetime.now() + datetime.timedelta(seconds=3)

	sched.add_job(go,
				# args               = (callee.__name__, ),
				trigger            = 'interval',
				seconds            = 60*60*1,
				start_date         = startTime,
				id                 = 0,
				max_instances      =  1,
				replace_existing   = True,
				jobstore           = "main_jobstore",
				misfire_grace_time = 2**30)

	sched.start()

def dump_db():
	settings = load_settings()
	amqp = AmqpInterface.RabbitQueueHandler(settings)
	print(amqp)

	sess = db.session()
	rows = sess.query(db.LinkWrappers).all()
	for row in rows:
		amqp.putRow(row)

if __name__ == '__main__':
	logSetup.initLogging()
	dump_db()
	# run()

