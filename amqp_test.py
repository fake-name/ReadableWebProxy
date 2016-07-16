
# import urllib.parse
# import logging
# import threading
# import time
# import json

# import rabbitpy

# DIE = False

# class AmqpContainer(object):
# 	def __init__(self):

# 		self.log = logging.getLogger("Main.Connector")

# 		self.log.info("Initializing AMQP connection.")

# 		self.config = json.load(open("test_conf.json"))

# 		qs = urllib.parse.urlencode({
# 			'cacertfile'           : self.config['sslopts']['ca_certs'],
# 			'certfile'             : self.config['sslopts']['certfile'],
# 			'keyfile'              : self.config['sslopts']['keyfile'],

# 			'verify'               : 'ignore',
# 			'heartbeat'            : 15,

# 			'connection_timeout'   : 60,

# 			})

# 		uri = '{scheme}://{username}:{password}@{host}:{port}/{virtual_host}?{query_str}'.format(
# 			scheme       = 'amqps',
# 			username     = self.config['userid'],
# 			password     = self.config['password'],
# 			host         = self.config['host'].split(":")[0],
# 			port         = self.config['host'].split(":")[1],
# 			virtual_host = self.config['vhost'],
# 			query_str    = qs,
# 			)


# 		self.connection = rabbitpy.Connection(uri)

# 		self.channel = self.connection.channel()
# 		self.log.info("Connection established. Setting up consumer.")


# 		self.log.info("Configuring queues.")


# 		resp_exchange = rabbitpy.Exchange(
# 					self.channel,
# 					name="test_resp_enchange.e",
# 					exchange_type="direct",
# 					durable=False
# 				)
# 		resp_exchange.declare()

# 		self.in_q  = rabbitpy.Queue(self.channel, name="test_resp_queue.q", durable=False,  auto_delete=False)
# 		self.in_q.declare()
# 		self.in_q.bind(resp_exchange, routing_key="test_resp_queue")


# 		print("Starting thread")
# 		self.rx_thread = threading.Thread(target=self.get_rx)
# 		self.tx_thread = threading.Thread(target=self.fill_queue)

# 		self.rx_thread.start()
# 		self.tx_thread.start()


# 	def get_rx(self):
# 		print("Get_rx call()")
# 		for item in self.in_q:
# 			print("Item: ", item.body)
# 			item.ack()

# 		print("Consumer exited!")

# 	def fill_queue(self):
# 		while not DIE:
# 			print("Putting message")
# 			rabbitpy.Message(self.channel, body_value="test?").publish(exchange="test_resp_enchange.e", routing_key="test_resp_queue")
# 			# self.channel.basic_publish(exchange="test_resp_enchange.e", body='test?', routing_key="test_resp_queue")
# 			time.sleep(0.1)

# 	def interrupt(self):
# 		self.in_q.stop_consuming()

# 	def close(self):
# 		print("Joining")
# 		self.rx_thread.join(0)
# 		print("Closing connection")
# 		global DIE
# 		DIE = True
# 		self.tx_thread.join()
# 		self.connection.close()
# 		print("Closed")




import urllib.parse
import logging
import threading
import time
import json

import rabbitpy

def test_disconnect():

	config = json.load(open("test_conf.json"))

	qs = urllib.parse.urlencode({
		'cacertfile'           : config['sslopts']['ca_certs'],
		'certfile'             : config['sslopts']['certfile'],
		'keyfile'              : config['sslopts']['keyfile'],

		'verify'               : 'ignore',
		'heartbeat'            : 15,

		'connection_timeout'   : 60,

		})

	uri = '{scheme}://{username}:{password}@{host}:{port}/{virtual_host}?{query_str}'.format(
		scheme       = 'amqps',
		username     = config['userid'],
		password     = config['password'],
		host         = config['host'].split(":")[0],
		port         = config['host'].split(":")[1],
		virtual_host = config['vhost'],
		query_str    = qs,
		)


	connection = rabbitpy.Connection(uri)
	time.sleep(5)
	connection.close()

def test():
	import sys
	import os.path
	logging.basicConfig(level=logging.INFO)
	test_disconnect()

	# tester = AmqpContainer()
	# time.sleep(5)
	# tester.interrupt()
	# time.sleep(3)
	# tester.close()


if __name__ == "__main__":
	test()


