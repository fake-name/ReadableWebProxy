from amqpstorm.compatibility import quote
from amqpstorm.management.basic import Basic
from amqpstorm.management.channel import Channel
from amqpstorm.management.connection import Connection
from amqpstorm.management.exchange import Exchange
from amqpstorm.management.http_client import HTTPClient
from amqpstorm.management.queue import Queue
from amqpstorm.management.user import User
from amqpstorm.management.virtual_host import VirtualHost

API_ALIVENESS_TEST = 'aliveness-test/%s'
API_NODES = 'nodes'
API_OVERVIEW = 'overview'
API_WHOAMI = 'whoami'
API_TOP = 'top/%s'


class ManagementApi(object):
    def __init__(self, api_url, username, password, timeout=10):
        self.http_client = HTTPClient(api_url, username, password,
                                      timeout=timeout)
        self._basic = Basic(self.http_client)
        self._channel = Channel(self.http_client)
        self._connection = Connection(self.http_client)
        self._exchange = Exchange(self.http_client)
        self._queue = Queue(self.http_client)
        self._user = User(self.http_client)
        self._virtual_host = VirtualHost(self.http_client)

    @property
    def basic(self):
        """RabbitMQ Basic Operations.

        :rtype: amqpstorm.management.basic.Basic
        """
        return self._basic

    @property
    def channel(self):
        """RabbitMQ Channel Operations.

        :rtype: amqpstorm.management.channel.Channel
        """
        return self._channel

    @property
    def connection(self):
        """RabbitMQ Connection Operations.

        :rtype: amqpstorm.management.connection.Connection
        """
        return self._connection

    @property
    def exchange(self):
        """RabbitMQ Exchange Operations.

        :rtype: amqpstorm.management.exchange.Exchange
        """
        return self._exchange

    @property
    def queue(self):
        """RabbitMQ Queue Operations.

        :rtype: amqpstorm.management.queue.Queue
        """
        return self._queue

    @property
    def user(self):
        """RabbitMQ User Operations.

        :rtype: amqpstorm.management.user.User
        """
        return self._user

    @property
    def virtual_host(self):
        """RabbitMQ VirtualHost Operations.

        :rtype: amqpstorm.management.virtual_host.VirtualHost
        """
        return self._virtual_host

    def aliveness_test(self, virtual_host='/'):
        """Aliveness Test.

        :param str virtual_host: Virtual host name

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: dict
        """
        virtual_host = quote(virtual_host, '')
        return self.http_client.get(API_ALIVENESS_TEST %
                                    virtual_host)

    def overview(self):
        """Get Overview.

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: dict
        """
        return self.http_client.get(API_OVERVIEW)

    def nodes(self):
        """Get Nodes.

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: dict
        """
        return self.http_client.get(API_NODES)

    def top(self):
        """Top Processes.

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: list
        """
        nodes = []
        for node in self.nodes():
            nodes.append(self.http_client.get(API_TOP % node['name']))
        return nodes

    def whoami(self):
        """Who am I?

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: dict
        """
        return self.http_client.get(API_WHOAMI)
