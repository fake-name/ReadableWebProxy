"""AMQPStorm Connection.IO."""

import logging
import select
import socket
import threading
from errno import EAGAIN
from errno import EINTR
from errno import EWOULDBLOCK
from time import sleep

from amqpstorm import compatibility
from amqpstorm.base import FRAME_MAX
from amqpstorm.base import IDLE_WAIT
from amqpstorm.compatibility import ssl
from amqpstorm.exception import AMQPConnectionError

EMPTY_BUFFER = bytes()
LOGGER = logging.getLogger(__name__)


class Poller(object):
    """Socket Read Poller."""

    def __init__(self, fileno, exceptions, timeout=5):
        self.select = select
        self._fileno = fileno
        self._exceptions = exceptions
        self.timeout = timeout

    @property
    def fileno(self):
        """Socket Fileno.

        :return:
        """
        return self._fileno

    @property
    def is_ready(self):
        """Is Socket Ready.

        :rtype: tuple
        """
        try:
            ready, _, _ = self.select.select([self.fileno], [], [],
                                             self.timeout)
            return bool(ready)
        except self.select.error as why:
            if why.args[0] != EINTR:
                self._exceptions.append(AMQPConnectionError(why))
        return False


class IO(object):
    """Internal Input/Output handler."""

    def __init__(self, parameters, exceptions=None, on_read=None):
        self._exceptions = exceptions
        self._lock = threading.Lock()
        self._inbound_thread = None
        self._on_read = on_read
        self._running = threading.Event()
        self._parameters = parameters
        self.data_in = EMPTY_BUFFER
        self.poller = None
        self.socket = None
        self.use_ssl = self._parameters['ssl']

    def close(self):
        """Close Socket.

        :return:
        """
        self._lock.acquire()
        try:
            self._running.clear()
            if self.socket:
                self.socket.close()
            if self._inbound_thread:
                self._inbound_thread.join(timeout=self._parameters['timeout'])
            self._inbound_thread = None
            self.poller = None
            self.socket = None
        finally:
            self._lock.release()

    def kill(self):
        if self._inbound_thread.is_alive():
            self._die.value = 1
            while self._inbound_thread.is_alive():
                self._inbound_thread.join(1)

    def open(self):
        """Open Socket and establish a connection.

        :raises AMQPConnectionError: Raises if the connection
                                     encountered an error.
        :return:
        """
        self._lock.acquire()
        try:
            self.data_in = EMPTY_BUFFER
            self._running.set()
            sock_addresses = self._get_socket_addresses()
            self.socket = self._find_address_and_connect(sock_addresses)
            self.poller = Poller(self.socket.fileno(), self._exceptions,
                                 timeout=self._parameters['timeout'])
            self._inbound_thread = self._create_inbound_thread()
        finally:
            self._lock.release()

    def write_to_socket(self, frame_data):
        """Write data to the socket.

        :param str frame_data:
        :return:
        """
        self._lock.acquire()
        try:
            total_bytes_written = 0
            bytes_to_send = len(frame_data)
            while total_bytes_written < bytes_to_send:
                try:
                    if not self.socket:
                        raise socket.error('connection/socket error')
                    bytes_written = \
                        self.socket.send(frame_data[total_bytes_written:])
                    if bytes_written == 0:
                        raise socket.error('connection/socket error')
                    total_bytes_written += bytes_written
                except socket.timeout:
                    pass
                except socket.error as why:
                    if why.args[0] in (EWOULDBLOCK, EAGAIN):
                        continue
                    self._exceptions.append(AMQPConnectionError(why))
                    return
        finally:
            self._lock.release()

    def _get_socket_addresses(self):
        """Get Socket address information.

        :rtype: list
        """
        family = socket.AF_UNSPEC
        if not socket.has_ipv6:
            family = socket.AF_INET
        try:
            addresses = socket.getaddrinfo(self._parameters['hostname'],
                                           self._parameters['port'], family)
        except socket.gaierror as why:
            raise AMQPConnectionError(why)
        return addresses

    def _find_address_and_connect(self, addresses):
        """Find and connect to the appropriate address.

        :param addresses:

        :raises AMQPConnectionError: Raises if the connection
                                     encountered an error.

        :rtype: socket.socket
        """
        for address in addresses:
            sock = self._create_socket(socket_family=address[0])
            try:
                sock.connect(address[4])
            except (IOError, OSError):
                continue
            return sock
        raise AMQPConnectionError(
            'Could not connect to %s:%d' % (
                self._parameters['hostname'],
                self._parameters['port']
            )
        )

    def _create_socket(self, socket_family):
        """Create Socket.

        :param int socket_family:
        :rtype: socket.socket
        """
        sock = socket.socket(socket_family, socket.SOCK_STREAM, 0)
        sock.settimeout(self._parameters['timeout'] or None)
        if self.use_ssl:
            if not compatibility.SSL_SUPPORTED:
                raise AMQPConnectionError(
                    'Python not compiled with support for TLSv1 or higher'
                )
            sock = self._ssl_wrap_socket(sock)
        return sock

    def _ssl_wrap_socket(self, sock):
        """Wrap SSLSocket around the Socket.

        :param socket.socket sock:
        :rtype: SSLSocket
        """
        if 'ssl_version' not in self._parameters['ssl_options']:
            self._parameters['ssl_options']['ssl_version'] = \
                compatibility.DEFAULT_SSL_VERSION
        return ssl.wrap_socket(sock, do_handshake_on_connect=True,
                               **self._parameters['ssl_options'])

    def _create_inbound_thread(self):
        """Internal Thread that handles all incoming traffic.

        :rtype: threading.Thread
        """
        inbound_thread = threading.Thread(target=self._process_incoming_data,
                                          name=__name__)
        inbound_thread.daemon = True
        inbound_thread.start()
        return inbound_thread

    def _process_incoming_data(self):
        """Retrieve and process any incoming data.

        :return:
        """
        while self._running.is_set():
            if self.poller.is_ready:
                self.data_in += self._receive()
                self.data_in = self._on_read(self.data_in)
            sleep(IDLE_WAIT)

    def _receive(self):
        """Receive any incoming socket data.

            If an error is thrown, handle it and return an empty string.

        :return: data_in
        :rtype: bytes
        """
        data_in = EMPTY_BUFFER
        try:
            if not self.socket:
                raise socket.error('connection/socket error')
            data_in = self._read_from_socket()
        except socket.timeout:
            pass
        except (IOError, OSError) as why:
            if why.args[0] not in (EWOULDBLOCK, EAGAIN):
                self._exceptions.append(AMQPConnectionError(why))
                self._running.clear()
        return data_in

    def _read_from_socket(self):
        """Read data from the socket.

        :rtype: bytes
        """
        if self.use_ssl:
            data_in = self.socket.read(FRAME_MAX)
        else:
            data_in = self.socket.recv(FRAME_MAX)
        return data_in
