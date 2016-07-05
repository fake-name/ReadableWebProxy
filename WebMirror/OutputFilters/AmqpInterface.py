#!/usr/bin/env python3
import msgpack
import multiprocessing
import LocalAmqpConnector
import logging
import os.path
import ssl


class RabbitQueueHandler(object):
	die = False

	def __init__(self, settings):

		logPath = 'Main.Feeds.RPC'

		self.log = logging.getLogger(logPath)
		self.log.info("RPC Management class instantiated.")


		# Require clientID in settings
		assert "RABBIT_LOGIN"       in settings
		assert "RABBIT_PASWD"       in settings
		assert "RABBIT_SRVER"       in settings
		assert "RABBIT_VHOST"       in settings

		assert "taskq_task"         in settings
		assert "taskq_response"     in settings

		sslopts = self.getSslOpts()

		self.connector = LocalAmqpConnector.Connector(userid            = settings["RABBIT_LOGIN"],
												password           = settings["RABBIT_PASWD"],
												host               = settings["RABBIT_SRVER"],
												virtual_host       = settings["RABBIT_VHOST"],
												ssl                = sslopts,
												master             = settings.get('master', True),
												synchronous        = settings.get('synchronous', False),
												flush_queues       = False,
												prefetch           = settings.get('prefetch', 25),
												durable            = True,
												heartbeat          = 60,
												task_exchange_type = settings.get('queue_mode', 'fanout'),
												poll_rate          = settings.get('poll_rate', 1.0/100),
												task_queue         = settings["taskq_task"],
												response_queue     = settings["taskq_response"],
												)


		self.log.info("Connected AMQP Interface: %s", self.connector)
		self.log.info("Connection parameters: %s, %s, %s, %s", settings["RABBIT_LOGIN"], settings["RABBIT_PASWD"], settings["RABBIT_SRVER"], settings["RABBIT_VHOST"])

	def getSslOpts(self):
		'''
		Verify the SSL cert exists in the proper place.
		'''
		certpath = './rabbit_pub_cert/'

		caCert = os.path.abspath(os.path.join(certpath, './cacert.pem'))
		cert = os.path.abspath(os.path.join(certpath, './cert1.pem'))
		keyf = os.path.abspath(os.path.join(certpath, './key1.pem'))

		assert os.path.exists(caCert), "No certificates found on path '%s'" % caCert
		assert os.path.exists(cert), "No certificates found on path '%s'" % cert
		assert os.path.exists(keyf), "No certificates found on path '%s'" % keyf

		ret = {"cert_reqs" : ssl.CERT_REQUIRED,
				"ca_certs" : caCert,
				"keyfile"  : keyf,
				"certfile"  : cert,
			}
		print("Certificate config: ", ret)

		return ret

	def put_item(self, data):
		# self.log.info("Putting data: %s", data)
		self.connector.putMessage(data, synchronous=1000)
		# self.log.info("Outgoing data size: %s bytes.", len(data))


	def get_item(self):
		ret = self.connector.getMessage()
		if ret:
			self.log.info("Received data size: %s bytes.", len(ret))
		return ret

	def get_job(self):

		new = self.get_item()
		if new:
			self.log.info("Processing AMQP response item!")
			new = msgpack.unpackb(new, encoding='utf-8', use_list=False)
			return new
		return None

	def put_job(self, new_job):
		assert 'module'       in new_job
		assert 'call'         in new_job
		assert 'dispatch_key' in new_job
		assert 'jobid'        in new_job
		assert new_job['jobid'] != None

		# Make sure we have a returned data list for the added job.

		packed_job = msgpack.packb(new_job, use_bin_type=True)
		self.put_item(packed_job)

	def __del__(self):
		self.close()

	def close(self):
		if hasattr(self, "connector") and self.connector:
			self.connector.stop()
			self.connector = None


def test(amqp_settings, is_master):
	amqp_settings['master'] = is_master
	amqpint = RabbitQueueHandler(amqp_settings)
	print(amqpint)
	delay = 10
	for x in range(delay):
		time.sleep(1)
		msg = 'wat %s' % x
		amqpint.put_item(msg.encode("ascii"))
		print("Slept %s of %s" % (x, delay))
	amqpint.close()


if __name__ == '__main__':
	import logSetup
	logSetup.initLogging()

	import config
	import time


	amqp_settings = {
		"RABBIT_LOGIN" : config.C_RABBIT_LOGIN,
		"RABBIT_PASWD" : config.C_RABBIT_PASWD,
		"RABBIT_SRVER" : config.C_RABBIT_SRVER,
		"RABBIT_VHOST" : config.C_RABBIT_VHOST,
		"taskq_task"     : 'tasks.test.q',
		"taskq_response" : 'resps.test.q',
	}

	while 1:
		test(amqp_settings, is_master=True)
		test(amqp_settings, is_master=False)
