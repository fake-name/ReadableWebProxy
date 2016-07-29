import logging

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from pamqp.specification import Exchange as pamqp_exchange

from amqpstorm import exception
from amqpstorm.channel import Exchange
from amqpstorm.channel import Channel

from amqpstorm.tests.utility import FakeConnection

logging.basicConfig(level=logging.DEBUG)


class ExchangeTests(unittest.TestCase):
    def test_exchange_declare(self):
        def on_declare(*_):
            channel.rpc.on_frame(pamqp_exchange.DeclareOk())

        connection = FakeConnection(on_write=on_declare)
        channel = Channel(0, connection, 0.1)
        channel.set_state(Channel.OPEN)
        exchange = Exchange(channel)
        self.assertFalse(exchange.declare())

    def test_exchange_delete(self):
        def on_delete(*_):
            channel.rpc.on_frame(pamqp_exchange.DeleteOk())

        connection = FakeConnection(on_write=on_delete)
        channel = Channel(0, connection, 0.1)
        channel.set_state(Channel.OPEN)
        exchange = Exchange(channel)
        self.assertFalse(exchange.delete())

    def test_exchange_bind(self):
        def on_bind(*_):
            channel.rpc.on_frame(pamqp_exchange.BindOk())

        connection = FakeConnection(on_write=on_bind)
        channel = Channel(0, connection, 0.1)
        channel.set_state(Channel.OPEN)
        exchange = Exchange(channel)
        self.assertFalse(exchange.bind())

    def test_exchange_unbind(self):
        def on_unbind(*_):
            channel.rpc.on_frame(pamqp_exchange.UnbindOk())

        connection = FakeConnection(on_write=on_unbind)
        channel = Channel(0, connection, 0.1)
        channel.set_state(Channel.OPEN)
        exchange = Exchange(channel)
        self.assertFalse(exchange.unbind())


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
