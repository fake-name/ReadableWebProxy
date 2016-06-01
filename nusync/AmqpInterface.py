#!/usr/bin/env python3
import json
import AmqpConnector
import logging
import os.path
import ssl


class RabbitQueueHandler(object):
	die = False

	def __init__(self, settings, master=False):

		logPath = 'Main.Feeds.RPC'

		self.log = logging.getLogger(logPath)
		self.log.info("RPC Management class instantiated.")


		# Require clientID in settings
		assert "RABBIT_LOGIN"       in settings
		assert "RABBIT_PASWD"       in settings
		assert "RABBIT_SRVER"       in settings
		assert "RABBIT_VHOST"       in settings

		sslopts = self.getSslOpts()

		self.connector = AmqpConnector.Connector(userid            = settings["RABBIT_LOGIN"],
												password           = settings["RABBIT_PASWD"],
												host               = settings["RABBIT_SRVER"],
												virtual_host       = settings["RABBIT_VHOST"],
												ssl                = sslopts,
												master             = master,
												synchronous        = False,
												flush_queues       = False,
												prefetch           = 25,
												durable            = True,
												task_exchange_type = "fanout",
												task_queue         = 'nuresponse.master.q',
												response_queue     = 'nureleases.master.q',
												)


		self.log.info("Connected AMQP Interface: %s", self.connector)
		self.log.info("Connection parameters: %s, %s, %s, %s", settings["RABBIT_LOGIN"], settings["RABBIT_PASWD"], settings["RABBIT_SRVER"], settings["RABBIT_VHOST"])

	def getSslOpts(self):
		'''
		Verify the SSL cert exists in the proper place.
		'''
		certpaths = ['../rabbit_pub_cert/', './rabbit_pub_cert/']
		for certpath in certpaths:

			caCert = os.path.abspath(os.path.join(certpath, './cacert.pem'))
			cert = os.path.abspath(os.path.join(certpath, './cert1.pem'))
			keyf = os.path.abspath(os.path.join(certpath, './key1.pem'))

			try:
				assert os.path.exists(caCert), "No certificates found on path '%s'" % caCert
				assert os.path.exists(cert), "No certificates found on path '%s'" % cert
				assert os.path.exists(keyf), "No certificates found on path '%s'" % keyf
				break
			except AssertionError:
				pass


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
		self.log.info("Received data size: %s bytes.", len(ret))
		return ret


	def __del__(self):
		self.close()

	def close(self):
		if self.connector:
			self.connector.stop()
			self.connector = None

	def putRow(self, row):

		message = {
			"nu_release" : {
				"seriesname"       : row.seriesname,
				"releaseinfo"      : row.releaseinfo,
				"groupinfo"        : row.groupinfo,
				"referrer"         : row.referrer,
				"outbound_wrapper" : row.outbound_wrapper,
				"actual_target"    : row.actual_target,
				"addtime"          : row.addtime.isoformat(),
			}
		}
		msg = json.dumps(message)
		self.put_item(msg)

