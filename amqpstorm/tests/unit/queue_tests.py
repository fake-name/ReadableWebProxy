import logging

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from pamqp.specification import Queue as pamqp_queue

from amqpstorm import exception
from amqpstorm.channel import Queue
from amqpstorm.channel import Channel

from amqpstorm.tests.utility import FakeConnection

logging.basicConfig(level=logging.DEBUG)


class QueueTests(unittest.TestCase):
    def test_queue_declare(self):
        def on_declare(*_):
            channel.rpc.on_frame(pamqp_queue.DeclareOk())

        connection = FakeConnection(on_write=on_declare)
        channel = Channel(0, connection, 0.1)
        channel.set_state(Channel.OPEN)
        queue = Queue(channel)

        self.assertEqual(queue.declare(),
                         {
                             'queue': '',
                             'message_count': 0,
                             'consumer_count': 0
                         })

    def test_queue_delete(self):
        def on_delete(*_):
            channel.rpc.on_frame(pamqp_queue.DeleteOk())

        connection = FakeConnection(on_write=on_delete)
        channel = Channel(0, connection, 0.1)
        channel.set_state(Channel.OPEN)
        exchange = Queue(channel)

        self.assertEqual(exchange.delete(), {'message_count': 0})

    def test_queue_purge(self):
        def on_purge(*_):
            channel.rpc.on_frame(pamqp_queue.PurgeOk())

        connection = FakeConnection(on_write=on_purge)
        channel = Channel(0, connection, 0.1)
        channel.set_state(Channel.OPEN)
        exchange = Queue(channel)

        self.assertEqual(exchange.purge(), {'message_count': 0})

    def test_queue_bind(self):
        def on_bind(*_):
            channel.rpc.on_frame(pamqp_queue.BindOk())

        connection = FakeConnection(on_write=on_bind)
        channel = Channel(0, connection, 0.1)
        channel.set_state(Channel.OPEN)
        exchange = Queue(channel)

        self.assertFalse(exchange.bind())

    def test_queue_unbind(self):
        def on_unbind(*_):
            channel.rpc.on_frame(pamqp_queue.UnbindOk())

        connection = FakeConnection(on_write=on_unbind)
        channel = Channel(0, connection, 0.1)
        channel.set_state(Channel.OPEN)
        exchange = Queue(channel)

        self.assertFalse(exchange.unbind())


class QueueExceptionTests(unittest.TestCase):
    def test_queue_declare_invalid_parameter(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        queue = Queue(channel)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'queue should be a string',
                                queue.declare, None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'passive should be a boolean',
                                queue.declare, 'unittest', None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'durable should be a boolean',
                                queue.declare, 'unittest', True, None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'exclusive should be a boolean',
                                queue.declare, 'unittest', True, True,
                                None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'auto_delete should be a boolean',
                                queue.declare, 'unittest', True, True,
                                True, None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'arguments should be a dict or None',
                                queue.declare, 'unittest', True, True,
                                True, True, [])

    def test_queue_delete_invalid_parameter(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        queue = Queue(channel)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'queue should be a string',
                                queue.delete, None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'if_unused should be a boolean',
                                queue.delete, '', None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'if_empty should be a boolean',
                                queue.delete, '', True, None)

    def test_queue_purge_invalid_parameter(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        queue = Queue(channel)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'queue should be a string',
                                queue.purge, None)

    def test_queue_bind_invalid_parameter(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        queue = Queue(channel)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'queue should be a string',
                                queue.bind, None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'exchange should be a string',
                                queue.bind, '', None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'routing_key should be a string',
                                queue.bind, '', '', None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'arguments should be a dict or None',
                                queue.bind, '', '', '', [])

    def test_queue_unbind_invalid_parameter(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        queue = Queue(channel)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'queue should be a string',
                                queue.unbind, None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'exchange should be a string',
                                queue.unbind, '', None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'routing_key should be a string',
                                queue.unbind, '', '', None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'arguments should be a dict or None',
                                queue.unbind, '', '', '', [])
