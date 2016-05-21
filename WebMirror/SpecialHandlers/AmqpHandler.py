
#!/usr/bin/env python3
import AmqpConnector
import logging
import os.path
import ssl
import time


class RabbitQueueHandler(object):
	die = False

	def __init__(self, settings):

		logPath = 'Main.Feeds.RPC'

		self.log = logging.getLogger(logPath)
		self.log.info("RPC Management class instantiated.")


		# Require clientID in settings
		assert "RPC_RABBIT_LOGIN"       in settings
		assert "RPC_RABBIT_PASWD"       in settings
		assert "RPC_RABBIT_SRVER"       in settings
		assert "RPC_RABBIT_VHOST"       in settings

		sslopts = self.getSslOpts()

		self.connector = AmqpConnector.Connector(userid            = settings["RPC_RABBIT_LOGIN"],
												password           = settings["RPC_RABBIT_PASWD"],
												host               = settings["RPC_RABBIT_SRVER"],
												virtual_host       = settings["RPC_RABBIT_VHOST"],
												ssl                = sslopts,
												master             = True,
												synchronous        = False,
												flush_queues       = False,
												prefetch           = 25,
												durable            = True,
												task_exchange_type = "direct",
												task_queue         = 'task.master.q',
												response_queue     = 'response.master.q',
												)


		self.log.info("Connected AMQP Interface: %s", self.connector)
		self.log.info("Connection parameters: %s, %s, %s, %s", settings["RPC_RABBIT_LOGIN"], settings["RPC_RABBIT_PASWD"], settings["RPC_RABBIT_SRVER"], settings["RPC_RABBIT_VHOST"])

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
		self.log.info("Received data size: %s bytes.", len(ret))
		return ret


	def __del__(self):
		self.close()

	def close(self):
		if self.connector:
			self.connector.stop()
			self.connector = None

if __name__ == '__main__':
	import logSetup
	logSetup.initLogging()

	import config


	amqp_settings = {
		"RPC_RABBIT_LOGIN" : config.C_RPC_RABBIT_LOGIN,
		"RPC_RABBIT_PASWD" : config.C_RPC_RABBIT_PASWD,
		"RPC_RABBIT_SRVER" : config.C_RPC_RABBIT_SRVER,
		"RPC_RABBIT_VHOST" : config.C_RPC_RABBIT_VHOST,
	}

	amqpint = RabbitQueueHandler(amqp_settings)
	print(amqpint)

	while 1:
		try:
			time.sleep(1)
		except KeyboardInterrupt:
			break

	try:
		amqpint.close()
	except ValueError:
		pass


