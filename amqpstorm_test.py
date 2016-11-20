
import urllib.parse
import logging
import threading
import time
import ssl
import os.path

import amqpstorm

DIE = False

import settings


def getSslOpts():
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

class AmqpContainer(object):
	def __init__(self):

		self.log = logging.getLogger("Main.Connector")

		self.log.info("Initializing AMQP connection.")

		sslopts = getSslOpts()

		# 'hostname': hostname,
		# 'username': username,
		# 'password': password,
		# 'port': port,
		# 'virtual_host': kwargs.get('virtual_host', '/'),
		# 'heartbeat': kwargs.get('heartbeat', 60),
		# 'timeout': kwargs.get('timeout', 30),
		# 'ssl': kwargs.get('ssl', False),
		# 'ssl_options': kwargs.get('ssl_options', {})
		self.connection = amqpstorm.Connection(
				hostname     = settings.RPC_RABBIT_SRVER.split(":")[0],
				username     = settings.RPC_RABBIT_LOGIN,
				password     = settings.RPC_RABBIT_PASWD,
				port         = int(settings.RPC_RABBIT_SRVER.split(":")[1]),
				virtual_host = settings.RPC_RABBIT_VHOST,
				heartbeat    = 15,
				timeout      = 30,
				ssl          = True,
				ssl_options  = {
					'ca_certs'           : sslopts['ca_certs'],
					'certfile'             : sslopts['certfile'],
					'keyfile'              : sslopts['keyfile'],
				}
			)

		print("Connection Established!")
		print("Connection: ", self.connection)

		self.storm_channel = self.connection.channel()
		self.storm_channel.basic.qos(10)
		self.log.info("Connection established. Setting up consumer.")


		self.storm_channel.exchange.declare(
					exchange="test_resp_enchange.e",
					exchange_type="direct",
					durable=False,
					auto_delete=True
				)


		self.log.info("Configuring queues.")

		self.storm_channel.queue.declare('test_resp_queue.q',
					durable=False,
					auto_delete=True)
		self.log.info("Declared.")

		self.storm_channel.queue.bind(queue='test_resp_queue.q', exchange="test_resp_enchange.e", routing_key='test_resp_queue')


		self.keepalive_exchange_name = "keepalive_exchange"+str(id("wat"))

		self.storm_channel.exchange.declare(
					exchange=self.keepalive_exchange_name,
					durable=False,
					auto_delete=True)

		self.storm_channel.queue.declare(
					queue=self.keepalive_exchange_name+'.nak.q',
					durable=False,
					auto_delete=True)

		self.storm_channel.queue.bind(
					queue=self.keepalive_exchange_name+'.nak.q',
					exchange=self.keepalive_exchange_name,
					routing_key="nak")


		self.log.info("Bound.")
		self.storm_channel.basic.consume(self.process_rx, 'test_resp_queue.q', no_ack=False)
		self.storm_channel.basic.consume(self.process_rx, self.keepalive_exchange_name+'.nak.q', no_ack=False)
		self.log.info("Consume triggered.")

		self.prefetch_extended = False
		self.storm_channel.basic.qos(1, global_=True)

		self.log.info("Starting thread")

		self.tx_thread_1 = threading.Thread(target=self.fill_queue_1)
		self.tx_thread_1.start()
		self.tx_thread_2 = threading.Thread(target=self.fill_queue_2)
		self.tx_thread_2.start()

		try:
			self.log.info("Consuming.")
			while 1:
				self.storm_channel.process_data_events(to_tuple=False)
				print("Loopin!")
				time.sleep(1)
			self.close()
		except KeyboardInterrupt:
			self.close()

		# self.in_q  = rabbitpy.Queue(self.channel, name="test_resp_queue.q", durable=False,  auto_delete=False)
		# self.in_q.declare()
		# self.in_q.bind(resp_exchange, routing_key="test_resp_queue")




	def process_rx(self, message):
		print("received message!", message)
		print("message body:", message.body)
		message.ack()



		if self.prefetch_extended is False:
			self.prefetch_extended = True
			self.storm_channel.basic.qos(50, global_=True)
			self.log.info("Prefetch updated")



	def poke_keepalive(self):
		self.storm_channel.basic.publish(body='wat', exchange=self.keepalive_exchange_name, routing_key='nak',
			properties={
				'correlation_id' : "keepalive"
			})


	def fill_queue_1(self):
		while not DIE:
			print("Putting message")

			# channel.basic.publish(body='Hello World!',
			# 					  routing_key='simple_queue')
			try:
				self.storm_channel.basic.publish(exchange="test_resp_enchange.e", body='test?', routing_key="test_resp_queue")
				self.storm_channel.basic.publish(exchange="test_resp_enchange.e", body='test?', routing_key="test_resp_queue")
				time.sleep(3)
			except amqpstorm.AMQPError as why:
				self.log.error("Exception in publish!")
				self.log.error(why)
				self.storm_channel.stop_consuming()
				return
			time.sleep(0.1)

	def fill_queue_2(self):
		while not DIE:
			print("Putting message")

			# channel.basic.publish(body='Hello World!',
			# 					  routing_key='simple_queue')
			try:
				self.poke_keepalive()
				self.poke_keepalive()
				time.sleep(3)
			except amqpstorm.AMQPError as why:
				self.log.error("Exception in publish!")
				self.log.error(why)
				self.storm_channel.stop_consuming()
				return
			time.sleep(0.1)


	def close(self):
		print("Joining")
		print("Closing connection")
		global DIE
		DIE = True
		self.tx_thread_1.join()
		self.tx_thread_2.join()
		self.connection.close()
		print("Closed")

		self.connection.close()




def test():
	import sys
	import os.path
	logging.basicConfig(level=logging.INFO)
	# test_disconnect()

	tester = AmqpContainer()


if __name__ == "__main__":
	test()


