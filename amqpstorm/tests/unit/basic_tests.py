# -*- coding: utf-8 -*-
import logging
import random
import string
import sys
import uuid

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from pamqp.body import ContentBody
from pamqp.header import ContentHeader
from pamqp.specification import Basic as spec_basic

from amqpstorm import exception
from amqpstorm.channel import Basic
from amqpstorm.channel import Channel
from amqpstorm.compatibility import RANGE
from amqpstorm.tests.utility import FakeConnection

logging.basicConfig(level=logging.DEBUG)


class BasicTests(unittest.TestCase):
    def test_basic_publish(self):
        message = str(uuid.uuid4())
        exchange = 'test'
        routing_key = 'hello'
        properties = {'headers': {
            'key': 'value'
        }}

        connection = FakeConnection()
        channel = Channel(9, connection, 0.0001)
        channel.set_state(Channel.OPEN)
        basic = Basic(channel)
        basic.publish(body=message,
                      routing_key=routing_key,
                      exchange=exchange,
                      properties=properties,
                      mandatory=True,
                      immediate=True)

        channel_id, payload = connection.frames_out.pop()
        basic_publish, content_header, content_body = payload

        # Verify Channel ID
        self.assertEqual(channel_id, 9)

        # Verify Classes
        self.assertIsInstance(basic_publish, spec_basic.Publish)
        self.assertIsInstance(content_header, ContentHeader)
        self.assertIsInstance(content_body, ContentBody)

        # Verify Content
        self.assertEqual(message, content_body.value.decode('utf-8'))
        self.assertEqual(exchange, basic_publish.exchange)
        self.assertEqual(routing_key, basic_publish.routing_key)
        self.assertTrue(basic_publish.immediate)
        self.assertTrue(basic_publish.mandatory)
        self.assertIn('key', dict(content_header.properties)['headers'])

    def test_basic_publish_confirms_ack(self):
        message = str(uuid.uuid4())

        def on_publish_return_ack(*_):
            channel.rpc.on_frame(spec_basic.Ack())

        connection = FakeConnection(on_write=on_publish_return_ack)
        channel = Channel(9, connection, 1)
        channel.confirming_deliveries = True
        channel.set_state(Channel.OPEN)
        basic = Basic(channel)

        self.assertTrue(basic.publish(body=message,
                                      routing_key='unittest'))

    def test_basic_publish_confirms_nack(self):
        message = str(uuid.uuid4())

        def on_publish_return_nack(*_):
            channel.rpc.on_frame(spec_basic.Nack())

        connection = FakeConnection(on_write=on_publish_return_nack)
        channel = Channel(9, connection, 1)
        channel.confirming_deliveries = True
        channel.set_state(Channel.OPEN)
        basic = Basic(channel)

        self.assertFalse(basic.publish(body=message,
                                       routing_key='unittest'))

    def test_basic_create_content_body(self):
        basic = Basic(None)

        message = b'Hello World!'
        results = []
        for frame in basic._create_content_body(message):
            results.append(frame)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].value, message)

    def test_basic_create_content_body_growing(self):
        basic = Basic(None)
        long_string = ''.join(random.choice(string.ascii_letters)
                              for _ in RANGE(32768))

        for index in RANGE(32768):
            results = []
            message = long_string[:index + 1]
            for frame in basic._create_content_body(message):
                results.append(frame)

            # Rebuild the string
            result_body = ''
            for frame in results:
                result_body += frame.value

            self.assertEqual(result_body, message)

    def test_basic_create_content_body_long_string(self):
        basic = Basic(None)

        message = b'Hello World!' * 80960
        results = []
        for frame in basic._create_content_body(message):
            results.append(frame)

        self.assertEqual(len(results), 8)

        # Rebuild the string
        result_body = b''
        for frame in results:
            result_body += frame.value

        # Confirm that it matches the original string.
        self.assertEqual(result_body, message)

    def test_basic_get_content_body(self):
        message = b'Hello World!'
        body = ContentBody(value=message)
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        basic = Basic(channel)
        uuid = channel.rpc.register_request([body.name])
        channel.rpc.on_frame(body)

        self.assertEqual(basic._get_content_body(uuid, len(message)),
                         message)

    def test_basic_get_content_body_break_on_none_value(self):
        body = ContentBody(value=None)
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        basic = Basic(channel)
        uuid = channel.rpc.register_request([body.name])
        channel.rpc.on_frame(body)

        self.assertEqual(basic._get_content_body(uuid, 10), b'')

    @unittest.skipIf(sys.version_info[0] == 2, 'No bytes decoding in Python 2')
    def test_basic_py3_utf_8_payload(self):
        message = 'Hellå World!'
        basic = Basic(None)
        payload = basic._handle_utf8_payload(message, {})

        self.assertEqual(payload, b'Hell\xc3\xa5 World!')

    @unittest.skipIf(sys.version_info[0] == 3, 'No unicode obj in Python 3')
    def test_basic_py2_utf_8_payload(self):
        message = u'Hellå World!'
        basic = Basic(None)
        properties = {}
        payload = basic._handle_utf8_payload(message, properties)

        self.assertEqual(payload, 'Hell\xc3\xa5 World!')

    def test_basic_content_not_in_properties(self):
        message = 'Hello World!'
        basic = Basic(None)
        properties = {}
        basic._handle_utf8_payload(message, properties)

        self.assertEqual(properties['content_encoding'], 'utf-8')

    def test_basic_consume_add_tag(self):
        tag = 'unittest'
        channel = Channel(0, None, 1)
        basic = Basic(channel)

        self.assertEqual(basic._consume_add_and_get_tag({'consumer_tag': tag}),
                         tag)
        self.assertEqual(channel.consumer_tags[0], tag)

    def test_basic_consume_rpc(self):
        tag = 'unittest'

        def on_publish_return_ack(_, frame):
            self.assertIsInstance(frame, spec_basic.Consume)
            self.assertEqual(frame.arguments, {})
            self.assertEqual(frame.consumer_tag, tag)
            self.assertEqual(frame.exclusive, True)
            self.assertEqual(frame.no_ack, True)
            self.assertEqual(frame.exclusive, True)
            self.assertEqual(frame.queue, '')
            channel.rpc.on_frame(spec_basic.ConsumeOk(tag))

        connection = FakeConnection(on_write=on_publish_return_ack)
        channel = Channel(9, connection, 1)
        channel.set_state(channel.OPEN)
        basic = Basic(channel)

        self.assertEqual(
            basic._consume_rpc_request({}, tag, True, True, True, ''),
            {'consumer_tag': 'unittest'})


