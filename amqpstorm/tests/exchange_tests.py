import logging

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from amqpstorm import exception
from amqpstorm.channel import Exchange
from amqpstorm.channel import Channel

from amqpstorm.tests.utility import FakeConnection

logging.basicConfig(level=logging.DEBUG)


class ExchangeExceptionTests(unittest.TestCase):
    def test_exchange_declare_invalid_parameter(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        exchange = Exchange(channel)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'exchange should be a string',
                                exchange.declare, None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'exchange_type should be a string',
                                exchange.declare, 'unittest', None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'passive should be a boolean',
                                exchange.declare, 'unittest', 'unittest', None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'durable should be a boolean',
                                exchange.declare, 'unittest', 'unittest', True,
                                None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'auto_delete should be a boolean',
                                exchange.declare, 'unittest', 'unittest', True,
                                True, None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'arguments should be a dict or None',
                                exchange.declare, 'unittest', 'unittest', True,
                                True, True, [])

    def test_exchange_delete_invalid_parameter(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        exchange = Exchange(channel)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'exchange should be a string',
                                exchange.delete, None)

    def test_exchange_bind_invalid_parameter(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        exchange = Exchange(channel)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'destination should be a string',
                                exchange.bind, None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'source should be a string',
                                exchange.bind, '', None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'routing_key should be a string',
                                exchange.bind, '', '', None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'arguments should be a dict or None',
                                exchange.bind, '', '', '', [])

    def test_exchange_unbind_invalid_parameter(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        exchange = Exchange(channel)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'destination should be a string',
                                exchange.unbind, None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'source should be a string',
                                exchange.unbind, '', None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'routing_key should be a string',
                                exchange.unbind, '', '', None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'arguments should be a dict or None',
                                exchange.unbind, '', '', '', [])
