from amqpstorm.management.base import ManagementHandler

API_CHANNEL = 'channels/%s'
API_CHANNELS = 'channels'


class Channel(ManagementHandler):
    def get(self, channel):
        """Get Connection details.

        :param channel: Channel name

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: dict
        """
        return self.http_client.get(API_CHANNEL % channel)

    def list(self):
        """List all Channels.

        :raises ApiError: Raises if the remote server encountered an error.
        :raises ApiConnectionError: Raises if there was a connectivity issue.

        :rtype: list
        """
        return self.http_client.get(API_CHANNELS)