class BasicExceptionTests(unittest.TestCase):
    def test_basic_qos_invalid_parameter(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        basic = Basic(channel)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'prefetch_count should be an integer',
                                basic.qos, 'unittest')

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'prefetch_size should be an integer',
                                basic.qos, 1, 'unittest')

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'global_ should be a boolean',
                                basic.qos, 1, 1, 'unittest')

    def test_basic_get_invalid_parameter(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        basic = Basic(channel)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'queue should be a string',
                                basic.get, None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'no_ack should be a boolean',
                                basic.get, '', 'unittest')

        channel.consumer_tags.append('unittest')

        self.assertRaisesRegexp(exception.AMQPChannelError,
                                "Cannot call 'get' when channel "
                                "is set to consume",
                                basic.get, '', True, 'unittest')

    def test_basic_recover_invalid_parameter(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        basic = Basic(channel)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'requeue should be a boolean',
                                basic.recover, None)

    def test_basic_consume_invalid_parameter(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        basic = Basic(channel)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'queue should be a string',
                                basic.consume, None, 1)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'consumer_tag should be a string',
                                basic.consume, None, '', 1)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'exclusive should be a boolean',
                                basic.consume, None, '', '', None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'no_ack should be a boolean',
                                basic.consume, None, '', '', True, None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'no_local should be a boolean',
                                basic.consume, None, '', '', True, True, None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'arguments should be a dict or None',
                                basic.consume, None, '', '', True, True, True,
                                [])

    def test_basic_cancel_invalid_parameter(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        basic = Basic(channel)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'consumer_tag should be a string',
                                basic.cancel, None)

    def test_basic_publish_invalid_parameter(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        basic = Basic(channel)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'body should be a string',
                                basic.publish, None, '')

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'routing_key should be a string',
                                basic.publish, '', None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'exchange should be a string',
                                basic.publish, '', '', None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'properties should be a dict or None',
                                basic.publish, '', '', '', [])

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'properties should be a dict or None',
                                basic.publish, '', '', '', 1)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'mandatory should be a boolean',
                                basic.publish, '', '', '', {}, None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'immediate should be a boolean',
                                basic.publish, '', '', '', {}, True, None)

    def test_basic_ack_invalid_parameter(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        basic = Basic(channel)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'delivery_tag should be an integer or None',
                                basic.ack, 'unittest')

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'multiple should be a boolean',
                                basic.ack, 1, None)

    def test_basic_nack_invalid_parameter(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        basic = Basic(channel)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'delivery_tag should be an integer or None',
                                basic.nack, 'unittest')

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'multiple should be a boolean',
                                basic.nack, 1, None)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'requeue should be a boolean',
                                basic.nack, 1, True, None)

    def test_basic_reject_invalid_parameter(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        basic = Basic(channel)

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'delivery_tag should be an integer or None',
                                basic.reject, 'unittest')

        self.assertRaisesRegexp(exception.AMQPInvalidArgument,
                                'requeue should be a boolean',
                                basic.reject, 1, None)

    def test_basic_get_content_body_timeout_error(self):
        message = b'Hello World!'
        body = ContentBody(value=message)
        channel = Channel(0, FakeConnection(), 0.0001)
        channel.set_state(Channel.OPEN)
        basic = Basic(channel)
        uuid = channel.rpc.register_request([body.name])

        self.assertRaises(exception.AMQPChannelError, basic._get_content_body,
                          uuid, len(message))

    def test_basic_publish_confirms_raises_on_timeout(self):
        message = str(uuid.uuid4())

        connection = FakeConnection()
        channel = Channel(9, connection, 0.01)
        channel.confirming_deliveries = True
        channel.set_state(Channel.OPEN)
        basic = Basic(channel)

        self.assertRaisesRegexp(exception.AMQPChannelError,
                                "rpc requests",
                                basic.publish, body=message,
                                routing_key='unittest')

    def test_basic_publish_confirms_raises_on_invalid_frame(self):
        message = str(uuid.uuid4())

        def on_publish_return_invalid_frame(*_):
            channel.rpc.on_frame(spec_basic.Cancel())

        connection = FakeConnection(on_write=on_publish_return_invalid_frame)
        channel = Channel(9, connection, 0.01)
        channel.confirming_deliveries = True
        channel.set_state(Channel.OPEN)
        basic = Basic(channel)

        self.assertRaisesRegexp(exception.AMQPChannelError,
                                "rpc requests",
                                basic.publish, body=message,
                                routing_key='unittest')
