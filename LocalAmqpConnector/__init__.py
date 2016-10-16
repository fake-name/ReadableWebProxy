
import amqpstorm
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

class Message_Publish_Exception(Exception):
	pass

class AmqpContainer(object):
	def __init__(self, conn_params, rx_queue, **config):

		self.log = logging.getLogger("Main.Connector.Container(%s)" % conn_params['virtual_host'])


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
		for key, value in conn_params.items():
			self.log.info("	%s -> %s", key, value)

		self.log.info("Config params:")
		for key, value in config.items():
			self.log.info("	%s -> %s", key, value)

		self.keepalive_exchange_name = "keepalive_exchange"+str(id("wat"))
		self.hearbeat_packet_timeout = config['hearbeat_packet_timeout']

		self.task_exchange   = config['task_exchange']
		self.task_queue_name = config['task_queue_name']
		self.durable         = config['durable']

		self.log.info("Initializing AMQP connection.")

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

		self.rx_queue = rx_queue

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
					queue=self.keepalive_exchange_name+'.nak.q',
					durable=False,
					auto_delete=True)

		self.storm_channel.queue.bind(
					queue=self.keepalive_exchange_name+'.nak.q',
					exchange=self.keepalive_exchange_name,
					routing_key="nak")

		self.storm_channel.queue.declare(
					queue=config['response_queue_name'],
					durable=config['durable'],
					auto_delete=False)
		self.log.info("Declared.")

		self.storm_channel.queue.bind(
					queue=config['response_queue_name'],
					exchange=config['response_exchange'],
					routing_key=config['response_queue_name'].split(".")[0])

		self.heartbeat_loops = 0
		self.consumer_cycle = 0

		self.prefetch_extended = False
		self.prefetch_count = config['prefetch']

	def start_consume(self, config):
		self.log.info("Bound. Triggering consume")
		self.storm_channel.basic.consume(self.handle_rx, queue=config['response_queue_name'],         no_ack=False)
		self.storm_channel.basic.consume(self.handle_rx, queue=self.keepalive_exchange_name+'.nak.q', no_ack=False)
		self.log.info("Consume triggered.")




	def close(self):
		# Stop the flow of new items

		# if self.channel:
		# 	try:
		# 		self.channel.prefetch_count(0)
		# 	except rabbitpy.exceptions.RabbitpyException as e:
		# 		self.log.error("Error on interface teardown!")
		# 		self.log.error("	%s", e)

		# Apparently you can close the underlying connection, and have it's thread die, and
		# somehow not have the channel consumer stop. Anyways, stop that first so it shouldn't
		# get wedged in the future.
		self.log.info("Closing channel")
		self.storm_channel.close()

		# Close the connection
		self.log.info("Closing connection")
		self.storm_connection.close()

	def kill(self):
		self.log.info("Killing connection")
		self.storm_connection.kill()
		self.storm_channel.kill()

	def enter_blocking_rx_loop(self):
		self.storm_channel.start_consuming(to_tuple=False)


	def handle_keepalive_rx(self, message):

		with self.heartbeat_timeout_lock:
			self.last_hearbeat_received = time.time()
		message.ack()
		self.log.info("Heartbeat packet received! %s", message.body)

	def handle_normal_rx(self, message):

		with self.rx_timeout_lock:
			self.last_message_received = time.time()
		self.rx_queue.put(message.body)
		message.ack()

		self.log.info("Message packet received! %s", len(message.body))
	def handle_rx(self, message):
		# self.log.info("Received message!")
		# self.log.info("Message channel: %s", message.channel)
		# self.log.info("Message properties: %s", message.properties)
		if message.properties['correlation_id'] == 'keepalive':
			self.handle_keepalive_rx(message)
		else:
			self.handle_normal_rx(message)

		if self.prefetch_extended is False:
			self.prefetch_extended = True
			self.storm_channel.basic.qos(self.prefetch_count, global_=True)
			self.log.info("Prefetch updated")

	def poke_keepalive(self):
		self.storm_channel.basic.publish(body='wat', exchange=self.keepalive_exchange_name, routing_key='nak',
			properties={
				'correlation_id' : "keepalive"
			})


	def put_tx(self, message):
		out_key   = self.task_queue_name.split(".")[0]

		msg_prop = {}
		if self.durable:
			msg_prop["delivery_mode"] = 2

		if not self.storm_channel:
			raise Message_Publish_Exception("Failed to publish message!")

		self.storm_channel.basic.publish(body=message, exchange=self.task_exchange, routing_key=out_key, properties=msg_prop)

	def checkTimeouts(self):
		with self.heartbeat_timeout_lock:
			if (time.time() - self.last_hearbeat_received) > self.hearbeat_packet_timeout:
				with self.active_lock:
					print()
					print()
					print()
					print()
					self.log.error("Heartbeat Timeout!")
					print()
					print()
					print()
					print()
					raise Heartbeat_Timeout_Exception("Heartbeat timeout!")

		with self.rx_timeout_lock:
			if (time.time() - self.last_message_received) > (self.hearbeat_packet_timeout * 30):
				with self.active_lock:
					print()
					print()
					print()
					print()
					self.log.error("RX Message Timeout!")
					print()
					print()
					print()
					print()
					raise Heartbeat_Timeout_Exception("RX Heartbeat timeout!")

		self.heartbeat_loops += 1
		if self.heartbeat_loops > 10:
			self.heartbeat_loops = 1
			with self.heartbeat_timeout_lock:
				last_hb = time.time() - self.last_hearbeat_received
			with self.rx_timeout_lock:
				last_rx = time.time() - self.last_message_received

			# self.consumer_cycle += 1
			# if self.consumer_cycle > 30:
			# 	# We periodically cycle the consuming state of the input queue, to stop it from being wedged.
			# 	self.storm_channel.close()
			self.log.info("Interface timeout thread. Ages: heartbeat -> %0.2f, last message -> %0.2f.", last_hb, last_rx)

