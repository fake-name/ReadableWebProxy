"""AMQPStorm Channel.Tx."""

import logging

from pamqp import specification

from amqpstorm.base import Handler

LOGGER = logging.getLogger(__name__)


class Tx(Handler):
    """RabbitMQ Transactions.

        Server local transactions, in which the server will buffer published
        messages until the client commits (or rollback) the messages.

    """
    __slots__ = ['_tx_active']

    def __init__(self, channel):
        self._tx_active = True
        super(Tx, self).__init__(channel)

    def __enter__(self):
        self.select()
        return self

    def __exit__(self, exception_type, exception_value, _):
        if exception_type:
            LOGGER.warning(
                'Leaving Transaction on exception: %s',
                exception_value
            )
            if self._tx_active:
                self.rollback()
            return
        if self._tx_active:
            self.commit()

    def select(self):
        """Enable standard transaction mode.

            This will enable transaction mode on the channel. Meaning that
            messages will be kept in the remote server buffer until such a
            time that either commit or rollback is called.

        :return:
        """
        self._tx_active = True
        return self._channel.rpc_request(specification.Tx.Select())

    def commit(self):
        """Commit the current transaction.

            Commit all messages published during the current transaction
            session to the remote server.

            A new transaction session starts as soon as the command has
            been executed.

        :return:
        """
        self._tx_active = False
        return self._channel.rpc_request(specification.Tx.Commit())

    def rollback(self):
        """Abandon the current transaction.

            Rollback all messages published during the current transaction
            session to the remote server.

            Note that all messages published during this transaction session
            will be lost, and will have to be published again.

            A new transaction session starts as soon as the command has
            been executed.

        :return:
        """
        self._tx_active = False
        return self._channel.rpc_request(specification.Tx.Rollback())
