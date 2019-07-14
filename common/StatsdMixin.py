
import time
import abc

import statsd
from influxdb import InfluxDBClient

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


class InfluxDBMixin(metaclass=abc.ABCMeta):


	@abc.abstractproperty
	def influxdb_measurement_name(self):
		pass

	@abc.abstractproperty
	def influxdb_type(self):
		pass

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.influx_client = InfluxDBClient(
				host     = settings.INFLUX_DB_URL,
				port     = settings.INFLUX_DB_PORT,
				database = settings.INFLUX_DB_DBNAME
			)

	def put_measurement(self, measurement_name, measurement, fields, extra_tags=None):
		if extra_tags is None:
			extra_tags = {}
		else:
			assert isinstance(extra_tags, dict)
		assert isinstance(fields, dict)

		points = [
			{
					'measurement' : self.influxdb_measurement_name,
					"tags": {
							'type' : self.influxdb_type,
							**extra_tags
						},
					'time' : int(time.time() * 1e9),
					'fields' : {
							measurement_name : measurement,
							**fields
						}
				}
			]

		self.influx_client.write_points(points)
