import logging

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from amqpstorm.base import Stateful
from amqpstorm.base import BaseChannel

logging.basicConfig(level=logging.DEBUG)


class BasicChannelTests(unittest.TestCase):
    def test_base_channel_id(self):
        channel = BaseChannel(1337)
        self.assertEqual(channel.channel_id, 1337)

    def test_base_channel_add_consumer_tag(self):
        channel = BaseChannel(0)
        channel.add_consumer_tag('my_tag')
        self.assertEqual(channel.consumer_tags[0], 'my_tag')

    def test_base_channel_remove_single_consumer_tag(self):
        channel = BaseChannel(0)
        channel.add_consumer_tag('1')
        channel.add_consumer_tag('2')
        channel.remove_consumer_tag('1')
        self.assertEqual(len(channel.consumer_tags), 1)
        self.assertEqual(channel.consumer_tags[0], '2')

    def test_base_channel_remove_all_consumer_tags(self):
        channel = BaseChannel(0)
        channel.add_consumer_tag('my_tag')
        channel.add_consumer_tag('my_tag')
        channel.add_consumer_tag('my_tag')
        channel.remove_consumer_tag()
        self.assertEqual(len(channel.consumer_tags), 0)


class StatefulTests(unittest.TestCase):
    def test_stateful_default_is_closed(self):
        stateful = Stateful()
        self.assertTrue(stateful.is_closed)

    def test_stateful_set_open(self):
        stateful = Stateful()
        stateful.set_state(Stateful.OPEN)
        self.assertTrue(stateful.is_open)

    def test_stateful_set_opening(self):
        stateful = Stateful()
        stateful.set_state(Stateful.OPENING)
        self.assertTrue(stateful.is_opening)

    def test_stateful_set_closed(self):
        stateful = Stateful()
        stateful.set_state(Stateful.CLOSED)
        self.assertTrue(stateful.is_closed)

    def test_stateful_set_closing(self):
        stateful = Stateful()
        stateful.set_state(Stateful.CLOSING)
        self.assertTrue(stateful.is_closing)
