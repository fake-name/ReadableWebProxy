"""AMQP-Storm."""
__version__ = '1.5.0'  # noqa
__author__ = 'eandersson'  # noqa

import logging


class NullHandler(logging.Handler):
    """Logging Null Handler."""

    def emit(self, record):
        pass


logging.getLogger('amqpstorm').addHandler(NullHandler())

from amqpstorm.channel import Channel  # noqa
from amqpstorm.connection import Connection  # noqa
from amqpstorm.uri_connection import UriConnection  # noqa
from amqpstorm.message import Message  # noqa
from amqpstorm.exception import AMQPError  # noqa
from amqpstorm.exception import AMQPChannelError  # noqa
from amqpstorm.exception import AMQPMessageError  # noga
from amqpstorm.exception import AMQPConnectionError  # noqa
from amqpstorm.exception import AMQPInvalidArgument  # noqa
