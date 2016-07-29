import logging
import socket
import ssl
import threading

from mock import MagicMock

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from amqpstorm.io import IO
from amqpstorm import Connection
from amqpstorm.exception import *

from pamqp.specification import Basic as spec_basic
from pamqp import specification as pamqp_spec
from pamqp import frame as pamqp_frame

from amqpstorm.tests.utility import FakeChannel
from amqpstorm.tests.utility import MockLoggingHandler

logging.basicConfig(level=logging.DEBUG)


class ConnectionTests(unittest.TestCase):
    def setUp(self):
        self.logging_handler = MockLoggingHandler()
        logging.root.addHandler(self.logging_handler)

    def test_connection_with_statement(self):
        with Connection('127.0.0.1', 'guest', 'guest', lazy=True) as con:
            self.assertIsInstance(con, Connection)

    def test_connection_with_statement_when_failing(self):
        try:
            with Connection('127.0.0.1', 'guest', 'guest', lazy=True) as con:
                con.exceptions.append(AMQPConnectionError('error'))
                con.check_for_errors()
        except AMQPConnectionError as why:
            self.assertIsInstance(why, AMQPConnectionError)

        self.assertEqual(self.logging_handler.messages['warning'][0],
                         'Closing connection due to an unhandled exception: '
                         'error')

    def test_connection_server_is_blocked_default_value(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', lazy=True)

        self.assertEqual(connection.is_blocked, False)

    def test_connection_server_properties_default_value(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', lazy=True)

        self.assertEqual(connection.server_properties, {})

    def test_connection_socket_property(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', lazy=True)
        connection._io.socket = 'FakeSocket'
        self.assertEqual(connection.socket, 'FakeSocket')

    def test_connection_socket_none_when_closed(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', lazy=True)

        self.assertFalse(connection.socket)

    def test_connection_fileno_property(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', lazy=True)
        connection.set_state(connection.OPENING)
        io = IO(connection.parameters, [])
        io.socket = MagicMock(name='socket', spec=socket.socket)
        connection._io = io
        io.socket.fileno.return_value = 5

        self.assertEqual(connection.fileno, 5)

    def test_connection_fileno_none_when_closed(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', lazy=True)

        self.assertIsNone(connection.fileno)

    def test_connection_close_state(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', lazy=True)
        connection.set_state(Connection.OPEN)
        connection.close()

        self.assertTrue(connection.is_closed)

    def test_connection_open_channel_on_closed_connection(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', lazy=True)

        self.assertRaises(AMQPConnectionError, connection.channel)

    def test_connection_basic_read_buffer(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', lazy=True)
        cancel_ok_frame = spec_basic.CancelOk().marshal()

        self.assertEqual(connection._read_buffer(cancel_ok_frame), b'\x00')

    def test_connection_handle_read_buffer_none_returns_none(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', lazy=True)

        self.assertIsNone(connection._read_buffer(None))

    def test_connection_basic_handle_amqp_frame(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', lazy=True)
        cancel_ok_frame = spec_basic.CancelOk().marshal()

        self.assertEqual(connection._handle_amqp_frame(cancel_ok_frame),
                         (b'\x00', None, None))

    def test_connection_handle_amqp_frame_none_returns_none(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', lazy=True)
        result = connection._handle_amqp_frame('')

        self.assertEqual(result[0], '')
        self.assertIsNone(result[1])
        self.assertIsNone(result[2])

    def test_connection_handle_amqp_frame_error(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', lazy=True)

        def throw_error(*_):
            raise pamqp_spec.AMQPFrameError()

        restore_func = pamqp_frame.unmarshal
        try:
            pamqp_frame.unmarshal = throw_error

            result = connection._handle_amqp_frame('error')

            self.assertEqual(result[0], 'error')
            self.assertIsNone(result[1])
            self.assertIsNone(result[2])
        finally:
            pamqp_frame.unmarshal = restore_func

    def test_connection_handle_unicode_error(self):
        """This test covers an unlikely issue triggered by network corruption.

            pamqp.decode._maybe_utf8 raises:
                UnicodeDecodeError: 'utf8' codec can't
                decode byte 0xc5 in position 1: invalid continuation byte

            The goal here is not to fix issues caused by network corruption,
            but rather to make sure that the exceptions raised when
            connections do fail are always predictable.

            Fail fast and reliably!

        :return:
        """
        connection = Connection('127.0.0.1', 'guest', 'guest', lazy=True)

        def throw_error(_):
            raise UnicodeDecodeError(str(), bytes(), 1, 1, str())

        restore_func = pamqp_frame.unmarshal
        try:
            pamqp_frame.unmarshal = throw_error

            result = connection._handle_amqp_frame('error')

            self.assertEqual(result[0], 'error')
            self.assertIsNone(result[1])
            self.assertIsNone(result[2])
        finally:
            pamqp_frame.unmarshal = restore_func

    def test_connection_handle_value_error(self):
        """This test covers an unlikely issue triggered by network corruption.

            pamqp.decode._embedded_value raises:
                ValueError: Unknown type: b'\x13'

            The goal here is not to fix issues caused by network corruption,
            but rather to make sure that the exceptions raised when
            connections do fail are always predictable.

            Fail fast and reliably!

        :return:
        """
        connection = Connection('127.0.0.1', 'guest', 'guest', lazy=True)

        def throw_error(_):
            raise ValueError("Unknown type: b'\x13'")

        restore_func = pamqp_frame.unmarshal
        try:
            pamqp_frame.unmarshal = throw_error

            result = connection._handle_amqp_frame('error')

            self.assertEqual(result[0], 'error')
            self.assertIsNone(result[1])
            self.assertIsNone(result[2])
        finally:
            pamqp_frame.unmarshal = restore_func

    def test_connection_wait_for_connection(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', timeout=5,
                                lazy=True)
        connection.set_state(connection.OPENING)
        io = IO(connection.parameters, [])
        io.socket = MagicMock(name='socket', spec=socket.socket)
        connection._io = io

        self.assertFalse(connection.is_open)

        def func(conn):
            conn.set_state(conn.OPEN)

        threading.Timer(function=func, interval=1, args=(connection,)).start()
        connection._wait_for_connection_to_open()

        self.assertTrue(connection.is_open)

    def test_connection_wait_for_connection_raises_on_timeout(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', timeout=0.1,
                                lazy=True)
        connection.set_state(connection.OPENING)
        io = IO(connection.parameters, [])
        io.socket = MagicMock(name='socket', spec=socket.socket)
        connection._io = io

        self.assertRaises(AMQPConnectionError,
                          connection._wait_for_connection_to_open)

    def test_connection_close_channels(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', timeout=1,
                                lazy=True)
        connection._channels[0] = FakeChannel()
        connection._channels[1] = FakeChannel()
        connection._channels[2] = FakeChannel(FakeChannel.CLOSED)

        self.assertTrue(connection._channels[0].is_open)
        self.assertTrue(connection._channels[1].is_open)
        self.assertTrue(connection._channels[2].is_closed)

        connection._close_channels()

        self.assertTrue(connection._channels[0].is_closed)
        self.assertTrue(connection._channels[1].is_closed)
        self.assertTrue(connection._channels[2].is_closed)

    def test_connection_closed_on_exception(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', timeout=1,
                                lazy=True)
        connection.set_state(connection.OPEN)
        connection.exceptions.append(AMQPConnectionError('error'))

        self.assertTrue(connection.is_open)
        self.assertRaises(AMQPConnectionError, connection.check_for_errors)
        self.assertTrue(connection.is_closed)

    def test_connection_heartbeat_stopped_on_close(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', timeout=1,
                                lazy=True)
        connection.set_state(connection.OPEN)
        connection.heartbeat.start(connection.exceptions)
        connection.exceptions.append(AMQPConnectionError('error'))

        self.assertTrue(connection.heartbeat._running.is_set())

        self.assertRaises(AMQPConnectionError, connection.check_for_errors)

        self.assertFalse(connection.heartbeat._running.is_set())


class ConnectionParameterTests(unittest.TestCase):
    def test_connection_set_hostname(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', lazy=True)

        self.assertEqual(connection.parameters['username'], 'guest')

    def test_connection_set_username(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', lazy=True)

        self.assertEqual(connection.parameters['username'], 'guest')

    def test_connection_set_password(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', lazy=True)

        self.assertEqual(connection.parameters['username'], 'guest')

    def test_connection_set_parameters(self):
        connection = Connection('127.0.0.1', 'guest', 'guest',
                                virtual_host='travis',
                                heartbeat=120,
                                timeout=180,
                                ssl=True,
                                ssl_options={
                                    'ssl_version': ssl.PROTOCOL_TLSv1
                                },
                                lazy=True)

        self.assertEqual(connection.parameters['virtual_host'], 'travis')
        self.assertEqual(connection.parameters['heartbeat'], 120)
        self.assertEqual(connection.parameters['timeout'], 180)
        self.assertEqual(connection.parameters['ssl'], True)
        self.assertEqual(connection.parameters['ssl_options']['ssl_version'],
                         ssl.PROTOCOL_TLSv1)

    def test_connection_invalid_hostname(self):
        self.assertRaises(AMQPInvalidArgument, Connection, 1,
                          'guest', 'guest', lazy=True)

    def test_connection_invalid_username(self):
        self.assertRaises(AMQPInvalidArgument, Connection, '127.0.0.1',
                          2, 'guest', lazy=True)
        self.assertRaises(AMQPInvalidArgument, Connection, '127.0.0.1',
                          None, 'guest', lazy=True)

    def test_connection_invalid_password(self):
        self.assertRaises(AMQPInvalidArgument, Connection, '127.0.0.1',
                          'guest', 3, lazy=True)
        self.assertRaises(AMQPInvalidArgument, Connection, '127.0.0.1',
                          'guest', None, lazy=True)

    def test_connection_invalid_virtual_host(self):
        self.assertRaises(AMQPInvalidArgument, Connection, '127.0.0.1',
                          'guest', 'guest', virtual_host=4, lazy=True)
        self.assertRaises(AMQPInvalidArgument, Connection, '127.0.0.1',
                          'guest', 'guest', virtual_host=None, lazy=True)

    def test_connection_invalid_port(self):
        self.assertRaises(AMQPInvalidArgument, Connection, '127.0.0.1',
                          'guest', 'guest', port='', lazy=True)
        self.assertRaises(AMQPInvalidArgument, Connection, '127.0.0.1',
                          'guest', 'guest', port=None, lazy=True)

    def test_connection_invalid_heartbeat(self):
        self.assertRaises(AMQPInvalidArgument, Connection, '127.0.0.1',
                          'guest', 'guest', heartbeat='5', lazy=True)
        self.assertRaises(AMQPInvalidArgument, Connection, '127.0.0.1',
                          'guest', 'guest', heartbeat=None, lazy=True)

    def test_connection_invalid_timeout(self):
        self.assertRaises(AMQPInvalidArgument, Connection, '127.0.0.1',
                          'guest', 'guest', timeout='6', lazy=True)
        self.assertRaises(AMQPInvalidArgument, Connection, '127.0.0.1',
                          'guest', 'guest', timeout=None, lazy=True)

    def test_connection_invalid_timeout_on_channel(self):
        connection = Connection('127.0.0.1', 'guest', 'guest', timeout=1,
                                lazy=True)

        self.assertRaisesRegexp(AMQPInvalidArgument,
                                'rpc_timeout should be an integer',
                                connection.channel, None)
