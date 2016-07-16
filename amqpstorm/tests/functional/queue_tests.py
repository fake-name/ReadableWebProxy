import logging

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import amqpstorm
from amqpstorm import Connection
from amqpstorm.tests.utility import MockLoggingHandler

HOST = '127.0.0.1'
USERNAME = 'guest'
PASSWORD = 'guest'

logging.basicConfig(level=logging.DEBUG)

LOGGER = logging.getLogger(__name__)


class QueueFunctionalTests(unittest.TestCase):
    def setUp(self):
        self.logging_handler = MockLoggingHandler()
        logging.root.addHandler(self.logging_handler)
        self.connection = Connection(HOST, USERNAME, PASSWORD)
        self.channel = self.connection.channel()

    def test_functional_queue_declare(self):
        self.channel.queue.declare('test_functional_queue_declare',
                                   passive=False,
                                   durable=True, auto_delete=True)
        self.channel.queue.declare('test_functional_queue_declare',
                                   passive=True)

    def test_functional_queue_delete(self):
        self.channel.queue.declare('test_functional_queue_delete')
        self.channel.queue.delete('test_functional_queue_delete',
                                  if_unused=True)
        self.assertRaises(amqpstorm.AMQPChannelError,
                          self.channel.queue.declare,
                          'test_functional_queue_delete', passive=True)

    def test_functional_queue_purge(self):
        payload = 'hello world'
        queue = 'test_functional_functional_queue_purge'
        messages_to_send = 10
        self.channel.queue.declare(queue, auto_delete=True)
        for _ in range(messages_to_send):
            self.channel.basic.publish(payload, queue)
        result = self.channel.queue.purge(queue)
        self.assertEqual(result['message_count'], messages_to_send)

    def test_functional_queue_bind(self):
        queue = 'test_functional_queue_bind'
        self.channel.queue.declare(queue,
                                   passive=False,
                                   durable=True, auto_delete=True)
        self.assertEqual(self.channel.queue.bind(queue=queue,
                                                 exchange='amq.direct'), {})

    def test_functional_queue_bind_no_queue(self):
        queue = 'test_functional_queue_bind'
        self.channel.queue.declare(queue,
                                   passive=False,
                                   durable=True, auto_delete=True)
        self.assertEqual(self.channel.queue.bind(queue=queue,
                                                 exchange='amq.direct'), {})

    def test_functional_queue_unbind(self):
        queue = 'test_functional_queue_unbind'
        self.channel.queue.declare(queue,
                                   passive=False,
                                   durable=True, auto_delete=True)
        self.channel.queue.bind(queue=queue, exchange='amq.direct')
        self.assertEqual(self.channel.queue.unbind(queue=queue,
                                                   exchange='amq.direct'), {})

    def tearDown(self):
        self.channel.close()
        self.connection.close()
        self.assertFalse(self.logging_handler.messages['warning'])
        self.assertFalse(self.logging_handler.messages['error'])
        self.assertFalse(self.logging_handler.messages['critical'])
