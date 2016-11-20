"""AMQPStorm Channel.Exchange."""

import logging

from pamqp.specification import Exchange as pamqp_exchange

from amqpstorm import compatibility
from amqpstorm.base import Handler
from amqpstorm.exception import AMQPInvalidArgument

LOGGER = logging.getLogger(__name__)


class Exchange(Handler):
    """RabbitMQ Exchange Operations."""
    __slots__ = []

    def declare(self, exchange='', exchange_type='direct', passive=False,
                durable=False, auto_delete=False, arguments=None):
        """Declare an Exchange.

        :param str exchange: Exchange name
        :param str exchange_type: Exchange type
        :param bool passive: Do not create
        :param bool durable: Durable exchange
        :param bool auto_delete: Automatically delete when not in use
        :param dict arguments: Exchange key/value arguments

        :raises AMQPInvalidArgument: Invalid Parameters
        :raises AMQPChannelError: Raises if the channel encountered an error.
        :raises AMQPConnectionError: Raises if the connection
                                     encountered an error.

        :rtype: dict
        """
        if not compatibility.is_string(exchange):
            raise AMQPInvalidArgument('exchange should be a string')
        elif not compatibility.is_string(exchange_type):
            raise AMQPInvalidArgument('exchange_type should be a string')
        elif not isinstance(passive, bool):
            raise AMQPInvalidArgument('passive should be a boolean')
        elif not isinstance(durable, bool):
            raise AMQPInvalidArgument('durable should be a boolean')
        elif not isinstance(auto_delete, bool):
            raise AMQPInvalidArgument('auto_delete should be a boolean')
        elif arguments is not None and not isinstance(arguments, dict):
            raise AMQPInvalidArgument('arguments should be a dict or None')

        declare_frame = pamqp_exchange.Declare(exchange=exchange,
                                               exchange_type=exchange_type,
                                               passive=passive,
                                               durable=durable,
                                               auto_delete=auto_delete,
                                               arguments=arguments)
        return self._channel.rpc_request(declare_frame)

    def delete(self, exchange='', if_unused=False):
        """Delete an Exchange.

        :param str exchange: Exchange name
        :param bool if_unused: Delete only if unused

        :raises AMQPInvalidArgument: Invalid Parameters
        :raises AMQPChannelError: Raises if the channel encountered an error.
        :raises AMQPConnectionError: Raises if the connection
                                     encountered an error.

        :rtype: dict
        """
        if not compatibility.is_string(exchange):
            raise AMQPInvalidArgument('exchange should be a string')

        delete_frame = pamqp_exchange.Delete(exchange=exchange,
                                             if_unused=if_unused)
        return self._channel.rpc_request(delete_frame)

    def bind(self, destination='', source='', routing_key='',
             arguments=None):
        """Bind an Exchange.

        :param str destination: Exchange name
        :param str source: Exchange to bind to
        :param str routing_key: The routing key to use
        :param dict arguments: Bind key/value arguments

        :raises AMQPInvalidArgument: Invalid Parameters
        :raises AMQPChannelError: Raises if the channel encountered an error.
        :raises AMQPConnectionError: Raises if the connection
                                     encountered an error.

        :rtype: dict
        """
        if not compatibility.is_string(destination):
            raise AMQPInvalidArgument('destination should be a string')
        elif not compatibility.is_string(source):
            raise AMQPInvalidArgument('source should be a string')
        elif not compatibility.is_string(routing_key):
            raise AMQPInvalidArgument('routing_key should be a string')
        elif arguments is not None and not isinstance(arguments, dict):
            raise AMQPInvalidArgument('arguments should be a dict or None')

        bind_frame = pamqp_exchange.Bind(destination=destination,
                                         source=source,
                                         routing_key=routing_key,
                                         arguments=arguments)
        return self._channel.rpc_request(bind_frame)

    def unbind(self, destination='', source='', routing_key='',
               arguments=None):
        """Unbind an Exchange.

        :param str destination: Exchange name
        :param str source: Exchange to unbind from
        :param str routing_key: The routing key used
        :param dict arguments: Unbind key/value arguments

        :raises AMQPInvalidArgument: Invalid Parameters
        :raises AMQPChannelError: Raises if the channel encountered an error.
        :raises AMQPConnectionError: Raises if the connection
                                     encountered an error.

        :rtype: dict
        """
        if not compatibility.is_string(destination):
            raise AMQPInvalidArgument('destination should be a string')
        elif not compatibility.is_string(source):
            raise AMQPInvalidArgument('source should be a string')
        elif not compatibility.is_string(routing_key):
            raise AMQPInvalidArgument('routing_key should be a string')
        elif arguments is not None and not isinstance(arguments, dict):
            raise AMQPInvalidArgument('arguments should be a dict or None')

        unbind_frame = pamqp_exchange.Unbind(destination=destination,
                                             source=source,
                                             routing_key=routing_key,
                                             arguments=arguments)
        return self._channel.rpc_request(unbind_frame)
