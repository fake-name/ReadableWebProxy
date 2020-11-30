
import time
import abc

import statsd
from influxdb import InfluxDBClient

import config

class StatsdMixin(metaclass=abc.ABCMeta):

	@abc.abstractproperty
	def statsd_prefix(self):
		pass

	@property
	def mon_con(self):
		if self.__mon_con is None:
			self.__mon_con = statsd.StatsClient(
					host = config.C_GRAPHITE_DB_IP,
					port = 8125,
					prefix = self.statsd_prefix,
					)
		return self.__mon_con

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__mon_con = None



class InfluxDBMixin(metaclass=abc.ABCMeta):


	@abc.abstractproperty
	def influxdb_measurement_name(self):
		pass

	@abc.abstractproperty
	def influxdb_type(self):
		pass

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.__influx_client = InfluxDBClient(
				host     = config.C_INFLUX_DB_URL,
				port     = config.C_INFLUX_DB_PORT,
				database = config.C_INFLUX_DB_DBNAME
			)

	def put_measurement(self, measurement_name, measurement, fields, extra_tags=None):
		if extra_tags is None:
			extra_tags = {}
		else:
			assert isinstance(extra_tags, dict)
		assert isinstance(fields, dict)

		if self.__influx_client is None:
			self.__influx_client = InfluxDBClient(
					host     = config.C_INFLUX_DB_URL,
					port     = config.C_INFLUX_DB_PORT,
					database = config.C_INFLUX_DB_DBNAME
				)


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

		self.__influx_client.write_points(points)
