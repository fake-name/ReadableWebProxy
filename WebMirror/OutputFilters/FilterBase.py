

import WebMirror.OutputFilters.AmqpInterface
import config
from WebMirror.processor.ProcessorBase import PageProcessor

class FilterBase(PageProcessor):

	# Filters don't return anything, so turn off that checking.
	_no_ret = True

	def __init__(self):
		amqp_settings = {
			"RABBIT_LOGIN" : config.C_RABBIT_LOGIN,
			"RABBIT_PASWD" : config.C_RABBIT_PASWD,
			"RABBIT_SRVER" : config.C_RABBIT_SRVER,
			"RABBIT_VHOST" : config.C_RABBIT_VHOST,
		}

		self.amqp_conn = WebMirror.OutputFilters.AmqpInterface.RabbitQueueHandler(amqp_settings)

		super().__init__()
		self._no_ret = True

