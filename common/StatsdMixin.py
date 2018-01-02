
import abc

import statsd
import settings


class StatsdMixin(metaclass=abc.ABCMeta):

	@abc.abstractproperty
	def statsd_prefix(self):
		pass

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


		self.mon_con = statsd.StatsClient(
				host = settings.GRAPHITE_DB_IP,
				port = 8125,
				prefix = self.statsd_prefix,
				)
