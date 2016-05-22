
#!/usr/bin/env python3
import logSetup
import AmqpConnector
import signal
import logging
import os.path
import ssl
import time
import msgpack
import multiprocessing
import queue
import config


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


		self.log.info("Connected AMQP RPC Interface: %s", self.connector)
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
		if ret:
			self.log.info("[get_item] Received data size: %s bytes.", len(ret))
		# else:
		# 	print("getMessage returned: ", ret)
		return ret


	def __del__(self):
		self.close()

	def close(self):
		if self.connector:
			self.connector.stop()
			self.connector = None

def nop(dummy_1, dummy_2):
	pass

def handleFetchResponse(message):
	pass
def handleheadResponse(message):
	pass

job_handlers = {
	"fetch" : handleFetchResponse,
	"head"  : handleheadResponse,
}

def processResponse(message):
	assert message['']


class AmqpRemoteJobManager():
	def __init__(self):

		logPath = 'Main.Feeds.RPC-Manager'
		self.log = logging.getLogger(logPath)


		self.input_queue  = multiprocessing.Queue()
		self.run = multiprocessing.Value("b", 1)

		self.thread = multiprocessing.Process(target=self.worker)
		self.thread.start()

		self.log.info("AMQP Job manager initialization.")

		self.rets = {}

	def __del__(self):
		self.run.value = 0
		self.thread.join()

	def _launch(self):
		amqp_settings = {
			"RPC_RABBIT_LOGIN" : config.C_RPC_RABBIT_LOGIN,
			"RPC_RABBIT_PASWD" : config.C_RPC_RABBIT_PASWD,
			"RPC_RABBIT_SRVER" : config.C_RPC_RABBIT_SRVER,
			"RPC_RABBIT_VHOST" : config.C_RPC_RABBIT_VHOST,
		}

		self.connector = RabbitQueueHandler(amqp_settings)

	def _teardown(self):
		self.connector.close()

	def worker(self):
		# logSetup.initLogging()
		signal.signal(signal.SIGINT, nop)
		self.log.info("AMQP Worker launched!")
		self._launch()
		while self.run.value:
			self.process_queues()
		self._teardown()
		self.log.info("AMQP Worker halted!")

	def process_queues(self):
		import pprint
		try:
			data = self.input_queue.get_nowait()
			with open("fetchresult.txt", "w") as fp:
				fp.write(pprint.pformat(msgpack.unpackb(data, encoding='utf-8', use_list=False)))
				fp.write("\n\n\n")
			self.connector.put_item(data)
		except queue.Empty:
			time.sleep(0.05)
		new = self.connector.get_item()
		if new:
			self.log.info("Processing AMQP response item!")
			new = msgpack.unpackb(new, encoding='utf-8', use_list=False)
			with open("fetchresult.txt", "a") as fp:
				fp.write(pprint.pformat(new))
			processResponse(new)


	def put_job(self, new_job):
		assert 'module'       in new_job
		assert 'call'         in new_job
		assert 'dispatch_key' in new_job
		assert 'jobid'        in new_job
		assert new_job['jobid'] != None

		# Make sure we have a returned data list for the added job.
		if not new_job['dispatch_key'] in self.rets:
			self.rets[new_job['dispatch_key']] = []

		packed_job = msgpack.packb(new_job, use_bin_type=True)
		self.input_queue.put(packed_job)


def buildjob(
			module,
			call,
			dispatchKey,
			jobid,
			args           = [],
			kwargs         = {},
			additionalData = None,
			postDelay      = 0
		):

	job = {
			'call'         : call,
			'module'       : module,
			'args'         : args,
			'kwargs'       : kwargs,
			'extradat'     : additionalData,
			'jobid'        : jobid,
			'dispatch_key' : dispatchKey,
			'postDelay'    : postDelay,
		}
	return job




if __name__ == '__main__':
	import logSetup
	logSetup.initLogging()

	amqpint = AmqpRemoteJobManager()
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


