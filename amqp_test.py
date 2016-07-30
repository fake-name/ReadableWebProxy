
import urllib.parse
import logging
import threading
import pickle
import time
import json
import logging
import ssl
import os.path
import LocalAmqpConnector

import amqpstorm
import logSetup

DIE = False

class AmqpContainer(object):
	def __init__(self):

		self.log = logging.getLogger("Main.Connector")

		self.log.info("Initializing AMQP connection.")

		config = json.load(open("test_conf.json"))
		self.config = config

		# qs = urllib.parse.urlencode({
		# 	'cacertfile'           : self.config['sslopts']['ca_certs'],
		# 	'certfile'             : self.config['sslopts']['certfile'],
		# 	'keyfile'              : self.config['sslopts']['keyfile'],

		# 	'verify'               : 'ignore',
		# 	'heartbeat'            : 15,

		# 	'connection_timeout'   : 60,

		# 	})

		# uri = '{scheme}://{username}:{password}@{host}:{port}/{virtual_host}?{query_str}'.format(
		# 	scheme       = 'amqps',
		# 	username     = self.config['userid'],
		# 	password     = self.config['password'],
		# 	host         = self.config['host'].split(":")[0],
		# 	port         = self.config['host'].split(":")[1],
		# 	virtual_host = self.config['vhost'],
		# 	query_str    = qs,
		# 	)


		assert 'task_queue_name'          in config
		assert 'response_queue_name'      in config
		assert 'task_exchange'            in config
		assert 'task_exchange_type'       in config
		assert 'response_exchange'        in config
		assert 'response_exchange_type'   in config
		assert 'durable'                  in config
		assert 'prefetch'                 in config
		assert 'flush_queues'             in config
		assert 'hearbeat_packet_timeout'  in config

		self.log.info("Connection configuration:")
		for key, value in config.items():
			self.log.info("	%s -> %s", key, value)

		self.keepalive_exchange_name = "keepalive_exchange"+str(id("wat"))
		self.hearbeat_packet_timeout = config['hearbeat_packet_timeout']

		self.task_exchange   = config['task_exchange']
		self.task_queue_name = config['task_queue_name']
		self.durable         = config['durable']

		self.log.info("Initializing AMQP connection.")

		conn_params = {
				'hostname'     : self.config['host'].split(":")[0],
				'username'     : self.config['userid'],
				'password'     : self.config['password'],
				'port'         : int(self.config['host'].split(":")[1]),
				'virtual_host' : self.config['virtual_host'],
				'heartbeat'    : self.config['socket_timeout'] // 2,
				'timeout'      : self.config['socket_timeout'],
				'ssl'          : True,
				'ssl_options'  : {
					'ca_certs'           : self.config['sslopts']['ca_certs'],
					'certfile'             : self.config['sslopts']['certfile'],
					'keyfile'              : self.config['sslopts']['keyfile'],
				}
			}

		self.storm_connection = amqpstorm.Connection(**conn_params)

		self.log.info("Connection established. Setting up consumer.")
		self.storm_channel = self.storm_connection.channel(rpc_timeout=conn_params['timeout'])

		# Initial QoS is tiny, throttle it up after everything is actually running.
		self.storm_channel.basic.qos(1, global_=True)

		self.last_hearbeat_received = time.time()
		self.last_message_received = time.time()

		self.rx_timeout_lock        = threading.Lock()
		self.heartbeat_timeout_lock = threading.Lock()
		self.active_lock            = threading.Lock()


		self.log.info("Configuring queues.")


		self.storm_channel.exchange.declare(
					exchange=config['task_exchange'],
					exchange_type=config['task_exchange_type'],
					durable=config['durable']
				)

		self.storm_channel.exchange.declare(
					exchange=config['response_exchange'],
					exchange_type=config['response_exchange_type'],
					durable=config['durable']
				)

		# # "NAK" queue, used for keeping the event loop ticking when we
		# # purposefully do not want to receive messages
		# # THIS IS A SHITTY WORKAROUND for keepalive issues.

		self.storm_channel.exchange.declare(
					exchange=self.keepalive_exchange_name,
					durable=False,
					auto_delete=True)

		self.storm_channel.queue.declare(
					queue=config['response_queue_name'],
					durable=config['durable'],
					auto_delete=False)
		self.log.info("Declared.")

		self.storm_channel.queue.bind(
					queue=config['response_queue_name'],
					exchange=config['response_exchange'],
					routing_key=config['response_queue_name'].split(".")[0])

		self.log.info("Bound.")

		self.log.info("Triggering consume from %s", config['response_queue_name'])
		self.storm_channel.basic.consume(self.handle_normal_rx, queue=config['response_queue_name'],         no_ack=False)
		self.log.info("Consume triggered.")

	def enter_blocking_rx_loop(self):
		self.storm_channel.start_consuming(to_tuple=False)

	def handle_normal_rx(self, message):

		with self.rx_timeout_lock:
			self.last_message_received = time.time()
		# self.rx_queue.put(message.body)
		message.ack()

		self.log.info("Message packet received! %s", len(message.body))
		with open("msg %s.json" % time.time(), "wb")  as fp:
			fp.write(pickle.dumps(message.body))

		self.close()

	def close(self):

		self.log.info("Killing connection")
		self.storm_connection.kill()
		self.storm_channel.kill()


