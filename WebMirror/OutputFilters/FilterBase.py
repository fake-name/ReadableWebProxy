

import WebMirror.OutputFilters.AmqpInterface
import config
import traceback
from WebMirror.processor.ProcessorBase import PageProcessor

class FilterBase(PageProcessor):

	# Filters don't return anything, so turn off that checking.
	_no_ret = True

	def __init__(self, **kwargs):
		super().__init__()

		if "message_q" in kwargs and kwargs['message_q']:
			print("Filter has a queue, not connecting directly.")
			self.msg_q = kwargs['message_q']
		else:
			print()
			print("No message queue! Doing independent RabbitMQ connection!")
			traceback.print_exc()
			print()
			self.msg_q = False
			amqp_settings = {
				"RABBIT_LOGIN" : config.C_RABBIT_LOGIN,
				"RABBIT_PASWD" : config.C_RABBIT_PASWD,
				"RABBIT_SRVER" : config.C_RABBIT_SRVER,
				"RABBIT_VHOST" : config.C_RABBIT_VHOST,
			}

			self._amqpint = WebMirror.OutputFilters.AmqpInterface.RabbitQueueHandler(amqp_settings)


		self._no_ret = True

	def amqp_put_item(self, item):
		if self.msg_q:
			self.msg_q.put(("amqp_msg", item))

		else:
			self._amqpint.put_item(item)

