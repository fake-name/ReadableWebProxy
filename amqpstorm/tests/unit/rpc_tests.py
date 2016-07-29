import logging
import time

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from amqpstorm.rpc import Rpc
from amqpstorm.exception import AMQPChannelError

from amqpstorm.tests.utility import FakeConnection
from amqpstorm.tests.utility import FakePayload

logging.basicConfig(level=logging.DEBUG)


class RpcTests(unittest.TestCase):
    def test_rpc_register_request(self):
        rpc = Rpc(FakeConnection())
        uuid = rpc.register_request(['Test'])
        self.assertEqual(len(rpc._request), 1)
        for key in rpc._request:
            self.assertEqual(uuid, rpc._request[key])

    def test_rpc_get_request(self):
        rpc = Rpc(FakeConnection())
        uuid = rpc.register_request(['Test'])
        self.assertTrue(rpc.on_frame(FakePayload(name='Test')))
        self.assertIsInstance(rpc.get_request(uuid=uuid, raw=True),
                              FakePayload)

    def test_rpc_get_request_multiple_1(self):
        rpc = Rpc(FakeConnection())
        uuid = rpc.register_request(['Test'])
        for index in range(1000):
            rpc.on_frame(FakePayload(name='Test', value=index))
        for index in range(1000):
            result = rpc.get_request(uuid=uuid, raw=True, multiple=True)
            self.assertEqual(result.value, index)

        rpc.remove(uuid)

    def test_rpc_get_request_multiple_2(self):
        rpc = Rpc(FakeConnection())
        uuid = rpc.register_request(['Test'])
        for index in range(1000):
            rpc.on_frame(FakePayload(name='Test', value=index))
            result = rpc.get_request(uuid=uuid, raw=True, multiple=True)
            self.assertEqual(result.value, index)

        rpc.remove(uuid)

    def test_rpc_remove(self):
        rpc = Rpc(FakeConnection())
        uuid = rpc.register_request(['Test'])
        self.assertEqual(len(rpc._request), 1)
        self.assertEqual(len(rpc._response), 1)
        self.assertEqual(len(rpc._response[uuid]), 0)
        rpc.on_frame(FakePayload(name='Test'))
        rpc.remove(uuid)
        self.assertEqual(len(rpc._request), 0)
        self.assertEqual(len(rpc._response), 0)

    def test_rpc_remove_multiple(self):
        rpc = Rpc(FakeConnection())
        uuid = rpc.register_request(['Test'])
        for index in range(1000):
            rpc.on_frame(FakePayload(name='Test', value=index))
        self.assertEqual(len(rpc._request), 1)
        self.assertEqual(len(rpc._response[uuid]), 1000)
        rpc.remove(uuid)
        self.assertEqual(len(rpc._request), 0)
        self.assertEqual(len(rpc._response), 0)

    def test_rpc_remove_request(self):
        rpc = Rpc(FakeConnection())
        uuid = rpc.register_request(['Test'])
        self.assertEqual(len(rpc._request), 1)
        rpc.remove_request(uuid)
        self.assertEqual(len(rpc._request), 0)

    def test_rpc_remove_response(self):
        rpc = Rpc(FakeConnection())
        uuid = rpc.register_request(['Test'])
        self.assertEqual(len(rpc._response), 1)
        self.assertEqual(len(rpc._response[uuid]), 0)
        rpc.remove_response(uuid)
        self.assertEqual(len(rpc._response), 0)

    def test_rpc_remove_request_none(self):
        rpc = Rpc(FakeConnection())
        self.assertIsNone(rpc.remove_request(None))

    def test_rpc_remove_response_none(self):
        rpc = Rpc(FakeConnection())
        self.assertIsNone(rpc.remove_response(None))

    def test_rpc_get_request_not_found(self):
        rpc = Rpc(FakeConnection())
        self.assertIsNone(rpc.get_request(None))

    def test_rpc_on_frame(self):
        rpc = Rpc(FakeConnection())
        uuid = rpc.register_request(['Test'])
        self.assertEqual(rpc._response[uuid], [])
        rpc.on_frame(FakePayload(name='Test'))
        self.assertIsInstance(rpc._response[uuid][0], FakePayload)

    def test_rpc_on_multiple_frames(self):
        rpc = Rpc(FakeConnection())
        uuid = rpc.register_request(['Test'])
        self.assertEqual(rpc._response[uuid], [])
        rpc.on_frame(FakePayload(name='Test'))
        rpc.on_frame(FakePayload(name='Test'))
        rpc.on_frame(FakePayload(name='Test'))
        self.assertIsInstance(rpc._response[uuid][0], FakePayload)
        self.assertIsInstance(rpc._response[uuid][1], FakePayload)
        self.assertIsInstance(rpc._response[uuid][2], FakePayload)

    def test_rpc_raises_on_timeout(self):
        rpc = Rpc(FakeConnection(), timeout=0.1)
        uuid = rpc.register_request(['Test'])
        self.assertEqual(rpc._response[uuid], [])
        time.sleep(0.25)
        self.assertRaises(AMQPChannelError, rpc.get_request, uuid)
