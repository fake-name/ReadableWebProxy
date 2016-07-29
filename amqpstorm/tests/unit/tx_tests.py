import logging

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from pamqp import specification as pamqp_spec

from amqpstorm.tx import Tx
from amqpstorm.channel import Channel

from amqpstorm.tests.utility import FakeConnection
from amqpstorm.tests.utility import MockLoggingHandler

logging.basicConfig(level=logging.DEBUG)


class TxTests(unittest.TestCase):
    def setUp(self):
        self.logging_handler = MockLoggingHandler()
        logging.root.addHandler(self.logging_handler)

    def test_tx_select(self):
        def on_tx_select(*_):
            channel.rpc.on_frame(pamqp_spec.Tx.SelectOk())

        connection = FakeConnection(on_write=on_tx_select)
        channel = Channel(0, connection, 0.1)
        channel.set_state(Channel.OPEN)
        tx = Tx(channel)

        self.assertIsInstance(tx.select(), dict)
        self.assertTrue(tx._tx_active)

    def test_tx_commit(self):
        def on_tx_commit(*_):
            channel.rpc.on_frame(pamqp_spec.Tx.CommitOk())

        connection = FakeConnection(on_write=on_tx_commit)
        channel = Channel(0, connection, 0.1)
        channel.set_state(Channel.OPEN)
        tx = Tx(channel)

        self.assertIsInstance(tx.commit(), dict)
        self.assertFalse(tx._tx_active)

    def test_tx_rollback(self):
        def on_tx_rollback(*_):
            channel.rpc.on_frame(pamqp_spec.Tx.RollbackOk())

        connection = FakeConnection(on_write=on_tx_rollback)
        channel = Channel(0, connection, 0.1)
        channel.set_state(Channel.OPEN)
        tx = Tx(channel)

        self.assertIsInstance(tx.rollback(), dict)
        self.assertFalse(tx._tx_active)

    def test_tx_with_statement(self):
        self._active_transaction = False

        def on_tx(*_):
            if not self._active_transaction:
                channel.rpc.on_frame(pamqp_spec.Tx.SelectOk())
                self._active_transaction = True
                return
            self._active_transaction = False
            channel.rpc.on_frame(pamqp_spec.Tx.CommitOk())

        connection = FakeConnection(on_write=on_tx)
        channel = Channel(0, connection, 0.1)
        channel.set_state(Channel.OPEN)
        tx = Tx(channel)

        with tx:
            self.assertTrue(tx._tx_active)
        self.assertFalse(tx._tx_active)

    def test_tx_with_statement_when_failing(self):
        self._active_transaction = False

        def on_tx(*_):
            if not self._active_transaction:
                channel.rpc.on_frame(pamqp_spec.Tx.SelectOk())
                self._active_transaction = True
                return
            self._active_transaction = False
            channel.rpc.on_frame(pamqp_spec.Tx.RollbackOk())

        connection = FakeConnection(on_write=on_tx)
        channel = Channel(0, connection, 0.1)
        channel.set_state(Channel.OPEN)
        tx = Tx(channel)

        try:
            with tx:
                self.assertTrue(tx._tx_active)
                raise Exception('error')
        except Exception as why:
            self.assertEqual('error', str(why))

        self.assertFalse(tx._tx_active)
        self.assertEqual(self.logging_handler.messages['warning'][0],
                         'Leaving Transaction on exception: error')
