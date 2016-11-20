"""AMQPStorm Channel.Queue."""

import logging

from pamqp.specification import Queue as pamqp_queue

from amqpstorm import compatibility
from amqpstorm.base import Handler
from amqpstorm.exception import AMQPInvalidArgument

LOGGER = logging.getLogger(__name__)


class Queue(Handler):
    """RabbitMQ Queue Operations."""
    __slots__ = []

    def declare(self, queue='', passive=False, durable=False,
                exclusive=False, auto_delete=False, arguments=None):
        """Declare a Queue.

        :param str queue: Queue name
        :param bool passive: Do not create
        :param bool durable: Durable queue
        :param bool exclusive: Request exclusive access
        :param bool auto_delete: Automatically delete when not in use
        :param dict arguments: Queue key/value arguments

        :raises AMQPInvalidArgument: Invalid Parameters
        :raises AMQPChannelError: Raises if the channel encountered an error.
        :raises AMQPConnectionError: Raises if the connection
                                     encountered an error.

        :rtype: dict
        """
        if not compatibility.is_string(queue):
            raise AMQPInvalidArgument('queue should be a string')
        elif not isinstance(passive, bool):
            raise AMQPInvalidArgument('passive should be a boolean')
        elif not isinstance(durable, bool):
            raise AMQPInvalidArgument('durable should be a boolean')
        elif not isinstance(exclusive, bool):
            raise AMQPInvalidArgument('exclusive should be a boolean')
        elif not isinstance(auto_delete, bool):
            raise AMQPInvalidArgument('auto_delete should be a boolean')
        elif arguments is not None and not isinstance(arguments, dict):
            raise AMQPInvalidArgument('arguments should be a dict or None')

        declare_frame = pamqp_queue.Declare(queue=queue,
                                            passive=passive,
                                            durable=durable,
                                            exclusive=exclusive,
                                            auto_delete=auto_delete,
                                            arguments=arguments)
        return self._channel.rpc_request(declare_frame)

    def delete(self, queue='', if_unused=False, if_empty=False):
        """Delete a Queue.

        :param str queue: Queue name
        :param bool if_unused: Delete only if unused
        :param bool if_empty: Delete only if empty

        :raises AMQPInvalidArgument: Invalid Parameters
        :raises AMQPChannelError: Raises if the channel encountered an error.
        :raises AMQPConnectionError: Raises if the connection
                                     encountered an error.

        :rtype: dict
        """
        if not compatibility.is_string(queue):
            raise AMQPInvalidArgument('queue should be a string')
        elif not isinstance(if_unused, bool):
            raise AMQPInvalidArgument('if_unused should be a boolean')
        elif not isinstance(if_empty, bool):
            raise AMQPInvalidArgument('if_empty should be a boolean')

        delete_frame = pamqp_queue.Delete(queue=queue, if_unused=if_unused,
                                          if_empty=if_empty)
        return self._channel.rpc_request(delete_frame)

    def purge(self, queue):
        """Purge a Queue.

        :param str queue: Queue name

        :raises AMQPInvalidArgument: Invalid Parameters
        :raises AMQPChannelError: Raises if the channel encountered an error.
        :raises AMQPConnectionError: Raises if the connection
                                     encountered an error.

        :rtype: dict
        """
        if not compatibility.is_string(queue):
            raise AMQPInvalidArgument('queue should be a string')

        purge_frame = pamqp_queue.Purge(queue=queue)

        return self._channel.rpc_request(purge_frame)

    def bind(self, queue='', exchange='', routing_key='', arguments=None):
        """Bind a Queue.

        :param str queue: Queue name
        :param str exchange: Exchange name
        :param str routing_key: The routing key to use
        :param dict arguments: Bind key/value arguments

        :raises AMQPInvalidArgument: Invalid Parameters
        :raises AMQPChannelError: Raises if the channel encountered an error.
        :raises AMQPConnectionError: Raises if the connection
                                     encountered an error.

        :rtype: dict
        """
        if not compatibility.is_string(queue):
            raise AMQPInvalidArgument('queue should be a string')
        elif not compatibility.is_string(exchange):
            raise AMQPInvalidArgument('exchange should be a string')
        elif not compatibility.is_string(routing_key):
            raise AMQPInvalidArgument('routing_key should be a string')
        elif arguments is not None and not isinstance(arguments, dict):
            raise AMQPInvalidArgument('arguments should be a dict or None')

        bind_frame = pamqp_queue.Bind(queue=queue,
                                      exchange=exchange,
                                      routing_key=routing_key,
                                      arguments=arguments)
        return self._channel.rpc_request(bind_frame)

    def unbind(self, queue='', exchange='', routing_key='', arguments=None):
        """Unbind a Queue.

        :param str queue: Queue name
        :param str exchange: Exchange name
        :param str routing_key: The routing key used
        :param dict arguments: Unbind key/value arguments

        :raises AMQPInvalidArgument: Invalid Parameters
        :raises AMQPChannelError: Raises if the channel encountered an error.
        :raises AMQPConnectionError: Raises if the connection
                                     encountered an error.

        :rtype: dict
        """
        if not compatibility.is_string(queue):
            raise AMQPInvalidArgument('queue should be a string')
        elif not compatibility.is_string(exchange):
            raise AMQPInvalidArgument('exchange should be a string')
        elif not compatibility.is_string(routing_key):
            raise AMQPInvalidArgument('routing_key should be a string')
        elif arguments is not None and not isinstance(arguments, dict):
            raise AMQPInvalidArgument('arguments should be a dict or None')

        unbind_frame = pamqp_queue.Unbind(queue=queue,
                                          exchange=exchange,
                                          routing_key=routing_key,
                                          arguments=arguments)
        return self._channel.rpc_request(unbind_frame)
