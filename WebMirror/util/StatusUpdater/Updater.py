


if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import pickle
from common import database
import config
import common.LogBase
import WebMirror.rules
from WebMirror.OutputFilters.util.MessageConstructors import pack_message
import WebMirror.TimedTriggers.TriggerBase

import common.get_rpyc
# import WebMirror.OutputFilters.AmqpInterface


class MetaUpdater(WebMirror.TimedTriggers.TriggerBase.TriggerBaseClass):

	pluginName = "Meta Updater"

	loggerPath = 'MetaUpdater'

	def __init__(self):
		super().__init__()
		# print()


		self.rpc_interface = common.get_rpyc.RemoteJobInterface("FeedUpdater")

		# if config.C_DO_RABBIT:
		# 	print("No message queue! Doing independent RabbitMQ connection!")
		# 	# traceback.print_stack()
		# 	# print("Wat?")
		# 	# print()
		# 	self.msg_q = False
		# 	amqp_settings = {
		# 		"RABBIT_LOGIN" : config.C_RABBIT_LOGIN,
		# 		"RABBIT_PASWD" : config.C_RABBIT_PASWD,
		# 		"RABBIT_SRVER" : config.C_RABBIT_SRVER,
		# 		"RABBIT_VHOST" : config.C_RABBIT_VHOST,
		# 		'taskq_task'     : 'task.master.q',
		# 		'taskq_response' : 'response.master.q',
		# 	}

		# 	self._amqpint = WebMirror.OutputFilters.AmqpInterface.RabbitQueueHandler(amqp_settings)

	def get_feed_count_message(self):
		feeds = set()
		for ruleset in WebMirror.rules.load_rules():
			feeds |= set(ruleset['feedurls'])

		data = {
			"feed-count" : len(feeds)
		}

		return pack_message("system-feed-counts", data)

	def get_times(self):
		conn = database.get_db_session()
		aps = conn.execute("SELECT job_state FROM apscheduler_jobs;")

		update_times = []
		for blob, in aps:
			job_dict = pickle.loads(blob)
			update_times.append((
					job_dict['id'],
					job_dict['next_run_time'].isoformat()
				))

		data = {
			"update-times" : update_times,
		}
		database.delete_db_session()

		return pack_message("system-update-times", data)

	def go(self):
		feeds = self.get_feed_count_message()
		times = self.get_times()

		self.rpc_interface.put_feed_job(feeds)
		self.rpc_interface.put_feed_job(times)
		# self._amqpint.put_item(feeds)
		# self._amqpint.put_item(times)




def do_meta_update():
	updator = MetaUpdater()
	updator._go()

	updator = MetaUpdater()
	updator._go()

	updator = MetaUpdater()
	updator._go()


if __name__ == '__main__':
	do_meta_update()

