import logging
import uuid
from datetime import datetime

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from amqpstorm import Message
from amqpstorm.exception import *

from amqpstorm.tests.utility import FakeChannel

logging.basicConfig(level=logging.DEBUG)


class MessageTests(unittest.TestCase):
    def test_message_create_new_message(self):
        body = b'Hello World'

        message = Message.create(None, body,
                                 properties={'key': 'value',
                                             'headers': {
                                                 b'name': b'eandersson'}
                                             })

        self.assertIsInstance(message, Message)
        self.assertEqual(message._body, body)

        result = message.to_dict()

        self.assertIsNone(result['method'])
        self.assertEqual(result['body'], body)
        self.assertEqual(result['properties']['key'], 'value')

    def test_message_default_properties(self):
        body = b'Hello World'

        message = Message.create(None, body)

        self.assertIsNone(message.app_id)
        self.assertIsNone(message.reply_to)
        self.assertIsNone(message.content_encoding)
        self.assertIsNone(message.content_type)
        self.assertIsNone(message.priority)
        self.assertIsNone(message.delivery_mode)
        self.assertIsInstance(message.message_id, str)
        self.assertIsInstance(message.correlation_id, str)
        self.assertIsInstance(message.timestamp, datetime)

    def test_message_app_id_custom_value(self):
        app_id = 'my-app'

        message = Message.create(None, '')
        message.app_id = app_id

        self.assertEqual(app_id, message.app_id)

    def test_message_id_custom_value(self):
        message_id = 'my-message-1'

        message = Message.create(None, '')
        message.message_id = message_id

        self.assertEqual(message_id, message.properties['message_id'])
        self.assertEqual(message_id, message._properties['message_id'])

    def test_message_timestamp_custom_value(self):
        dt = datetime.now()

        message = Message.create(None, '')
        message.timestamp = dt

        self.assertEqual(dt, message.timestamp)

    def test_message_content_encoding_custom_value(self):
        content_encoding = 'gzip'

        message = Message.create(None, '')
        message.content_encoding = content_encoding

        self.assertEqual(content_encoding, message.content_encoding)

    def test_message_content_type_custom_value(self):
        content_type = 'application/json'

        message = Message.create(None, '')
        message.content_type = content_type

        self.assertEqual(content_type, message.content_type)

    def test_message_delivery_mode_two(self):
        delivery_mode = 2

        message = Message.create(None, '')
        message.delivery_mode = delivery_mode

        self.assertEqual(delivery_mode, message.delivery_mode)

    def test_message_priority_three(self):
        priority = 3

        message = Message.create(None, '')
        message.priority = priority

        self.assertEqual(priority, message.priority)

    def test_message_correlation_id_custom_value(self):
        correlation_id = str(uuid.uuid4())

        message = Message.create(None, '')
        message.correlation_id = correlation_id

        self.assertEqual(correlation_id, message.correlation_id)

    def test_message_reply_to_custom_value(self):
        reply_to = str(uuid.uuid4())

        message = Message.create(None, '')
        message.reply_to = reply_to

        self.assertEqual(reply_to, message.reply_to)

    def test_message_do_not_override_properties(self):
        reply_to = 'hello_world',
        correlation_id = str(uuid.uuid4())
        timestamp = datetime.now()

        properties = {
            'reply_to': reply_to,
            'correlation_id': correlation_id,
            'timestamp': timestamp
        }

        message = Message.create(None, '', properties)

        self.assertEqual(reply_to, message.reply_to)
        self.assertEqual(correlation_id, message.correlation_id)
        self.assertEqual(timestamp, message.timestamp)

    def test_message_get_channel(self):
        class FakeClass(object):
            pass

        message = Message(body='',
                          channel=FakeClass())

        self.assertIsInstance(message.channel, FakeClass)

    def test_message_ack(self):
        delivery_tag = 123456
        message = Message.create(body='',
                                 channel=FakeChannel())
        message._method = {
            'delivery_tag': delivery_tag
        }

        message.ack()
        result = message.channel.result.pop(0)
        self.assertEqual(result[0], delivery_tag)
        self.assertEqual(result[1], False)

    def test_message_nack(self):
        delivery_tag = 123456
        message = Message.create(body='',
                                 channel=FakeChannel())
        message._method = {
            'delivery_tag': delivery_tag
        }

        message.nack(requeue=True)
        result = message.channel.result.pop(0)
        self.assertEqual(result[0], delivery_tag)
        self.assertEqual(result[1], False)
        self.assertEqual(result[2], True)

        message.nack(requeue=False)
        result = message.channel.result.pop(0)
        self.assertEqual(result[0], delivery_tag)
        self.assertEqual(result[1], False)
        self.assertEqual(result[2], False)

    def test_message_reject(self):
        delivery_tag = 123456
        message = Message.create(body='',
                                 channel=FakeChannel())
        message._method = {
            'delivery_tag': delivery_tag
        }

        message.reject(requeue=True)
        result = message.channel.result.pop(0)
        self.assertEqual(result[0], delivery_tag)
        self.assertEqual(result[1], True)

        message.reject(requeue=False)
        result = message.channel.result.pop(0)
        self.assertEqual(result[0], delivery_tag)
        self.assertEqual(result[1], False)

    def test_message_ack_raises_on_outbound(self):
        message = Message.create(body='',
                                 channel=None)

        self.assertRaises(AMQPMessageError, message.ack)

    def test_message_nack_raises_on_outbound(self):
        message = Message.create(body='',
                                 channel=None)

        self.assertRaises(AMQPMessageError, message.nack)

    def test_message_reject_raises_on_outbound(self):
        message = Message.create(body='',
                                 channel=None)

        self.assertRaises(AMQPMessageError, message.reject)

    def test_message_auto_decode_enabled(self):
        body = 'Hello World',
        message = Message(body=body,
                          properties={'key': 'value',
                                      'headers': {b'name': b'eandersson'}},
                          channel=None)

        self.assertEqual(body, message.body)
        self.assertIn('name', message.properties['headers'])
        self.assertIn(b'name', message._properties['headers'])
        self.assertIsInstance(message.properties['headers']['name'], str)

    def test_message_auto_decode_cache(self):
        body = 'Hello World',
        message = Message(body=body,
                          channel=None)

        self.assertEqual(body, message.body)
        message._body = 'invalidate'
        self.assertEqual(body, message.body)

    def test_message_auto_decode_when_method_is_none(self):
        message = Message(body='Hello World',
                          method=None,
                          channel=None)

        self.assertIsNone(message.method)

    def test_message_auto_decode_when_method_contains_list(self):
        method_data = {'key': [b'a', b'b']}

        message = Message(body='Hello World',
                          method=method_data,
                          channel=None)

        self.assertEqual(method_data['key'][0].decode('utf-8'),
                         message.method['key'][0])

    def test_message_auto_decode_when_method_is_tuple(self):
        method_data = (1, 2, 3, 4, 5)

        message = Message(body='Hello World',
                          method=method_data,
                          channel=None)

        self.assertEqual(method_data, message.method)
        self.assertEqual(method_data[0], message.method[0])
        self.assertEqual(method_data[4], message.method[4])

    def test_message_auto_decode_when_properties_contains_list(self):
        prop_data = [b'travis', 2, 3, 4, 5]

        message = Message(body='Hello World',
                          properties={'key': prop_data},
                          channel=None)

        self.assertIsInstance(message.properties['key'], list)
        self.assertEqual(prop_data[0].decode('utf-8'),
                         message.properties['key'][0])
        self.assertEqual(prop_data[4], message.properties['key'][4])

    def test_message_auto_decode_when_properties_contains_tuple(self):
        prop_data = (b'travis', 2, 3, 4, 5)

        message = Message(body='Hello World',
                          properties={'key': prop_data},
                          channel=None)

        self.assertIsInstance(message.properties['key'], tuple)
        self.assertEqual(prop_data[0].decode('utf-8'),
                         message.properties['key'][0])
        self.assertEqual(prop_data[4], message.properties['key'][4])

    def test_message_auto_decode_when_properties_contains_dict(self):
        prop_data = {
            'hello': b'travis'
        }

        message = Message(body='Hello World',
                          properties={'key': prop_data},
                          channel=None)

        self.assertIsInstance(message.properties['key'], dict)
        self.assertEqual(prop_data['hello'].decode('utf-8'),
                         message.properties['key']['hello'])

    def test_message_auto_decode_disabled(self):
        body = 'Hello World'
        message = Message(body=body,
                          properties={'key': 'value',
                                      'headers': {b'name': b'eandersson'}},
                          channel=None,
                          auto_decode=False)

        self.assertEqual(body, message.body)
        self.assertIn(b'name', message.properties['headers'])
        self.assertIsInstance(message.properties['headers'][b'name'], bytes)

    def test_message_update_property_with_decode(self):
        message = Message(None, auto_decode=True)
        message._update_properties('app_id', '123')
        self.assertEqual(message.properties['app_id'], '123')
        self.assertEqual(message._properties['app_id'], '123')

    def test_message_update_property_without_decode(self):
        message = Message.create(None, '', None)
        message._auto_decode = False
        message._update_properties('app_id', '123')
        self.assertEqual(message.properties['app_id'], '123')
        self.assertEqual(message._properties['app_id'], '123')

    def test_message_json(self):
        body = '{"key": "value"}'
        message = Message(body=body, channel=None)

        result = message.json()

        self.assertIsInstance(result, dict)
        self.assertEqual(result['key'], 'value')

    def test_message_dict(self):
        body = b'Hello World'
        properties = {'key': 'value'}
        method = {b'alternative': 'value'}
        message = Message(body=body,
                          properties=properties,
                          method=method,
                          channel=None)

        result = dict(message)

        self.assertIsInstance(result, dict)
        self.assertEqual(result['body'], body)
        self.assertEqual(result['properties'], properties)
        self.assertEqual(result['method'], method)

    def test_message_to_dict(self):
        body = b'Hello World'
        properties = {'key': 'value'}
        method = {b'alternative': 'value'}
        message = Message(body=body,
                          properties=properties,
                          method=method,
                          channel=None)

        result = message.to_dict()

        self.assertIsInstance(result, dict)
        self.assertEqual(result['body'], body)
        self.assertEqual(result['properties'], properties)
        self.assertEqual(result['method'], method)

    def test_message_to_tuple(self):
        body = b'Hello World'
        message = Message(body=body,
                          properties={'key': 'value'},
                          method={'key': 'value'},
                          channel=None)

        body, channel, method, properties = message.to_tuple()

        self.assertEqual(body, body)
        self.assertIsInstance(method, dict)
        self.assertIsInstance(properties, dict)
        self.assertIsNone(channel)