class ConnectorManager:
	def __init__(self, config, runstate, task_queue, response_queue):

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
		assert 'hearbeat_packet_timeout'  in config
		assert 'ack_rx'                   in config



		self.log = logging.getLogger("Main.Connector.Internal(%s)" % config['virtual_host'])
		self.runstate           = runstate
		self.config             = config
		self.task_queue         = task_queue
		self.response_queue     = response_queue

		self.connected          = multiprocessing.Value("i", 0)

		self.had_exception      = multiprocessing.Value("i", 0)
		self.threads_live       = multiprocessing.Value("i", 0)


		self.session_fetched        = 0
		self.queue_fetched          = 0
		self.active                 = 0
		self.sent_messages = 0
		self.recv_messages = 0

		self.delivered = 0
		self.die_timeout = time.time()

		self.connect_lock = threading.Lock()
		self.__connect()

	def __connect(self):

		rabbit_params = {
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

		with self.connect_lock:
			self.threads_live.value  = 1
			self.had_exception.value = 0

			self.interface = AmqpContainer(conn_params, self.task_queue, **rabbit_params)

			self.rx_thread = threading.Thread(target=self._rx_poll,         daemon=False)
			self.tx_thread = threading.Thread(target=self._tx_poll,         daemon=False)
			self.hb_thread = threading.Thread(target=self._timeout_watcher, daemon=False)
			self.rx_thread.start()
			self.tx_thread.start()
			self.hb_thread.start()

			# print("Living threads:")
			# print("rx_thread", self.rx_thread.is_alive())
			# print("tx_thread", self.tx_thread.is_alive())
			# print("hb_thread", self.hb_thread.is_alive())

			self.interface.start_consume(rabbit_params)


	def disconnect(self):
		with self.connect_lock:
			self.threads_live.value = 0
			if hasattr(self, "interface"):
				self.interface.close()
			failed_to_die = 0
			threads = [self.rx_thread, self.tx_thread, self.hb_thread]
			while any([thread.is_alive() for thread in threads]):
				for thread in [thread for thread in threads if thread.is_alive()]:
					thread.join(1)
				self.log.warning("Waiting on threads to join (tx: %s, rx: %s, hb: %s),  Threads_live: %s, had exception %s, resp queue size: %s, die: %s!",
					self.tx_thread.is_alive(),
					self.rx_thread.is_alive(),
					self.hb_thread.is_alive(),
					self.threads_live.value,
					self.had_exception.value,
					self.response_queue.qsize(),
					failed_to_die,
					)
				failed_to_die += 1
				try:
					if failed_to_die > 15:
						self.log.warning("Attempting to kill interface!")
						self.interface.kill()
					else:
						self.interface.close()
				except Exception:
					self.log.error("Closing interface failed!")

					for line in traceback.format_exc().split("\n"):
						self.log.error(line)

			self.log.info("Interface threads joined")

			try:
				del self.rx_thread
			except Exception:
				pass
			try:
				del self.tx_thread
			except Exception:
				pass
			try:
				del self.hb_thread
			except Exception:
				pass

			try:
				del self.interface
			except Exception:
				pass

	def __should_die(self):
		# ret = self.runstate.value != 1 or self.threads_live.value != 1 or self.had_exception.value != 0

		if self.runstate.value == 1:
			self.die_timeout = time.time()
		elif self.response_queue.qsize() > 0:
			pass
		else:
			self.die_timeout -= 500



		ret = self.threads_live.value != 1 or self.had_exception.value != 0 or (time.time() - self.die_timeout > 20)
		if ret:

			self.log.warning("Should die flag! Runstate: %s, threads live: %s, had exception: %s.",
				"running" if self.runstate.value == 1 else "halting",
				"threads alive" if self.threads_live.value == 1 else "threads stopping",
				"yes" if self.had_exception.value == 1 else "no"
				)
		return ret

	def _tx_poll(self):
		time.sleep(1)
		self.log.info("TX Poll process starting. Threads_live: %s, resp queue size: %s, had exception %s", self.threads_live.value, self.response_queue.qsize(), self.had_exception.value)

		# When run is false, don't halt until
		# we've flushed the outgoing items out the queue
		while not self.__should_die():
			for dummy_x in range(250):

				if self.__should_die():
					self.log.info("Transmit loop saw exit flag. Breaking!")
					return
				else:
					self.log.info("Transmit looping!")

				try:
					put = self.response_queue.get_nowait()
				except queue.Empty:
					break
					# self.log.info("Publishing message of len '%0.3f'K to exchange '%s'", len(put)/1024, out_queue)
					# message = amqp.basic_message.Message(body=put)

				try:

					self.interface.put_tx(put)
					self.sent_messages += 1
					self.active -= 1

				except amqpstorm.AMQPError as e:
					self.log.error("Error while tx_polling interface!")
					self.log.error("	%s", e)
					for line in traceback.format_exc().split("\n"):
						self.log.error(line)
					self.had_exception.value = 1
					break
				except Message_Publish_Exception as e:
					self.log.error("Error while publishing message!")
					self.response_queue.put(put)
					self.log.error("	%s", e)
					for line in traceback.format_exc().split("\n"):
						self.log.error(line)
					self.had_exception.value = 1
					break
			time.sleep(1)

		self.log.info("TX Poll process dying (should die: %s). Threads_live: %s, runstate: %s, resp queue size: %s, had exception %s.",
			self.__should_die(), self.threads_live.value, self.runstate.value, self.response_queue.qsize(), self.had_exception.value)

	def _timeout_watcher(self):
		time.sleep(1)
		print_time = 30              # Print a status message every n seconds
		hb_time    =  5              # Print a status message every n seconds
		integrator =  0              # Time since last status message emitted.

		while not self.__should_die():
			try:

				self.interface.checkTimeouts()
				time.sleep(1)

				integrator += 1
				# Reset the print integrator.
				if self.interface and (integrator % hb_time) == 0:
					self.interface.poke_keepalive()
				if self.interface and (integrator % print_time) == 0:
					self.log.info("Timeout watcher loop. Current message counts: %s (out: %s, in: %s)", self.active, self.sent_messages, self.recv_messages)
			except Heartbeat_Timeout_Exception:
				self.had_exception.value = 1
			except Message_Publish_Exception:
				self.had_exception.value = 1
			except amqpstorm.AMQPError as e:
				self.log.error("RabbitPy Exception in worker.")
				for line in traceback.format_exc().split("\n"):
					self.log.error(line)
				self.had_exception.value = 1
			except Exception:
				self.log.error("Generic exception in timeout watcher thread.")
				for line in traceback.format_exc().split("\n"):
					self.log.error(line)
				self.had_exception.value = 1


	def _rx_poll(self):
		time.sleep(1)

		self.log.info("RX Poll process starting. Threads_live: %s, had exception %s", self.threads_live.value, self.had_exception.value)
		try:
			while not self.__should_die():
				self.interface.enter_blocking_rx_loop()
		except amqpstorm.AMQPError as e:
			self.log.error("Error while in rx runloop!")
			self.log.error("	%s", e)
			for line in traceback.format_exc().split("\n"):
				self.log.error(line)
			self.had_exception.value = 1

		self.log.info("RX Poll process dying. Threads_live: %s, had exception %s, should_die %s", self.threads_live.value, self.had_exception.value, self.__should_die())

	def monitor_loop(self):

		self.had_exception.value = 0
		while self.runstate.value == 1:
			if self.had_exception.value == 1:
				print("Disconnecting!")
				try:
					self.disconnect()
				except Exception:
					for line in traceback.format_exc().split("\n"):
						self.log.error(line)
					self.had_exception.value = 1
				print("Reconnecting")
				time.sleep(5)
				try:
					self.__connect()
					self.had_exception.value = 0
				except Exception:
					for line in traceback.format_exc().split("\n"):
						self.log.error(line)
					self.had_exception.value = 1
			time.sleep(1)
			print("Monitor loop!", self.runstate.value)

		self.shutdown()

	def shutdown(self):
		self.log.info("ConnectorManager shutdown called!")
		for dummy_x in range(30):
			qs = self.response_queue.qsize()
			if qs == 0:
				break
			else:
				self.log.warning("Outgoing queue draining. Items: %s", qs)
				self._tx_poll()
				time.sleep(1)
		self.threads_live.value = 0
		self.disconnect()

	@classmethod
	def run_fetcher(cls, config, runstate, tx_q, rx_q):
		'''
		bleh

		'''

		log = logging.getLogger("Main.Connector.Manager(%s)" % config['virtual_host'])

		log.info("Worker thread starting up.")
		try:
			print()
			print()
			print("Connecting %s" % config['virtual_host'])
			print()
			print()
			connection_manager = cls(config, runstate, tx_q, rx_q)
			print()
			print()
			print("Entering monitor-loop %s" % config['virtual_host'])
			print()
			print()
			connection_manager.monitor_loop()

		except Exception:
			log.error("Exception in connector! Terminating connection...")
			for line in traceback.format_exc().split('\n'):
				log.error(line)
			try:
				connection_manager.disconnect()
			except Exception:
				log.info("")
				log.error("Failed pre-emptive closing before reconnection. May not be a problem?")
				for line in traceback.format_exc().split('\n'):
					log.error(line)
			try:
				connection_manager.shutdown()
				del connection_manager
			except Exception:
				log.info("")
				log.error("Failed pre-emptive closing before reconnection. May not be a problem?")
				for line in traceback.format_exc().split('\n'):
					log.error(line)
			if runstate.value != 0:
				log.error("Triggering reconnection...")

		if connection_manager:
			connection_manager.shutdown()
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
			'heartbeat'                : kwargs.get('heartbeat',                 60),
			'sslopts'                  : kwargs.get('ssl',                      None),
			'poll_rate'                : kwargs.get('poll_rate',                  0.25),
			'prefetch'                 : kwargs.get('prefetch',                   1),
			'session_fetch_limit'      : kwargs.get('session_fetch_limit',      None),
			'durable'                  : kwargs.get('durable',                  False),
			'socket_timeout'           : kwargs.get('socket_timeout',            30),

			'hearbeat_packet_timeout'  : kwargs.get('hearbeat_packet_timeout',  60),
			'ack_rx'                   : kwargs.get('ack_rx',                   True),
		}

		assert config['hearbeat_packet_timeout'] > config['socket_timeout'],                                   \
			"Heartbeat time must be greater then socket timeout! Heartbeat interval: %s. Socket timeout: %s" % \
			(config['hearbeat_packet_timeout'], config['socket_timeout'])

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

		self.thread = threading.Thread(target=ConnectorManager.run_fetcher, args=(self.__config, self.runstate, self.taskQueue, self.responseQueue), daemon=True)
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

		self.log.info("%s remaining outgoing AMQP items. Joining on thread.", resp_q.qsize())

		self.thread.join()
		self.log.info("AMQP interface thread halted.")

	def __del__(self):
		# print("deleter: ", self.runstate, self.runstate.value)
		if self.runstate.value:
			self.stop()
