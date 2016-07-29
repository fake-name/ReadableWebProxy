import imp
import logging
import sys
import threading
import time
import uuid

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from amqpstorm import Connection
from amqpstorm import AMQPConnectionError
from amqpstorm import compatibility

HOST = '127.0.0.1'
USERNAME = 'guest'
PASSWORD = 'guest'
URI = 'amqp://guest:guest@127.0.0.1:5672/%2F'

logging.basicConfig(level=logging.DEBUG)

LOGGER = logging.getLogger(__name__)


class OpenCloseChannelLoopTest(unittest.TestCase):
    connection = None
    channel = None
    queue_name = 'test.open.close'

    def setUp(self):
        self.connection = Connection(HOST, USERNAME, PASSWORD, lazy=True)

    def test_functional_open_close_channel_loop(self):
        for _ in range(100):
            self.connection.open()
            self.channel = self.connection.channel()

            # Verify that the Connection/Channel has been opened properly.
            self.assertIsNotNone(self.connection._io.socket)
            self.assertIsNotNone(self.connection._io.poller)
            self.assertTrue(self.channel.is_open)
            self.assertTrue(self.connection.is_open)

            self.channel.queue.declare(self.queue_name)
            self.channel.basic.publish(body=str(uuid.uuid4()),
                                       routing_key=self.queue_name)
            self.channel.close()
            self.connection.close()

            # Verify that the Connection/Channel has been closed properly.
            self.assertTrue(self.channel.is_closed)
            self.assertTrue(self.connection.is_closed)
            self.assertIsNone(self.connection._io.socket)
            self.assertIsNone(self.connection._io.poller)

        time.sleep(0.1)

        self.assertEqual(threading.activeCount(), 1,
                         msg='Current Active threads: %s'
                             % threading._active)

    def tearDown(self):
        self.connection = Connection(HOST, USERNAME, PASSWORD)
        self.channel = self.connection.channel()
        self.channel.queue.delete(self.queue_name)
        self.channel.close()
        self.connection.close()


class OpenMultipleChannelTest(unittest.TestCase):
    connection = None
    channel = None

    def setUp(self):
        self.connection = Connection(HOST, USERNAME, PASSWORD, lazy=True)

    def test_functional_open_multiple_channels(self):
        self.connection.open()
        self.assertIsNotNone(self.connection._io.socket)
        self.assertIsNotNone(self.connection._io.poller)
        self.assertTrue(self.connection.is_open)
        for index in range(255):
            channel = self.connection.channel()

            # Verify that the Channel has been opened properly.
            self.assertTrue(channel.is_open)
            self.assertEqual(int(channel), index + 1)

        self.connection.close()

        time.sleep(0.1)

        self.assertTrue(self.connection.is_closed)
        self.assertIsNone(self.connection._io.socket)
        self.assertIsNone(self.connection._io.poller)
        self.assertEqual(threading.activeCount(), 1,
                         msg='Current Active threads: %s'
                             % threading._active)

    def tearDown(self):
        self.connection.close()


class Publish50kTest(unittest.TestCase):
    connection = None
    channel = None
    messages_to_send = 50000
    queue_name = 'test.basic.50k'

    def setUp(self):
        self.connection = Connection(HOST, USERNAME, PASSWORD)
        self.channel = self.connection.channel()
        self.channel.queue.declare(self.queue_name)
        self.channel.queue.purge(self.queue_name)

    def test_functional_publish_50k_messages(self):
        body = str(uuid.uuid4())
        # Publish 50k Messages.
        for _ in range(self.messages_to_send):
            self.channel.basic.publish(body=body,
                                       routing_key=self.queue_name)
        result = {}

        # Let's give RabbitMQ a few seconds to catch up.
        for _ in range(5):
            time.sleep(0.5)
            result = self.channel.queue.declare(queue=self.queue_name,
                                                passive=True)
            if self.messages_to_send == result['message_count']:
                break

        self.assertEqual(result['message_count'], self.messages_to_send)

    def tearDown(self):
        self.channel.queue.delete(self.queue_name)
        self.channel.close()
        self.connection.close()


class ConnectionWithoutSSLSupportTest(unittest.TestCase):
    def test_functional_ssl_connection_without_ssl(self):
        restore_func = sys.modules['ssl']
        try:
            sys.modules['ssl'] = None
            imp.reload(compatibility)
            self.assertIsNone(compatibility.ssl)
            self.assertRaisesRegexp(AMQPConnectionError,
                                    'Python not compiled with '
                                    'support for TLSv1 or higher',
                                    Connection, HOST, USERNAME,
                                    PASSWORD, ssl=True)
        finally:
            sys.modules['ssl'] = restore_func
            imp.reload(compatibility)
