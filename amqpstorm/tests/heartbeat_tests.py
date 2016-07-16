import logging
import time

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from amqpstorm.heartbeat import Heartbeat
from amqpstorm.exception import AMQPConnectionError

logging.basicConfig(level=logging.DEBUG)


class HeartbeatTests(unittest.TestCase):
    def test_heartbeat_start(self):
        heartbeat = Heartbeat(1)

        self.assertFalse(heartbeat._running.is_set())

        heartbeat.start([])

        self.assertTrue(heartbeat._running.is_set())

        self.assertIsNotNone(heartbeat._timer)
        heartbeat.stop()

    def test_heartbeat_disabled(self):
        heartbeat = Heartbeat(0)

        self.assertFalse(heartbeat._running.is_set())

        heartbeat.start([])

        self.assertFalse(heartbeat._running.is_set())
        self.assertIsNone(heartbeat._timer)

    def test_heartbeat_stop(self):
        heartbeat = Heartbeat(1)

        self.assertFalse(heartbeat._running.is_set())

        heartbeat.start([])

        self.assertTrue(heartbeat._running.is_set())

        heartbeat.stop()

        self.assertFalse(heartbeat._running.is_set())
        self.assertIsNone(heartbeat._timer)

    def test_heartbeat_interval(self):
        heartbeat = Heartbeat(60)

        self.assertEqual(heartbeat._interval, 60)
        self.assertEqual(heartbeat._threshold, 0)

    def test_heartbeat_register_reads(self):
        heartbeat = Heartbeat(1)
        heartbeat.start([])
        time.sleep(0.01)
        for _ in range(100):
            heartbeat.register_read()

        self.assertEqual(heartbeat._reads_since_check, 100)

        heartbeat.stop()

    def test_heartbeat_register_writes(self):
        heartbeat = Heartbeat(1)
        heartbeat.start([])
        time.sleep(0.01)
        for _ in range(100):
            heartbeat.register_write()

        self.assertEqual(heartbeat._writes_since_check, 100)

        heartbeat.stop()

    def test_heartbeat_do_not_execute_life_signs_when_stopped(self):
        heartbeat = Heartbeat(60)

        self.assertFalse(heartbeat._check_for_life_signs())

    def test_heartbeat_do_not_start_new_timer_when_stopped(self):
        heartbeat = Heartbeat(60)

        self.assertIsNone(heartbeat._timer)

        heartbeat._start_new_timer()

        self.assertIsNone(heartbeat._timer)

    def test_heartbeat_basic_raise_on_missed_heartbeats(self):
        def fake_function():
            pass

        heartbeat = Heartbeat(0.01, fake_function)
        exceptions = []
        heartbeat.start(exceptions)
        time.sleep(0.1)

        self.assertGreater(len(heartbeat._exceptions), 0)

        heartbeat.stop()

    def test_heartbeat_send_heartbeat(self):
        self.beats = 0

        def send_heartbeat():
            self.beats += 1

        heartbeat = Heartbeat(10, send_heartbeat=send_heartbeat)
        heartbeat._running.set()

        for _ in range(10):
            heartbeat.register_read()
            self.assertTrue(heartbeat._check_for_life_signs())
        self.assertEqual(self.beats, 10)

    def test_heartbeat_threshold_reset(self):
        heartbeat = Heartbeat(10)
        heartbeat._running.set()
        heartbeat.register_write()

        self.assertEqual(heartbeat._threshold, 0)
        self.assertTrue(heartbeat._check_for_life_signs())
        self.assertEqual(heartbeat._threshold, 1)

        heartbeat.register_write()
        heartbeat.register_read()

        self.assertTrue(heartbeat._check_for_life_signs())
        self.assertEqual(heartbeat._threshold, 0)

    def test_heartbeat_raise_after_threshold(self):
        heartbeat = Heartbeat(1)
        exceptions = []
        heartbeat.start(exceptions)
        heartbeat.register_write()

        self.assertTrue(heartbeat._check_for_life_signs())

        heartbeat.register_write()

        self.assertFalse(heartbeat._check_for_life_signs())
        self.assertTrue(exceptions)

        heartbeat.stop()

    def test_heartbeat_raise_when_check_for_life_when_exceptions_not_set(self):
        heartbeat = Heartbeat(1)
        heartbeat._running.set()
        heartbeat._reads_since_check = 0
        heartbeat._threshold = 3
        heartbeat.register_write()

        # Normally the exception should be passed down to the list of
        # exceptions in the connection, but if that list for some obscure
        # reason is None, we should raise directly in _check_for_life_signs.
        self.assertRaises(AMQPConnectionError, heartbeat._check_for_life_signs)

    def test_heartbeat_extended_loop(self):
        self.beats = 0

        def send_heartbeat():
            self.beats += 1

        heartbeat = Heartbeat(10, send_heartbeat=send_heartbeat)
        heartbeat._running.set()
        heartbeat.register_read()

        # Miss one write/
        self.assertTrue(heartbeat._check_for_life_signs())

        for _ in range(1000):
            heartbeat.register_read()
            heartbeat.register_write()

            self.assertFalse(heartbeat._threshold)
            self.assertTrue(heartbeat._check_for_life_signs())

        heartbeat.register_write()

        # Miss one read.
        self.assertTrue(heartbeat._check_for_life_signs())

        self.assertEqual(heartbeat._threshold, 1)
        self.assertEqual(self.beats, 1)

        heartbeat.register_read()
        heartbeat.register_write()
        self.assertTrue(heartbeat._check_for_life_signs())

        self.assertEqual(heartbeat._threshold, 0)
