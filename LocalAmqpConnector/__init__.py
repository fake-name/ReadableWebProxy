
import rabbitpy
import urllib.parse
import socket
import traceback
import logging
import threading
import multiprocessing
import queue
import time

class Heartbeat_Timeout_Exception(Exception):
	pass

class ConnectorManager:
	def __init__(self, config, runstate, active, task_queue, response_queue):

		assert 'host'                     in config
		assert 'userid'                   in config
		assert 'password'                 in config
		assert 'virtual_host'             in config
		assert 'task_queue_name'          in config
		assert 'response_queue_name'      in config
		assert 'task_exchange'            in config
		assert 'task_exchange_type'       in config
		assert 'response_exchange'        in config
		assert 'response_exchange_type'   in config
		assert 'master'                   in config
		assert 'synchronous'              in config
		assert 'flush_queues'             in config
		assert 'heartbeat'                in config
		assert 'sslopts'                  in config
		assert 'poll_rate'                in config
		assert 'prefetch'                 in config
		assert 'session_fetch_limit'      in config
		assert 'durable'                  in config
		assert 'socket_timeout'           in config
		assert 'hearbeat_packet_interval' in config
		assert 'hearbeat_packet_timeout'  in config
		assert 'ack_rx'                   in config


		self.log = logging.getLogger("Main.Connector.Internal(%s)" % config['virtual_host'])
		self.runstate           = runstate
		self.config             = config
		self.task_queue         = task_queue
		self.active_connections = active
		self.response_queue     = response_queue


		self.session_fetched        = 0
		self.queue_fetched          = 0
		self.active                 = 0
		self.last_hearbeat_sent     = time.time()
		self.last_hearbeat_received = time.time()

		self.sent_messages = 0
		self.recv_messages = 0

		self.connection     = None
		self.channel        = None

		self.keepalive_exchange_name = "keepalive_exchange"+str(id("wat"))

		self.delivered = 0

		self._connect()


		if self.config['master']:
			self.in_queue = self.config['response_queue_name']
		else:
			self.in_queue = self.config['task_queue_name']


		self.in_q = rabbitpy.Queue(self.connection.channel(), self.in_queue)


		self.rx_thread = threading.Thread(target=self._processReceiving, daemon=False)
		self.rx_thread.start()

		self.active_lock = threading.Lock()


		# config = {
		# 	'host'                   : kwargs.get('host',                   None),
		# 	'userid'                 : kwargs.get('userid',                 'guest'),
		# 	'password'               : kwargs.get('password',               'guest'),
		# 	'virtual_host'           : kwargs.get('virtual_host',           '/'),
		# 	'task_queue_name'             : kwargs.get('task_queue_name',             'task.q'),
		# 	'response_queue_name'         : kwargs.get('response_queue_name',         'response.q'),
		# 	'task_exchange'          : kwargs.get('task_exchange',          'tasks.e'),
		# 	'task_exchange_type'     : kwargs.get('task_exchange_type',     'direct'),
		# 	'response_exchange'      : kwargs.get('response_exchange',      'resps.e'),
		# 	'response_exchange_type' : kwargs.get('response_exchange_type', 'direct'),
		# 	'master'                 : kwargs.get('master',                 False),
		# 	'synchronous'            : kwargs.get('synchronous',            True),
		# 	'flush_queues'           : kwargs.get('flush_queues',           False),
		# 	'heartbeat'              : kwargs.get('heartbeat',              60*5),
		# 	'ssl'                    : kwargs.get('ssl',                    None),
		# 	'poll_rate'              : kwargs.get('poll_rate',              0.25),
		# 	'prefetch'               : kwargs.get('prefetch',               1),
		# 	'session_fetch_limit'    : kwargs.get('session_fetch_limit',    None),
		# 	'durable'                : kwargs.get('durable',                False),
		# 	'socket_timeout'         : kwargs.get('socket_timeout',         10),
		# }

	def __del__(self):
		try:
			self.close()
		except Exception:
			pass

		# Force everything closed, because we seem to have two instances somehow
		self.connection     = None
		self.channel        = None
		self.config         = None
		self.runstate       = None
		self.task_queue     = None
		self.response_queue = None

		# Finally, deincrement the active count
		self.active_connections.value = 0

		if hasattr(self, "rx_thread"):
			self.rx_thread.join()

	def _connect(self):

		assert self.active_connections.value == 0
		self.active_connections.value = 1

		self.log.info("Initializing AMQP connection.")
		# Connect to server
		# self.connection = amqp.connection.Connection(host           = self.config['host'],
		# 											userid          = self.config['userid'],
		# 											password        = self.config['password'],
		# 											virtual_host    = self.config['virtual_host'],
		# 											heartbeat       = self.config['heartbeat'],
		# 											ssl             = self.config['sslopts'],
		# 											connect_timeout = self.config['socket_timeout'],
		# 											read_timeout    = self.config['socket_timeout'],
		# 											write_timeout   = self.config['socket_timeout'])

		# "cert_reqs" : ssl.CERT_REQUIRED,
		# "ca_certs" : caCert,
		# "keyfile"  : keyf,
		# "certfile"  : cert,

		qs = urllib.parse.urlencode({
			'cacertfile'           :self.config['sslopts']['ca_certs'],
			'certfile'             :self.config['sslopts']['certfile'],
			'keyfile'              :self.config['sslopts']['keyfile'],

			'verify'               : 'ignore',
			'heartbeat'            : self.config['heartbeat'],

			'connection_timeout'   : self.config['socket_timeout'],

			})

		uri = '{scheme}://{username}:{password}@{host}:{port}/{virtual_host}?{query_str}'.format(
			scheme       = 'amqps',
			username     = self.config['userid'],
			password     = self.config['password'],
			host         = self.config['host'].split(":")[0],
			port         = self.config['host'].split(":")[1],
			virtual_host = self.config['virtual_host'],
			query_str    = qs,
			)
		self.connection = rabbitpy.Connection(uri)

		# self.connection.connect()

		# Channel and exchange setup
		self.channel = rabbitpy.AMQP(self.connection.channel(blocking_read = True))
		self.channel.basic_qos(
				prefetch_size  = 0,
				prefetch_count = self.config['prefetch'],
				global_flag    = False
			)


		self.log.info("Connection established. Setting up consumer.")

		if self.config['flush_queues']:
			self.log.info("Flushing items in queue.")
			self.channel.queue_purge(self.config['task_queue_name'])
			self.channel.queue_purge(self.config['response_queue_name'])

		self.log.info("Configuring queues.")
		self._setupQueues()


		self.no_ack = not self.config['ack_rx']



	def _setupQueues(self):

		self.channel.exchange_declare(self.config['task_exchange'],     exchange_type=self.config['task_exchange_type'],     auto_delete=False, durable=self.config['durable'])
		self.channel.exchange_declare(self.config['response_exchange'], exchange_type=self.config['response_exchange_type'], auto_delete=False, durable=self.config['durable'])

		# set up consumer and response queues
		if self.config['master']:
			# Master has to declare the response queue so it can listen for responses
			self.channel.queue_declare(self.config['response_queue_name'], auto_delete=False, durable=self.config['durable'])
			self.channel.queue_bind(   self.config['response_queue_name'], exchange=self.config['response_exchange'], routing_key=self.config['response_queue_name'].split(".")[0])
			self.log.info("Binding queue %s to exchange %s.", self.config['response_queue_name'], self.config['response_exchange'])

		if not self.config['master']:
			# Clients need to declare their task queues, so the master can publish into them.
			self.channel.queue_declare(self.config['task_queue_name'], auto_delete=False, durable=self.config['durable'])
			self.channel.queue_bind(   self.config['task_queue_name'], exchange=self.config['task_exchange'], routing_key=self.config['task_queue_name'].split(".")[0])
			self.log.info("Binding queue %s to exchange %s.", self.config['task_queue_name'], self.config['task_exchange'])

		# "NAK" queue, used for keeping the event loop ticking when we
		# purposefully do not want to receive messages
		# THIS IS A SHITTY WORKAROUND for keepalive issues.
		self.channel.exchange_declare(self.keepalive_exchange_name, exchange_type="direct", auto_delete=True, durable=False, arguments={"x-expires" : 5*60*1000})
		self.channel.queue_declare('nak.q', auto_delete=False, durable=False)
		self.channel.queue_bind('nak.q',    exchange=self.keepalive_exchange_name, routing_key="nak")



	def poll(self):
		'''
		Internal function.
		Polls the AMQP interface, processing any messages received on it.
		Received messages are ack-ed, and then placed into the appropriate local queue.
		messages in the outgoing queue are transmitted.

		NOTE: Maximum throughput is 4 messages-second, limited by the internal poll-rate.
		'''

		# _connect() is called in _poll_proxy before _poll is called, so
		# we /should/ be connected by the time this point is reached. In any
		# event, it should fine even if that is somehow not true, since
		# the interface calls should
		connected = True


		print_time = 15              # Print a status message every n seconds
		integrator = 0               # Time since last status message emitted.
		loop_delay = self.config['poll_rate']  # Poll interval for queues.

		# When run is false, don't halt until
		# we've flushed the outgoing items out the queue
		while self.runstate.value or self.response_queue.qsize():

			if not connected:
				self._connect()
				connected = True

			time.sleep(loop_delay)

			self._publishOutgoing()
			# Reset the print integrator.
			if integrator > print_time:
				integrator = 0
				with self.active_lock:
					self.log.info("AMQP Interface process. Current message counts: %s (out: %s, in: %s)", self.active, self.sent_messages, self.recv_messages)
			integrator += loop_delay

		self.log.info("AMQP Thread Exiting")
		self.close()

	def close(self):
		# Stop the flow of new items
		self.channel.basic_qos(
				prefetch_size  = 0,
				prefetch_count = 0,
				global_flag    = False
			)

		# Close the connection once it's empty.
		try:
			self.in_q.stop_consuming()
			self.connection.close()
		except rabbitpy.exceptions.RabbitpyException as e:
			# We don't really care about exceptions on teardown
			self.log.error("Error on interface teardown!")
			self.log.error("	%s", e)
			# for line in traceback.format_exc().split('\n'):
			# 	self.log.error(line)

		self.log.info("AMQP Thread exited")

	def _processReceiving(self):
		for item in self.in_q:
			# Prevent never breaking from the loop if the feeding queue is backed up.

			if item:
				self.log.info("Received packet from queue '%s'! Processing.", self.in_queue)
				self.task_queue.put(item.body)

				with self.active_lock:
					self.active += 1
					self.recv_messages += 1
					self.session_fetched += 1

				item.ack()

				while self.task_queue.qsize() > self.config['prefetch']:
					time.sleep(1)

				if self.atFetchLimit():
					self.log.info("Session fetch limit reached. Not fetching any additional content.")
					break


	def _publishOutgoing(self):
		if self.config['master']:
			out_queue = self.config['task_exchange']
			out_key   = self.config['task_queue_name'].split(".")[0]
		else:
			out_queue = self.config['response_exchange']
			out_key   = self.config['response_queue_name'].split(".")[0]

		while 1:
			try:
				put = self.response_queue.get_nowait()
				# self.log.info("Publishing message of len '%0.3f'K to exchange '%s'", len(put)/1024, out_queue)
				# message = amqp.basic_message.Message(body=put)
				msg_prop = {}
				if self.config['durable']:
					msg_prop["delivery_mode"] = 2
				self.channel.basic_publish(body=put, exchange=out_queue, routing_key=out_key, properties=msg_prop)
				with self.active_lock:
					self.sent_messages += 1
					self.active -= 1

			except queue.Empty:
				break

	def atFetchLimit(self):
		'''
		Track the fetch-limit for the active session. Used to allow an instance to connect,
		fetch one (and only one) item, and then do things with the fetched item without
		having the background thread fetch and queue a bunch more items while it's working.
		'''
		if not self.config['session_fetch_limit']:
			return False

		return self.session_fetched >= self.config['session_fetch_limit']



