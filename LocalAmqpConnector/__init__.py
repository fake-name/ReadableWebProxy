
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

class AmqpContainer(object):
	def __init__(self, vhost, uri, **config):


		assert 'task_queue_name'          in config
		assert 'response_queue_name'      in config
		assert 'task_exchange'            in config
		assert 'task_exchange_type'       in config
		assert 'response_exchange'        in config
		assert 'response_exchange_type'   in config
		assert 'durable'                  in config
		assert 'flush_queues'             in config
		assert 'hearbeat_packet_timeout'  in config

		self.keepalive_exchange_name = "keepalive_exchange"+str(id("wat"))
		self.hearbeat_packet_timeout = config['hearbeat_packet_timeout']

		self.log = logging.getLogger("Main.Connector.Container(%s)" % vhost)

		self.task_exchange   = config['task_exchange']
		self.task_queue_name = config['task_queue_name']
		self.durable         = config['durable']

		self.log.info("Initializing AMQP connection.")

		self.connection = rabbitpy.Connection(uri)

		self.bare_channel = self.connection.channel(blocking_read = True)
		# self.connection.connect()

		# Channel and exchange setup
		self.channel = rabbitpy.AMQP(self.bare_channel)
		self.channel.basic_qos(
				prefetch_size  = 0,
				prefetch_count = config['prefetch'],
				global_flag    = False
			)

		self.last_hearbeat_received = time.time()
		self.last_message_received = time.time()

		self.rx_timeout_lock        = threading.Lock()
		self.heartbeat_timeout_lock = threading.Lock()
		self.active_lock            = threading.Lock()

		self.log.info("Connection established. Setting up consumer.")

		if config['flush_queues']:
			self.log.info("Flushing items in queue.")
			self.channel.queue_purge(config['task_queue_name'])
			self.channel.queue_purge(config['response_queue_name'])

		self.log.info("Configuring queues.")

		task_exchange = rabbitpy.Exchange(
					self.bare_channel,
					name=config['task_exchange'],
					exchange_type=config['task_exchange_type'],
					durable=config['durable']
				)
		task_exchange.declare()

		resp_exchange = rabbitpy.Exchange(
					self.bare_channel,
					name=config['response_exchange'],
					exchange_type=config['response_exchange_type'],
					durable=config['durable']
				)
		resp_exchange.declare()

		# "NAK" queue, used for keeping the event loop ticking when we
		# purposefully do not want to receive messages
		# THIS IS A SHITTY WORKAROUND for keepalive issues.
		keepalive_exchange = rabbitpy.Exchange(
					self.bare_channel,
					name=self.keepalive_exchange_name,
					durable=False,
					auto_delete=True,
				)
		keepalive_exchange.declare()

		self.nak_q = rabbitpy.Queue(self.bare_channel, name=self.keepalive_exchange_name+'.nak.q', durable=False, auto_delete=True, expires=1000*self.hearbeat_packet_timeout*10)
		self.nak_q.declare()
		self.nak_q.bind(keepalive_exchange, routing_key="nak")

		self.in_q  = rabbitpy.Queue(self.bare_channel, name=config['response_queue_name'], durable=config['durable'],  auto_delete=False)
		self.in_q.bind(resp_exchange, routing_key=config['response_queue_name'].split(".")[0])

		self.in_q.declare()

		self.heartbeat_loops = 0

	def close(self):
		# Stop the flow of new items
		if self.channel:
			try:
				self.channel.basic_qos(
						prefetch_size  = 0,
						prefetch_count = 0,
						global_flag    = False
					)
			except rabbitpy.exceptions.RabbitpyException as e:
				self.log.error("Error on interface teardown!")
				self.log.error("	%s", e)

		# Close the connection once it's empty.
		closers = [
			self.in_q.stop_consuming,
			self.nak_q.stop_consuming,
			self.connection.close,
			self.bare_channel.close,
		]
		try:
			for func in closers:
				try:
					func()
				except rabbitpy.exceptions.RabbitpyException as e:
					self.log.error("Error on interface teardown!")
					self.log.error("	%s", e)
		finally:
			self.bare_channel   = None
			self.connection     = None
			self.channel        = None

			self.in_q  = None
			self.nak_q = None

			self.log.info("AMQP Thread exited")

	def keepalive_ticker(self):

		with self.active_lock:
			nak = self.nak_q.get()
			if nak:
				nak.ack()
				with self.heartbeat_timeout_lock:
					self.last_hearbeat_received = time.time()
				self.log.info("Heartbeat packet received!")
			self.channel.basic_publish(body={'wat' : 'wat'}, exchange=self.keepalive_exchange_name, routing_key='nak')

	def get_rx(self):
		print("Get_rx call()")
		for item in self.in_q:
			with self.rx_timeout_lock:
				self.last_message_received = time.time()
			self.log.info("Received packet from queue '%s'! Processing.", self.in_q.name)
			yield item

	def put_tx(self, message):
		out_queue = self.task_exchange
		out_key   = self.task_queue_name.split(".")[0]

		msg_prop = {}
		if self.durable:
			msg_prop["delivery_mode"] = 2
		self.channel.basic_publish(body=message, exchange=out_queue, routing_key=out_key, properties=msg_prop)


	def checkTimeouts(self):
		with self.heartbeat_timeout_lock:
			if (time.time() - self.last_hearbeat_received) > self.hearbeat_packet_timeout:
				with self.active_lock:
					self.log.error("Heartbeat Timeout!")
					raise Heartbeat_Timeout_Exception("Heartbeat timeout!")

		with self.rx_timeout_lock:
			if (time.time() - self.last_message_received) > self.hearbeat_packet_timeout:
				with self.active_lock:
					self.log.error("RX Message Timeout!")
					raise Heartbeat_Timeout_Exception("RX Heartbeat timeout!")

		self.heartbeat_loops += 1
		if self.heartbeat_loops > 10:
			self.heartbeat_loops = 1
			with self.heartbeat_timeout_lock:
				last_hb = time.time() - self.last_hearbeat_received
			with self.rx_timeout_lock:
				last_rx = time.time() - self.last_message_received

			self.log.info("Interface timeout thread. Ages: heartbeat -> %s, last message -> %s.", last_hb, last_rx)

	def __del__(self):
		try:
			self.close()
		except Exception:
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

		self.connected          = multiprocessing.Value("i", 0)
		self.run_threads          = multiprocessing.Value("i", 1)


		self.session_fetched        = 0
		self.queue_fetched          = 0
		self.active                 = 0
		self.sent_messages = 0
		self.recv_messages = 0

		self.delivered = 0

		self.connect_lock = threading.Lock()
		self.connect()

	def disconnect(self):

		with self.connect_lock:
			self.interface.close()
			self.run_threads.value = 0

			self.rx_thread.join()
			self.timeout_thread.join()

			try:
				del self.rx_thread
			except Exception:
				pass
			try:
				del self.timeout_thread
			except Exception:
				pass

	def connect(self):

		conn_params = {
			'task_queue_name'         : self.config['task_queue_name'],
			'response_queue_name'     : self.config['response_queue_name'],
			'task_exchange'           : self.config['task_exchange'],
			'task_exchange_type'      : self.config['task_exchange_type'],
			'response_exchange'       : self.config['response_exchange'],
			'response_exchange_type'  : self.config['response_exchange_type'],
			'durable'                 : self.config['durable'],
			'prefetch'                : self.config['prefetch'],
			'flush_queues'            : self.config['flush_queues'],
			'hearbeat_packet_timeout' : self.config['hearbeat_packet_timeout'],
		}


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

		with self.connect_lock:
			self.run_threads.value = 1

			self.interface = AmqpContainer(self.config['virtual_host'], uri, **conn_params)

			self.rx_thread = threading.Thread(target=self._processReceiving, daemon=True)
			self.timeout_thread = threading.Thread(target=self._timeoutWatcher, daemon=True)
			self.rx_thread.start()
			self.timeout_thread.start()

	def __del__(self):
		try:
			self.interface.close()
		except Exception:
			pass
		self.run_threads.value = 0

		self.rx_thread.join()
		self.timeout_thread.join()
		self.interface = None


	def tx_poll(self):


		print_time = 15              # Print a status message every n seconds
		integrator = 0               # Time since last status message emitted.

		# When run is false, don't halt until
		# we've flushed the outgoing items out the queue
		while self.runstate.value or self.response_queue.qsize():
			# print("TX Polling!")
			if not hasattr(self, 'interface') or not self.interface:
				self.connect()

			time.sleep(1)

			self._publishOutgoing()
			# Reset the print integrator.
			if self.interface and integrator > print_time:
				integrator = 0
				self.interface.keepalive_ticker()
				self.log.info("AMQP Interface process. Current message counts: %s (out: %s, in: %s)", self.active, self.sent_messages, self.recv_messages)
			integrator += 1


	def _timeoutWatcher(self):
		while self.runstate.value:
			try:
				self.interface.checkTimeouts()
				time.sleep(1)
			except Heartbeat_Timeout_Exception:
				self.disconnect()


	def _processReceiving(self):

		while self.runstate.value:
			try:
				# # 	# Prevent never breaking from the loop if the feeding queue is backed up.
				# item = self.in_q.get()
				# if item:
				if self.interface:
					# print("RX Polling")
					for item in self.interface.get_rx():
						self.task_queue.put(item.body)
						item.ack()

						self.active += 1
						self.recv_messages += 1
						self.session_fetched += 1


						blocked = 0
						while self.task_queue.qsize() > self.config['prefetch']:
							if not self.runstate.value:
								self.log.info("Receving loop saw exit flag. Breaking!")
								return

							time.sleep(1)
							blocked += 1
							if blocked > 10:
								self.log.warning("Receive loop blocked due to excessive rx queue size (%s).", self.task_queue.qsize())
								blocked = 0
				time.sleep(1)

			except rabbitpy.exceptions.RabbitpyException as e:
				self.log.error("Error while tx_polling interface!")
				self.log.error("	%s", e)
				self.disconnect()

	def _publishOutgoing(self):
		while self.runstate.value:
			try:
				put = self.response_queue.get_nowait()
				# self.log.info("Publishing message of len '%0.3f'K to exchange '%s'", len(put)/1024, out_queue)
				# message = amqp.basic_message.Message(body=put)

				self.interface.put_tx(put)
				self.sent_messages += 1
				self.active -= 1

			except queue.Empty:
				break
		time.sleep(1)


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
			connection.tx_poll()

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

		self.is_master = config['master']

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
		if self.is_master:
			resp_q = self.taskQueue
		else:
			resp_q = self.responseQueue

		block = 0
		blocklen = 25
		while resp_q.qsize() > 0:
			self.log.info("%s remaining outgoing AMQP items (%s).", resp_q.qsize(), blocklen-block)
			time.sleep(1)
			block += 1
			if block > blocklen:
				break

		self.log.info("%s remaining outgoing AMQP items.", resp_q.qsize())

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


