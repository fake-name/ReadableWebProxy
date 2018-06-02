
import amqpstorm
import urllib.parse
import socket
import random
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
class ThreadDieException(Exception):
	pass

GLOBAL_THREAD_NO = 1

def validate_config(config):
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
		assert 'heartbeat'                in config
		assert 'sslopts'                  in config
		assert 'prefetch'                 in config
		assert 'socket_timeout'           in config

class SingleAmqpConnection(object):
	def __init__(self, config, task_queue, response_queue):

		validate_config(config)
		self.config             = config

		self.log = logging.getLogger("Main.Connector.Internal")

		self.task_queue              = task_queue
		self.response_queue          = response_queue

		self.info_printerval         = time.time()
		self.last_heartbeat_sent     = time.time()
		self.last_heartbeat_received = time.time()
		self.last_message_received   = time.time()

		self.session_fetched         = 0
		self.queue_fetched           = 0
		self.keepalive_num           = 0
		self.prefetch_extended       = False


		self.exit_signaled           = multiprocessing.Value("i", 0, lock=False)
		self.keepalive_exchange_name = "keepalive_exchange"+str(id("wat"))

		self.__launch_thread()

	def __connect(self):

		self.__open_connection()
		self.__configure_channel()
		self.__configure_rpc_exchanges()
		self.__configure_keepalive_channel()

		# Re-enqueue any not-acked packets.
		self.storm_channel.basic.recover(requeue=True)
		self.storm_channel._inbound.clear()

		self.__start_consume()


	def __open_connection(self):
		self.log.info("Initializing AMQP connection.")
		self.storm_connection = amqpstorm.Connection(
				hostname     = self.config['host'].split(":")[0],
				username     = self.config['userid'],
				password     = self.config['password'],
				port         = int(self.config['host'].split(":")[1]),
				virtual_host = self.config['virtual_host'],
				heartbeat    = self.config['heartbeat'],
				timeout      = self.config['socket_timeout'],
				ssl          = True,
				ssl_options  = {
					'ca_certs'           : self.config['sslopts']['ca_certs'],
					'certfile'           : self.config['sslopts']['certfile'],
					'keyfile'            : self.config['sslopts']['keyfile'],
				}

			)

	def __start_consume(self):
		self.log.info("Bound. Triggering consume")
		self.storm_channel.basic.consume(self.__handle_rx, queue=self.config['response_queue_name'],    no_ack=False)
		self.storm_channel.basic.consume(self.__handle_rx, queue=self.keepalive_exchange_name+'.nak.q', no_ack=False)
		self.log.info("Consume triggered.")



	def __configure_channel(self):

		self.log.info("Connection established. Setting up consumer.")
		self.storm_channel = self.storm_connection.channel(rpc_timeout=self.config['socket_timeout'])

		# Initial QoS is tiny, throttle it up after everything is actually running.
		self.storm_channel.basic.qos(1, global_=True)
		self.prefetch_extended = False



	def __configure_keepalive_channel(self):

		# "NAK" queue, used for keeping the event loop ticking when we
		# purposefully do not want to receive messages
		# THIS IS A SHITTY WORKAROUND for keepalive issues.

		self.log.info("Configuring keepalive channel")
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

		self.log.info("Configuring keepalive channel complete")


	def __configure_rpc_exchanges(self):

		self.log.info("Configuring RPC channel.")

		args = {}
		# if 'dlq' in self.config and self.config['dlq']:
		# 	dlexc =

		self.storm_channel.exchange.declare(
					exchange      = self.config['task_exchange'],
					exchange_type = self.config['task_exchange_type'],
					durable       = True,
					arguments     = args,
				)

		self.storm_channel.exchange.declare(
					exchange      = self.config['response_exchange'],
					exchange_type = self.config['response_exchange_type'],
					durable       = True
				)

		self.storm_channel.queue.declare(
					queue         = self.config['response_queue_name'],
					durable       = True,
					auto_delete   = False)

		self.storm_channel.queue.bind(
					queue         = self.config['response_queue_name'],
					exchange      = self.config['response_exchange'],
					routing_key   = self.config['response_queue_name'].split(".")[0])

		self.log.info("Configured.")


	def __poke_keepalive(self):
		mbody = "keepalive %s, random: %s" % (self.keepalive_num, random.random())
		self.storm_channel.basic.publish(body=mbody, exchange=self.keepalive_exchange_name, routing_key='nak',
			properties={
				'correlation_id' : "keepalive_{}".format(self.keepalive_num)
			})
		self.keepalive_num += 1
		self.last_heartbeat_sent = time.time()

	def __do_rx(self):
		self.storm_channel.process_data_events(to_tuple=False)

	def __handle_rx(self, message):
		# self.log.info("Received message!")
		# self.log.info("Message channel: %s", message.channel)
		# self.log.info("Message properties: %s", message.properties)
		corr_id = message.properties['correlation_id']
		if isinstance(corr_id, (bytes, bytearray)):
			corr_id = corr_id.decode('ascii')
		if corr_id.startswith('keepalive'):
			self.__handle_keepalive_rx(corr_id, message)
		else:
			self.__handle_normal_rx(corr_id, message)

		if self.prefetch_extended is False:
			self.prefetch_extended = True
			self.storm_channel.basic.qos(self.config['prefetch'], global_=True)
			self.log.info("Prefetch updated")


	def __handle_keepalive_rx(self, corr_id, message):

		self.last_heartbeat_received = time.time()
		message.ack()
		self.log.info("Heartbeat packet received! %s -> %s", message.body.decode("ascii"), corr_id)

	def __handle_normal_rx(self, corr_id, message):

		self.last_message_received = time.time()
		self.response_queue.put(message.body)
		message.ack()

		self.log.info("Message packet received! %s", len(message.body))

	def __do_tx(self):

		for dummy_x in range(500):

			# self.log.info("Items in outgoing TX queue: %s", self.task_queue.qsize())
			print("/", end="", flush=True)
			try:
				put = self.task_queue.get_nowait()
			except queue.Empty:
				return

			try:
				out_key   = self.config['task_queue_name'].split(".")[0]

				msg_prop = {}
				if self.config['task_queue_name']:
					msg_prop["delivery_mode"] = 2

				if not self.storm_channel:
					raise Message_Publish_Exception("Failed to publish message!")

				self.storm_channel.basic.publish(body=put, exchange=self.config['task_exchange'], routing_key=out_key, properties=msg_prop)

			except amqpstorm.AMQPError as e:
				self.log.error("Error while tx_polling interface!")
				self.task_queue.put(put)
				self.log.error("	%s", e)
				for line in traceback.format_exc().split("\n"):
					self.log.error(line)
				raise ThreadDieException("Error!")

			except Message_Publish_Exception as e:
				self.log.error("Error while publishing message!")
				self.task_queue.put(put)
				self.log.error("	%s", e)
				for line in traceback.format_exc().split("\n"):
					self.log.error(line)
				raise ThreadDieException("Error!")



	def __check_timeouts(self):
		now = time.time()

		if self.info_printerval + 10 < now:
			self.log.info("Interface timeout thread. Ages: heartbeat -> %0.2f, last message -> %0.2f, TX, RX q: (%s, %s).",
					now - self.last_heartbeat_received,
					now-self.last_message_received,
					self.task_queue.qsize(),
					self.response_queue.qsize(),
					)
			self.info_printerval += 10

		# Send heartbeats every 5 seconds.
		if self.last_heartbeat_sent + 5 < now:
			self.__poke_keepalive()

		# Allow data to act as a heartbeat.
		if (self.last_heartbeat_received + self.config['heartbeat'] < now
				and self.last_message_received + self.config['heartbeat'] < now):

			self.log.error("Heartbeat receive timeout! Missed heartbeat (%s, %s).",
					self.last_heartbeat_received + self.config['heartbeat'] - now,
					self.last_message_received + self.config['heartbeat'] - now,
				)
			self.last_heartbeat_received = now
			raise ThreadDieException("Timed out! Dying!")


		if (self.last_message_received + (self.config['heartbeat'] * 8) < now and
			self.last_heartbeat_received + (self.config['heartbeat'] * 8) < now):
			# Attempt recover if we've been idle for a while.
			self.log.info("Reconnect retrigger seems to have not fixed the issue?")



	def __run(self):
		self.__connect()

		while self.exit_signaled.value == 0:
			try:
				print("\\", end="", flush=True)
				self.__do_tx()
				self.__do_rx()
				self.__check_timeouts()
				time.sleep(0.1)
			except Exception as e:
				# with open("mq error %s.txt" % time.time(), 'w') as fp:
				# 	fp.write("Error!\n\n")
				# 	fp.write(traceback.format_exc())
				self.log.error("Error!")
				self.log.error("%s", e)
				for line in traceback.format_exc().split("\n"):
					self.log.error(line)
				raise e



	def disconnect(self):
		self.prefetch_extended = False
		try:
			self.storm_channel.close()
		except Exception:
			pass
		try:
			self.storm_connection.close()
		except Exception:
			pass
		raise ThreadDieException("Exiting")

	def shutdown(self):
		self.log.info("ConnectorManager shutdown called!")
		for dummy_x in range(30):
			qs = self.task_queue.qsize()
			if qs == 0:
				break
			else:
				self.log.warning("Outgoing queue draining. Items: %s", qs)
				self.__do_tx()
				time.sleep(1)
		self.disconnect()


	def __launch_thread(self):
		self.__worker = threading.Thread(
					target=self.__run,
					name="RMQ Consumer {}: {}".format(GLOBAL_THREAD_NO, self.config['virtual_host'])
				)
		self.__worker.start()

		global GLOBAL_THREAD_NO
		GLOBAL_THREAD_NO += 1

	def get_thread(self):
		return self.__worker

	def worker_alive(self):
		return self.__worker.is_alive()

	def signal_stop(self):
		self.exit_signaled.value = 1

	def join(self):
		self.signal_stop()
		self.__worker.join()

	def __del__(self):
		self.shutdown()
		self.signal_stop()
		try:
			self.__worker.join()
		except Exception:
			pass

	@classmethod
	def build_thread(cls, config, tx_q, rx_q):
		instance = cls(config, tx_q, rx_q)

		return instance