# def test_disconnect():

# 	config = json.load(open("test_conf.json"))

# 	qs = urllib.parse.urlencode({
# 		'cacertfile'           : config['sslopts']['ca_certs'],
# 		'certfile'             : config['sslopts']['certfile'],
# 		'keyfile'              : config['sslopts']['keyfile'],

# 		'verify'               : 'ignore',
# 		'heartbeat'            : 15,

# 		'connection_timeout'   : 60,

# 		})

# 	uri = '{scheme}://{username}:{password}@{host}:{port}/{virtual_host}?{query_str}'.format(
# 		scheme       = 'amqps',
# 		username     = config['userid'],
# 		password     = config['password'],
# 		host         = config['host'].split(":")[0],
# 		port         = config['host'].split(":")[1],
# 		virtual_host = config['vhost'],
# 		query_str    = qs,
# 		)


# 	connection = rabbitpy.Connection(uri)
# 	print("Connected. Connection: ", connection)
# 	time.sleep(5)
# 	print("Closing")
# 	connection.close()

def test_basic():


	tester = AmqpContainer()


	thread = threading.Thread(target=tester.enter_blocking_rx_loop, daemon=True)
	thread.start()
	wait_time = 120
	for x in range(wait_time):
		time.sleep(1)
		print("Sleeping: ", wait_time-x)

	tester.close()


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

def test_direct():

	logPath = 'Main.Feeds.RPC'

	log = logging.getLogger(logPath)
	log.info("RPC Management class instantiated.")

	settings = json.load(open("test_conf.json"))

	# Require clientID in settings
	assert "userid"       in settings
	assert "password"       in settings
	assert "host"       in settings
	assert "virtual_host"       in settings

	assert "task_queue_name"         in settings
	assert "response_queue_name"     in settings

	sslopts = getSslOpts()
	connector = LocalAmqpConnector.Connector(userid            = settings["userid"],
											password           = settings["password"],
											host               = settings["host"],
											virtual_host       = settings["virtual_host"],
											ssl                = sslopts,
											master             = True,
											synchronous        = False,
											flush_queues       = False,
											prefetch           = 25,
											durable            = True,
											heartbeat          = 240,
											task_exchange_type = 'direct',
											poll_rate          = 1.0/100,
											task_queue         = settings["task_queue_name"],
											response_queue     = settings["response_queue_name"],
											)


	log.info("Connected AMQP Interface: %s", connector)
	log.info("Connection parameters: %s, %s, %s, %s", settings["userid"], settings["password"], settings["host"], settings["virtual_host"])


	wait_time = 120
	for x in range(wait_time):
		time.sleep(1)
		print("Sleeping: ", wait_time-x)

	connector.stop()


if __name__ == "__main__":
	logSetup.initLogging(logLevel=logging.DEBUG)

	test_basic()
	# test_disconnect()
	# test_direct()



