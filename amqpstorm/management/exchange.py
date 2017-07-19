from amqpstorm.compatibility import json
from amqpstorm.compatibility import quote
from amqpstorm.compatibility import urlparse
from amqpstorm.management.base import ManagementHandler

API_EXCHANGE = 'exchanges/%s/%s'
API_EXCHANGES = 'exchanges'
API_EXCHANGES_VIRTUAL_HOST = 'exchanges/%s'
API_EXCHANGE_BINDINGS = 'exchanges/%s/%s/bindings/source'
API_EXCHANGE_BIND = 'bindings/%s/e/%s/e/%s'
API_EXCHANGE_UNBIND = 'bindings/%s/e/%s/e/%s/%s'


class Exchange(ManagementHandler):
    def get(self, exchange, virtual_host='/'):
        """Get Exchange details.

        :param str exchange: Exchange name
        :param str virtual_host: Virtual host name

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: dict
        """
        virtual_host = quote(virtual_host, '')
        return self.http_client.get(
            API_EXCHANGE
            % (
                virtual_host,
                exchange)
        )

    def list(self, virtual_host='/', show_all=False):
        """List Exchanges.

        :param str virtual_host: Virtual host name
        :param bool show_all: List all Exchanges

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: list
        """
        if show_all:
            return self.http_client.get(API_EXCHANGES)
        virtual_host = quote(virtual_host, '')
        return self.http_client.get(
            API_EXCHANGES_VIRTUAL_HOST % virtual_host
        )

    def declare(self, exchange='', exchange_type='direct', virtual_host='/',
                passive=False, durable=False, auto_delete=False,
                internal=False, arguments=None):
        """Declare an Exchange.

        :param str exchange: Exchange name
        :param str exchange_type: Exchange type
        :param str virtual_host: Virtual host name
        :param bool passive: Do not create
        :param bool durable: Durable exchange
        :param bool auto_delete: Automatically delete when not in use
        :param bool internal: Is the exchange for use by the broker only.
        :param dict|None arguments: Exchange key/value arguments

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: None
        """
        virtual_host = quote(virtual_host, '')
        if passive:
            return self.get(exchange, virtual_host=virtual_host)
        exchange_payload = json.dumps(
            {
                'durable': durable,
                'auto_delete': auto_delete,
                'internal': internal,
                'type': exchange_type,
                'arguments': arguments or {},
                'vhost': urlparse.unquote(virtual_host)
            }
        )
        return self.http_client.put(API_EXCHANGE %
                                    (
                                        virtual_host,
                                        exchange
                                    ),
                                    payload=exchange_payload)

    def delete(self, exchange, virtual_host='/'):
        """Delete an Exchange.

        :param str exchange: Exchange name
        :param str virtual_host: Virtual host name

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: dict
        """
        virtual_host = quote(virtual_host, '')
        return self.http_client.delete(API_EXCHANGE %
                                       (
                                           virtual_host,
                                           exchange
                                       ))

    def bindings(self, exchange, virtual_host='/'):
        """Get Exchange bindings.

        :param str exchange: Exchange name
        :param str virtual_host: Virtual host name

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: list
        """
        virtual_host = quote(virtual_host, '')
        return self.http_client.get(API_EXCHANGE_BINDINGS %
                                    (
                                        virtual_host,
                                        exchange
                                    ))

    def bind(self, destination='', source='', routing_key='', virtual_host='/',
             arguments=None):
        """Bind an Exchange.

        :param str source: Source Exchange name
        :param str destination: Destination Exchange name
        :param str routing_key: The routing key to use
        :param str virtual_host: Virtual host name
        :param dict|None arguments: Bind key/value arguments

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: None
        """
        bind_payload = json.dumps({
            'destination': destination,
            'destination_type': 'e',
            'routing_key': routing_key,
            'source': source,
            'arguments': arguments or {},
            'vhost': virtual_host
        })
        virtual_host = quote(virtual_host, '')
        return self.http_client.post(API_EXCHANGE_BIND %
                                     (
                                         virtual_host,
                                         source,
                                         destination
                                     ),
                                     payload=bind_payload)

    def unbind(self, destination='', source='', routing_key='',
               virtual_host='/', properties_key=None):
        """Unbind an Exchange.

        :param str source: Source Exchange name
        :param str destination: Destination Exchange name
        :param str routing_key: The routing key to use
        :param str virtual_host: Virtual host name
        :param str properties_key:

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: None
        """
        unbind_payload = json.dumps({
            'destination': destination,
            'destination_type': 'e',
            'properties_key': properties_key or routing_key,
            'source': source,
            'vhost': virtual_host
        })
        virtual_host = quote(virtual_host, '')
        return self.http_client.delete(API_EXCHANGE_UNBIND %
                                       (
                                           virtual_host,
                                           source,
                                           destination,
                                           properties_key or routing_key
                                       ),
                                       payload=unbind_payload)
