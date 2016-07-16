import logging

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from amqpstorm import Connection
from amqpstorm.exception import AMQPChannelError
from amqpstorm.tests.utility import MockLoggingHandler

HOST = '127.0.0.1'
USERNAME = 'guest'
PASSWORD = 'guest'

logging.basicConfig(level=logging.DEBUG)

LOGGER = logging.getLogger(__name__)


class TxFunctionalTests(unittest.TestCase):
    def setUp(self):
        self.logging_handler = MockLoggingHandler()
        logging.root.addHandler(self.logging_handler)
        self.connection = Connection(HOST, USERNAME, PASSWORD)
        self.channel = self.connection.channel()

    def test_functional_tx_select(self):
        self.channel.tx.select()

    def test_functional_tx_select_multiple(self):
        for _ in range(10):
            self.channel.tx.select()

    def test_functional_tx_commit(self):
        self.channel.tx.select()

        payload = 'hello world'
        queue = 'test_functional_tx_commit'
        try:
            self.channel.queue.declare(queue)
            self.channel.basic.publish(payload, queue)

            self.channel.tx.commit()

            queue_status = self.channel.queue.declare(queue, passive=True)
            self.assertEqual(queue_status['message_count'], 1)
        finally:
            self.channel.queue.delete(queue)

    def test_functional_tx_commit_multiple(self):
        self.channel.tx.select()

        payload = 'hello world'
        queue = 'test_functional_tx_commit'
        try:
            self.channel.queue.declare(queue)
            for _ in range(10):
                self.channel.basic.publish(payload, queue)

            self.channel.tx.commit()

            queue_status = self.channel.queue.declare(queue, passive=True)
            self.assertEqual(queue_status['message_count'], 10)
        finally:
            self.channel.queue.delete(queue)

    def test_functional_tx_commit_without_select(self):
        self.assertRaisesRegexp(AMQPChannelError,
                                'Channel 1 was closed by remote server: '
                                'PRECONDITION_FAILED - channel is not '
                                'transactional', self.channel.tx.commit)

    def test_functional_tx_rollback(self):
        self.channel.tx.select()

        payload = 'hello world'
        queue = 'test_functional_tx_rollback'
        try:
            self.channel.queue.declare(queue)
            self.channel.basic.publish(payload, queue)

            self.channel.tx.rollback()

            queue_status = self.channel.queue.declare(queue, passive=True)
            self.assertEqual(queue_status['message_count'], 0)
        finally:
            self.channel.queue.delete(queue)

    def test_functional_tx_rollback_multiple(self):
        self.channel.tx.select()

        payload = 'hello world'
        queue = 'test_functional_tx_rollback'
        try:
            self.channel.queue.declare(queue)
            for _ in range(10):
                self.channel.basic.publish(payload, queue)

            self.channel.tx.rollback()

            queue_status = self.channel.queue.declare(queue, passive=True)
            self.assertEqual(queue_status['message_count'], 0)
        finally:
            self.channel.queue.delete(queue)

    def test_functional_tx_rollback_without_select(self):
        self.assertRaisesRegexp(AMQPChannelError,
                                'Channel 1 was closed by remote server: '
                                'PRECONDITION_FAILED - channel is not '
                                'transactional', self.channel.tx.rollback)

    def tearDown(self):
        self.channel.close()
        self.connection.close()
        self.assertFalse(self.logging_handler.messages['warning'])
        self.assertFalse(self.logging_handler.messages['error'])
        self.assertFalse(self.logging_handler.messages['critical'])
