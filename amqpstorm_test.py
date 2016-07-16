
import urllib.parse
import logging
import threading
import time
import json

import amqpstorm

DIE = False

class AmqpContainer(object):
	def __init__(self):

		self.log = logging.getLogger("Main.Connector")

		self.log.info("Initializing AMQP connection.")

		self.config = json.load(open("test_conf.json"))



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
				hostname     = self.config['host'].split(":")[0],
				username     = self.config['userid'],
				password     = self.config['password'],
				port         = int(self.config['host'].split(":")[1]),
				virtual_host = self.config['vhost'],
				heartbeat    = 15,
				timeout      = 30,
				ssl          = True,
				ssl_options  = {
					'ca_certs'           : self.config['sslopts']['ca_certs'],
					'certfile'             : self.config['sslopts']['certfile'],
					'keyfile'              : self.config['sslopts']['keyfile'],
				}
			)

		print("Connection Established!")
		print("Connection: ", self.connection)

		self.channel = self.connection.channel()
		self.channel.basic.qos(10)
		self.log.info("Connection established. Setting up consumer.")


		self.channel.exchange.declare(
					exchange="test_resp_enchange.e",
					exchange_type="direct",
					durable=False,
					auto_delete=True
				)


		self.log.info("Configuring queues.")

		self.channel.queue.declare('test_resp_queue.q',
					durable=False,
					auto_delete=True)
		self.log.info("Declared.")

		self.channel.queue.bind(queue='test_resp_queue.q', exchange="test_resp_enchange.e", routing_key='test_resp_queue')
		self.log.info("Bound.")
		self.channel.basic.consume(self.process_rx, 'test_resp_queue.q', no_ack=False)
		self.log.info("Consume triggered.")

		self.log.info("Starting thread")
		self.tx_thread = threading.Thread(target=self.fill_queue)

		self.tx_thread.start()

		try:
			self.log.info("Consuming.")
			self.channel.start_consuming(to_tuple=False)
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

	def fill_queue(self):
		while not DIE:
			print("Putting message")

			# channel.basic.publish(body='Hello World!',
			# 					  routing_key='simple_queue')
			try:
				self.channel.basic.publish(exchange="test_resp_enchange.e", body='test?', routing_key="test_resp_queue")
			except amqpstorm.AMQPError as why:
				self.log.error("Exception in publish!")
				self.log.error(why)
				self.channel.stop_consuming()
				return
			time.sleep(0.1)

	def interrupt(self):
		self.in_q.stop_consuming()

	def close(self):
		print("Joining")
		print("Closing connection")
		global DIE
		DIE = True
		self.tx_thread.join()
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


