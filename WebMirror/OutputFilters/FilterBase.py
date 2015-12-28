

import WebMirror.OutputFilters.AmqpInterface
import config
import traceback
from WebMirror.processor.ProcessorBase import PageProcessor

class FilterBase(PageProcessor):

	# Filters don't return anything, so turn off that checking.
	_no_ret = True
	_needs_amqp = True

	def __init__(self, **kwargs):
		super().__init__()
		if self._needs_amqp:
			if "message_q" in kwargs and kwargs['message_q']:
				# print("Filter has a queue, not connecting directly.")
				self.msg_q = kwargs['message_q']
			else:
				# print()
				if config.C_DO_RABBIT:
					print("No message queue! Doing independent RabbitMQ connection!")
					# traceback.print_stack()
					# print("Wat?")
					# print()
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
		if self._needs_amqp:
			raise ValueError("Plugin declared to not require AMQP connectivity, and yet AMQP call used?")

		if config.C_DO_RABBIT:
			self.log.info("Putting item in to AMQP queue!")
			if self.msg_q:
				items_in_queue = self.msg_q.qsize()
				if items_in_queue > 100:
					self.log.warning("AMQP Message queue too large? Items in queue: %s", items_in_queue)

				self.msg_q.put(("amqp_msg", item))

			else:
				self._amqpint.put_item(item)
		else:
			self.log.info("NOT Putting item in to AMQP queue!")
