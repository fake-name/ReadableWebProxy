"""AMQPStorm Base."""

import locale
import threading

from amqpstorm.compatibility import is_string
from amqpstorm.exception import AMQPChannelError

AUTH_MECHANISM = 'PLAIN'
IDLE_WAIT = 0.01
FRAME_MAX = 131072
MAX_CHANNELS = 65535
LOCALE = locale.getdefaultlocale()[0] or 'en_US'


class Stateful(object):
    """Stateful implementation."""
    CLOSED = 0
    CLOSING = 1
    OPENING = 2
    OPEN = 3

    def __init__(self):
        self._lock = threading.Lock()
        self._state = self.CLOSED
        self._exceptions = []

    @property
    def lock(self):
        """Threading lock.

        :return:
        """
        return self._lock

    def set_state(self, state):
        """Set State.

        :param int state:
        :return:
        """
        self._state = state

    @property
    def current_state(self):
        """Get the State.

        :rtype: int
        """
        return self._state

    @property
    def is_closed(self):
        """Is Closed?

        :rtype: bool
        """
        return self._state == self.CLOSED

    @property
    def is_closing(self):
        """Is Closing?

        :rtype: bool
        """
        return self._state == self.CLOSING

    @property
    def is_opening(self):
        """Is Opening?

        :rtype: bool
        """
        return self._state == self.OPENING

    @property
    def is_open(self):
        """Is Open?

        :rtype: bool
        """
        return self._state == self.OPEN

    @property
    def exceptions(self):
        """Stores all exceptions thrown by this instance.

            This is useful for troubleshooting, and is used internally
            to check the health of the connection.

        :rtype: list
        """
        return self._exceptions


class BaseChannel(Stateful):
    """Channel base class."""
    __slots__ = [
        '_channel_id', '_consumer_tags'
    ]

    def __init__(self, channel_id):
        super(BaseChannel, self).__init__()
        self._consumer_tags = []
        self._channel_id = channel_id

    @property
    def channel_id(self):
        """Get Channel id.

        :rtype: int
        """
        return self._channel_id

    @property
    def consumer_tags(self):
        """Get a list of consumer tags.

        :rtype: list
        """
        return self._consumer_tags

    def add_consumer_tag(self, tag):
        """Add a Consumer tag.

        :param str tag: Consumer tag.
        :return:
        """
        if not is_string(tag):
            raise AMQPChannelError('consumer tag needs to be a string')
        if tag not in self._consumer_tags:
            self._consumer_tags.append(tag)

    def remove_consumer_tag(self, tag=None):
        """Remove a Consumer tag.

            If no tag is specified, all all tags will be removed.

        :param str|None tag: Consumer tag.
        :return:
        """
        if tag is not None:
            if tag in self._consumer_tags:
                self._consumer_tags.remove(tag)
        else:
            self._consumer_tags = []


class BaseMessage(object):
    """Message base class."""
    __slots__ = [
        '_body', '_channel', '_method', '_properties'
    ]

    def __init__(self, channel, **message):
        """
        :param Channel channel: AMQPStorm Channel
        :param str|unicode body: Message body
        :param dict method: Message method
        :param dict properties: Message properties
        """
        self._channel = channel
        self._body = message.get('body', None)
        self._method = message.get('method', None)
        self._properties = message.get('properties', {'headers': {}})

    def __iter__(self):
        for attribute in ['_body', '_channel', '_method', '_properties']:
            yield (attribute[1::], getattr(self, attribute))

    def to_dict(self):
        """Message to Dictionary.

        :rtype: dict
        """
        return {
            'body': self._body,
            'method': self._method,
            'properties': self._properties,
            'channel': self._channel
        }

    def to_tuple(self):
        """Message to Tuple.

        :rtype: tuple
        """
        return self._body, self._channel, self._method, self._properties


class Handler(object):
    """Operations Handler (e.g. Queue, Exchange)"""
    __slots__ = [
        '_channel'
    ]

    def __init__(self, channel):
        self._channel = channel
