from amqpstorm.compatibility import json
from amqpstorm.compatibility import quote
from amqpstorm.management.base import ManagementHandler

API_CONNECTION = 'connections/%s'
API_CONNECTIONS = 'connections'


class Connection(ManagementHandler):
    def get(self, connection):
        """Get Connection details.

        :param str connection: Connection name

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: dict
        """
        return self.http_client.get(API_CONNECTION % connection)

    def list(self):
        """Get Connections.

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: list
        """
        return self.http_client.get(API_CONNECTIONS)

    def close(self, connection, reason='Closed via management api'):
        """Close Connection.

        :param str connection: Connection name
        :param str reason: Reason for closing connection.

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: None
        """

        close_payload = json.dumps({
            'name': connection,
            'reason': reason
        })
        connection = quote(connection, '')
        return self.http_client.delete(API_CONNECTION % connection,
                                       payload=close_payload,
                                       headers={
                                           'X-Reason': reason
                                       })
