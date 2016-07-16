import logging

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from amqpstorm import Connection
from amqpstorm.tests.utility import MockLoggingHandler

HOST = '127.0.0.1'
USERNAME = 'guest'
PASSWORD = 'guest'

logging.basicConfig(level=logging.DEBUG)

LOGGER = logging.getLogger(__name__)


class BasicFunctionalTests(unittest.TestCase):
    def setUp(self):
        self.logging_handler = MockLoggingHandler()
        logging.root.addHandler(self.logging_handler)
        self.connection = Connection(HOST, USERNAME, PASSWORD)
        self.channel = self.connection.channel()

    def test_functional_basic_qos(self):
        result = self.channel.basic.qos(prefetch_count=100)
        self.assertEqual(result, {})

    def test_functional_basic_get(self):
        payload = 'hello world'
        queue = 'test_functional_basic_get'
        try:
            self.channel.queue.declare(queue)
            self.channel.basic.publish(payload, queue)

            message = self.channel.basic.get(queue, to_dict=False)
            self.assertEqual(message.body, payload)
            message.ack()
        finally:
            self.channel.queue.delete(queue)

    def test_functional_basic_cancel(self):
        queue = 'test_functional_basic_cancel'
        try:
            self.channel.queue.declare(queue)
            consumer_tag = self.channel.basic.consume(None, queue)

            result = self.channel.basic.cancel(consumer_tag)
            self.assertEqual(result['consumer_tag'], consumer_tag)
        finally:
            self.channel.queue.delete(queue)

    def test_functional_basic_recover(self):
        payload = 'hello world'
        queue = 'test_functional_basic_recover'
        try:
            self.channel.queue.declare(queue)
            self.channel.basic.publish(payload, queue)

            self.assertEqual(self.channel.basic.recover(requeue=True), {})
        finally:
            self.channel.queue.delete(queue)

    def test_functional_basic_ack(self):
        payload = 'hello world'
        queue = 'test_functional_basic_ack'
        try:
            self.channel.queue.declare(queue)
            self.channel.basic.publish(payload, queue)

            message = self.channel.basic.get(queue, to_dict=True)

            result = self.channel.basic.ack(
                delivery_tag=message['method']['delivery_tag'])

            self.assertEqual(result, None)

            # Make sure the message wasn't requeued.
            self.assertFalse(self.channel.basic.get(queue, to_dict=True))
        finally:
            self.channel.queue.delete(queue)

    def test_functional_basic_nack(self):
        payload = 'hello world'
        queue = 'test_functional_basic_nack'
        try:
            self.channel.queue.declare(queue)
            self.channel.basic.publish(payload, queue)

            message = self.channel.basic.get(queue, to_dict=True)

            result = self.channel.basic.nack(
                requeue=False,
                delivery_tag=message['method']['delivery_tag'])

            self.assertEqual(result, None)

            # Make sure the message wasn't requeued.
            self.assertFalse(self.channel.basic.get(queue, to_dict=True))
        finally:
            self.channel.queue.delete(queue)

    def test_functional_basic_nack_requeue(self):
        payload = 'hello world'
        queue = 'test_functional_basic_nack_requeue'
        try:
            self.channel.queue.declare(queue)
            self.channel.basic.publish(payload, queue)

            message = self.channel.basic.get(queue, to_dict=True)

            result = self.channel.basic.nack(
                requeue=True,
                delivery_tag=message['method']['delivery_tag'])

            self.assertEqual(result, None)

            # Make sure the message was requeued.
            self.assertIsInstance(self.channel.basic.get(queue, to_dict=True),
                                  dict)
        finally:
            self.channel.queue.delete(queue)

    def test_functional_basic_reject(self):
        payload = 'hello world'
        queue = 'test_functional_basic_reject'
        try:
            self.channel.queue.declare(queue)
            self.channel.basic.publish(payload, queue)

            message = self.channel.basic.get(queue, to_dict=True)

            result = self.channel.basic.reject(
                requeue=False,
                delivery_tag=message['method']['delivery_tag'])

            self.assertEqual(result, None)

            # Make sure the message wasn't requeued.
            self.assertFalse(self.channel.basic.get(queue, to_dict=True))
        finally:
            self.channel.queue.delete(queue)

    def test_functional_basic_reject_requeue(self):
        payload = 'hello world'
        queue = 'test_functional_basic_reject'
        try:
            self.channel.queue.declare(queue)
            self.channel.basic.publish(payload, queue)

            message = self.channel.basic.get(queue, to_dict=True)

            result = self.channel.basic.reject(
                requeue=True,
                delivery_tag=message['method']['delivery_tag'])

            self.assertEqual(result, None)

            # Make sure the message was requeued.
            self.assertIsInstance(self.channel.basic.get(queue, to_dict=True),
                                  dict)
        finally:
            self.channel.queue.delete(queue)

    def tearDown(self):
        self.channel.close()
        self.connection.close()
        self.assertFalse(self.logging_handler.messages['warning'])
        self.assertFalse(self.logging_handler.messages['error'])
        self.assertFalse(self.logging_handler.messages['critical'])
