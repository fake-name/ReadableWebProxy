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


class ExchangeFunctionalTests(unittest.TestCase):
    def setUp(self):
        self.logging_handler = MockLoggingHandler()
        logging.root.addHandler(self.logging_handler)
        self.connection = Connection(HOST, USERNAME, PASSWORD)
        self.channel = self.connection.channel()

    def test_functional_exchange_declare(self):
        self.channel.exchange.declare('test_functional_exchange_declare',
                                      passive=False,
                                      durable=True, auto_delete=True)
        self.channel.exchange.declare('test_functional_exchange_declare',
                                      passive=True)

    def test_functional_exchange_delete(self):
        self.channel.exchange.declare('test_functional_exchange_delete')
        self.channel.exchange.delete('test_functional_exchange_delete',
                                     if_unused=True)
        self.assertRaises(amqpstorm.AMQPChannelError,
                          self.channel.exchange.declare,
                          'test_functional_exchange_delete', passive=True)

    def test_functional_exchange_bind(self):
        self.channel.exchange.declare('exchange1')
        self.channel.exchange.declare('exchange2')

        self.assertEqual(self.channel.exchange.bind('exchange1', 'exchange2',
                                                    'routing_key'), {})

    def test_functional_exchange_unbind(self):
        self.channel.exchange.declare('exchange1')
        self.channel.exchange.declare('exchange2')
        self.channel.exchange.bind('exchange1', 'exchange2', 'routing_key')

        self.assertEqual(self.channel.exchange.unbind('exchange1', 'exchange2',
                                                      'routing_key'), {})

    def tearDown(self):
        self.channel.close()
        self.connection.close()
        self.assertFalse(self.logging_handler.messages['warning'])
        self.assertFalse(self.logging_handler.messages['error'])
        self.assertFalse(self.logging_handler.messages['critical'])
