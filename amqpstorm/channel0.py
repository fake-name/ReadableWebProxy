"""AMQP-Storm Connection.Channel0."""

import logging
import platform

from pamqp import specification as pamqp_spec
from pamqp.heartbeat import Heartbeat
from pamqp.specification import Connection as pamqp_connection

from amqpstorm import __version__
from amqpstorm.base import AUTH_MECHANISM
from amqpstorm.base import FRAME_MAX
from amqpstorm.base import LOCALE
from amqpstorm.base import MAX_CHANNELS
from amqpstorm.base import Stateful
from amqpstorm.compatibility import try_utf8_decode
from amqpstorm.exception import AMQPConnectionError

LOGGER = logging.getLogger(__name__)


class Channel0(object):
    """AMQP Connection.Channel0"""

    def __init__(self, connection):
        super(Channel0, self).__init__()
        self.is_blocked = False
        self.server_properties = {}
        self.parameters = connection.parameters
        self._connection = connection
        self._heartbeat = self.parameters['heartbeat']

    def on_frame(self, frame_in):
        """Handle frames sent to Channel0.

        :param frame_in: Amqp frame.
        :return:
        """
        LOGGER.debug('Frame Received: %s', frame_in.name)
        if frame_in.name == 'Heartbeat':
            return
        elif frame_in.name == 'Connection.Close':
            self._close_connection(frame_in)
        elif frame_in.name == 'Connection.CloseOk':
            self._close_connection_ok()
        elif frame_in.name == 'Connection.Blocked':
            self._blocked_connection(frame_in)
        elif frame_in.name == 'Connection.Unblocked':
            self._unblocked_connection()
        elif frame_in.name == 'Connection.OpenOk':
            self._set_connection_state(Stateful.OPEN)
        elif frame_in.name == 'Connection.Start':
            self.server_properties = frame_in.server_properties
            self._send_start_ok_frame(frame_in)
        elif frame_in.name == 'Connection.Tune':
            self._send_tune_ok_frame()
            self._send_open_connection()
        else:
            LOGGER.error('[Channel0] Unhandled Frame: %s', frame_in.name)

    def send_close_connection_frame(self):
        """Send Connection Close frame.

        :return:
        """
        self._write_frame(pamqp_spec.Connection.Close())

    def send_heartbeat(self):
        """Send Heartbeat frame.

        :return:
        """
        self._write_frame(Heartbeat())

    def _close_connection(self, frame_in):
        """Connection Close.

        :param pamqp_spec.Connection.Close frame_in: Amqp frame.
        :return:
        """
        self._set_connection_state(Stateful.CLOSED)
        if frame_in.reply_code != 200:
            reply_text = try_utf8_decode(frame_in.reply_text)
            message = ('Connection was closed by remote server: %s'
                       % reply_text)
            exception = AMQPConnectionError(message,
                                            reply_code=frame_in.reply_code)
            self._connection.exceptions.append(exception)

    def _close_connection_ok(self):
        """Connection CloseOk frame received.

        :return:
        """
        self._set_connection_state(Stateful.CLOSED)

    def _blocked_connection(self, frame_in):
        """Connection is Blocked.

        :param frame_in:
        :return:
        """
        self.is_blocked = True
        LOGGER.warning('Connection is blocked by remote server: %s',
                       try_utf8_decode(frame_in.reason))

    def _unblocked_connection(self):
        """Connection is Unblocked.

        :return:
        """
        self.is_blocked = False
        LOGGER.info('Connection is no longer blocked by remote server')

    def _plain_credentials(self):
        """AMQP Plain Credentials.

        :rtype: str
        """
        return '\0%s\0%s' % (self.parameters['username'],
                             self.parameters['password'])

    def _send_start_ok_frame(self, frame_in):
        """Send Start OK frame.

        :param pamqp_spec.Connection.StartOk frame_in: Amqp frame.
        :return:
        """
        if 'PLAIN' not in try_utf8_decode(frame_in.mechanisms):
            exception = AMQPConnectionError('Unsupported Security Mechanism(s)'
                                            ': %s' % frame_in.mechanisms)
            self._connection.exceptions.append(exception)
            return
        credentials = self._plain_credentials()
        start_ok_frame = pamqp_connection.StartOk(
            mechanism=AUTH_MECHANISM,
            client_properties=self._client_properties(),
            response=credentials,
            locale=LOCALE)
        self._write_frame(start_ok_frame)

    def _send_tune_ok_frame(self):
        """Send Tune OK frame.

        :return:
        """
        tune_ok_frame = pamqp_connection.TuneOk(channel_max=MAX_CHANNELS,
                                                frame_max=FRAME_MAX,
                                                heartbeat=self._heartbeat)
        self._write_frame(tune_ok_frame)

    def _send_open_connection(self):
        """Send Open Connection frame.

        :return:
        """
        open_frame = pamqp_connection.Open(
            virtual_host=self.parameters['virtual_host']
        )
        self._write_frame(open_frame)

    def _set_connection_state(self, state):
        """Set Connection state.

        :param state:
        :return:
        """
        self._connection.set_state(state)

    def _write_frame(self, frame_out):
        """Write a pamqp frame from Channel0.

        :param frame_out: Amqp frame.
        :return:
        """
        self._connection.write_frame(0, frame_out)
        LOGGER.debug('Frame Sent: %s', frame_out.name)

    @staticmethod
    def _client_properties():
        """AMQPStorm Client Properties.

        :rtype: dict
        """
        return {
            'product': 'AMQP-Storm',
            'platform': 'Python %s (%s)' % (platform.python_version(),
                                            platform.python_implementation()),
            'capabilities': {
                'basic.nack': True,
                'connection.blocked': True,
                'publisher_confirms': True,
                'consumer_cancel_notify': True,
                'authentication_failure_close': True,
            },
            'information': 'See https://github.com/eandersson/amqpstorm',
            'version': __version__
        }