def run_fetcher(config, runstate, tx_q, rx_q):
	'''
	bleh

	'''

	# Active instances tracker
	active = multiprocessing.Value("i", 0)

	log = logging.getLogger("Main.Connector.Manager")

	log.info("Worker thread starting up.")
	connection = False
	while runstate.value != 0:
		try:
			if connection is False:
				connection = ConnectorManager(config, runstate, active, tx_q, rx_q)
			connection.poll()

		except Exception:
			log.error("Exception in connector! Terminating connection...")
			for line in traceback.format_exc().split('\n'):
				log.error(line)
			try:
				del connection
			except Exception:
				log.info("")
				log.error("Failed pre-emptive closing before reconnection. May not be a problem?")
				for line in traceback.format_exc().split('\n'):
					log.error(line)
			if runstate.value != 0:
				connection = False
				log.error("Triggering reconnection...")


	log.info("")
	log.info("Worker thread has terminated.")
	log.info("")

class Connector:

	def __init__(self, *args, **kwargs):

		assert args == (), "All arguments must be passed as keyword arguments. Positional arguments: '%s'" % (args, )

		self.log = logging.getLogger("Main.Connector")

		self.log.info("Setting up AqmpConnector!")

		config = {
			'host'                     : kwargs.get('host',                     None),
			'userid'                   : kwargs.get('userid',                   'guest'),
			'password'                 : kwargs.get('password',                 'guest'),
			'virtual_host'             : kwargs.get('virtual_host',             '/'),
			'task_queue_name'          : kwargs.get('task_queue',               'task.q'),
			'response_queue_name'      : kwargs.get('response_queue',           'response.q'),
			'task_exchange'            : kwargs.get('task_exchange',            'tasks.e'),
			'task_exchange_type'       : kwargs.get('task_exchange_type',       'direct'),
			'response_exchange'        : kwargs.get('response_exchange',        'resps.e'),
			'response_exchange_type'   : kwargs.get('response_exchange_type',   'direct'),
			'master'                   : kwargs.get('master',                   False),
			'synchronous'              : kwargs.get('synchronous',              True),
			'flush_queues'             : kwargs.get('flush_queues',             False),
			'heartbeat'                : kwargs.get('heartbeat',                 120),
			'sslopts'                  : kwargs.get('ssl',                      None),
			'poll_rate'                : kwargs.get('poll_rate',                  0.25),
			'prefetch'                 : kwargs.get('prefetch',                   1),
			'session_fetch_limit'      : kwargs.get('session_fetch_limit',      None),
			'durable'                  : kwargs.get('durable',                  False),
			'socket_timeout'           : kwargs.get('socket_timeout',            10),

			'hearbeat_packet_interval' : kwargs.get('hearbeat_packet_interval',  10),
			'hearbeat_packet_timeout'  : kwargs.get('hearbeat_packet_timeout',  120),
			'ack_rx'                   : kwargs.get('ack_rx',                   True),
		}

		self.log.info("Fetch limit: '%s'", config['session_fetch_limit'])
		self.log.info("Comsuming from queue '%s', emitting responses on '%s'.", config['task_queue_name'], config['response_queue_name'])

		# Validity-Check args
		if not config['host']:
			raise ValueError("You must specify a host to connect to!")

		assert        config['task_queue_name'].endswith(".q") is True
		assert    config['response_queue_name'].endswith(".q") is True
		assert     config['task_exchange'].endswith(".e") is True
		assert config['response_exchange'].endswith(".e") is True

		# Patch in the port number to the host name if it's not present.
		# This is really clumsy, but you can't explicitly specify the port
		# in the amqp library
		if not ":" in config['host']:
			if config['ssl']:
				config['host'] += ":5671"
			else:
				config['host'] += ":5672"

		self.session_fetch_limit = config['session_fetch_limit']
		self.queue_fetched       = 0
		self.queue_put           = 0

		# set up the task and response queues.
		# These need to be multiprocessing queues because
		# messages can sometimes be inserted from a different process
		# then the interface is created in.
		self.taskQueue = queue.Queue()
		self.responseQueue = queue.Queue()

		self.runstate = multiprocessing.Value("b", 1)

		self.log.info("Starting AMQP interface thread.")

		self.forwarded = 0

		self.thread = None
		self.__config = config
		self.checkLaunchThread()

	def checkLaunchThread(self):
		if self.thread and self.thread.isAlive():
			return
		if self.thread and not self.thread.isAlive():
			self.thread.join()
			self.log.error("")
			self.log.error("")
			self.log.error("")
			self.log.error("Thread has died!")
			self.log.error("")
			self.log.error("")
			self.log.error("")

		self.thread = threading.Thread(target=run_fetcher, args=(self.__config, self.runstate, self.taskQueue, self.responseQueue), daemon=False)
		self.thread.start()

	def atQueueLimit(self):
		'''
		Track the fetch-limit for the active session. Used to allow an instance to connect,
		fetch one (and only one) item, and then do things with the fetched item without
		having the background thread fetch and queue a bunch more items while it's working.
		'''
		if not self.session_fetch_limit:
			return False

		return self.queue_fetched >= self.session_fetch_limit


	def getMessage(self):
		'''
		Try to fetch a message from the receiving Queue.
		Returns the method if there is one, False if there is not.
		Non-Blocking.
		'''
		self.checkLaunchThread()
		if self.atQueueLimit():
			raise ValueError("Out of fetchable items!")

		try:
			put = self.taskQueue.get_nowait()
			self.queue_fetched += 1
			self.forwarded += 1
			if self.forwarded >= 25:
				self.log.info("Fetched item from proxy queue. Total received: %s, total sent: %s", self.queue_fetched, self.queue_put)
				self.forwarded = 0
			return put
		except queue.Empty:
			return None

	def putMessage(self, message, synchronous=False):
		'''
		Place a message into the outgoing queue.

		if synchronous is true, this call will block until
		the items in the outgoing queue are less then the
		value of synchronous
		'''
		self.checkLaunchThread()
		if synchronous:
			while self.responseQueue.qsize() > synchronous:
				time.sleep(0.1)
		self.queue_put += 1
		self.responseQueue.put(message)



	def stop(self):
		'''
		Tell the AMQP interface thread to halt, and then join() on it.
		Will block until the queue has been cleanly shut down.
		'''
		self.log.info("Stopping AMQP interface thread.")
		self.runstate.value = 0
		while self.responseQueue.qsize() > 0:
			self.log.info("%s remaining outgoing AMQP items.", self.responseQueue.qsize())
			time.sleep(1)

		self.log.info("%s remaining outgoing AMQP items.", self.responseQueue.qsize())

		self.thread.join()
		self.log.info("AMQP interface thread halted.")

	def __del__(self):
		# print("deleter: ", self.runstate, self.runstate.value)
		if self.runstate.value:
			self.stop()

def test():
	import json
	import sys
	import os.path
	logging.basicConfig(level=logging.INFO)

	sPaths = ['./settings.json', '../settings.json']

	for sPath in sPaths:
		if not os.path.exists(sPath):
			continue
		with open(sPath, 'r') as fp:
			settings = json.load(fp)

	isMaster = len(sys.argv) > 1
	con = Connector(userid       = settings["RABBIT_LOGIN"],
					password     = settings["RABBIT_PASWD"],
					host         = settings["RABBIT_SRVER"],
					virtual_host = settings["RABBIT_VHOST"],
					master       = isMaster,
					synchronous  = not isMaster,
					flush_queues = isMaster)

	while 1:
		try:
			# if not isMaster:
			time.sleep(1)

			new = con.getMessage()
			if new:
				# print(new)
				if not isMaster:
					con.putMessage("Hi Thar!")

			if isMaster:
				con.putMessage("Oh HAI")

		except KeyboardInterrupt:
			break

	con.stop()

if __name__ == "__main__":
	test()


