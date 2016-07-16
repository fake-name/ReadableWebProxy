import logging

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from amqpstorm import exception
from amqpstorm.channel import Queue
from amqpstorm.channel import Channel

from amqpstorm.tests.utility import FakeConnection

logging.basicConfig(level=logging.DEBUG)


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
