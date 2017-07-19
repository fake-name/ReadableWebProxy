"""AMQPStorm Connection.Heartbeat."""

import logging
import threading

from amqpstorm.exception import AMQPConnectionError

LOGGER = logging.getLogger(__name__)


class Heartbeat(object):
    """Internal Heartbeat handler."""

    def __init__(self, interval, send_heartbeat, timer=threading.Timer):
        self.send_heartbeat = send_heartbeat
        self.timer_impl = timer
        self._lock = threading.Lock()
        self._running = threading.Event()
        self._timer = None
        self._exceptions = None
        self._reads_since_check = 0
        self._writes_since_check = 0
        self._interval = interval
        self._threshold = 0

    def register_read(self):
        """Register that a frame has been received.

        :return:
        """
        self._reads_since_check += 1

    def register_write(self):
        """Register that a frame has been sent.

        :return:
        """
        self._writes_since_check += 1

    def start(self, exceptions):
        """Start the Heartbeat Checker.

        :param list exceptions:
        :return:
        """
        if not self._interval:
            return False
        self._running.set()
        with self._lock:
            self._threshold = 0
            self._reads_since_check = 0
            self._writes_since_check = 0
        self._exceptions = exceptions
        LOGGER.debug('Heartbeat Checker Started')
        return self._start_new_timer()

    def stop(self):
        """Stop the Heartbeat Checker.

        :return:
        """
        self._running.clear()
        with self._lock:
            if self._timer:
                self._timer.cancel()
            self._timer = None

    def _check_for_life_signs(self):
        """Check Connection for life signs.

            First check if any data has been sent, if not send a heartbeat
            to the remote server.

            If we have not received any data what so ever within two
            intervals, we need to raise an exception so that we can
            close the connection.

        :rtype: bool
        """
        if not self._running.is_set():
            return False
        if self._writes_since_check == 0:
            self.send_heartbeat()
        self._lock.acquire()
        try:
            if self._reads_since_check == 0:
                self._threshold += 1
                if self._threshold >= 2:
                    self._running.clear()
                    self._raise_or_append_exception()
                    return False
            else:
                self._threshold = 0
        finally:
            self._reads_since_check = 0
            self._writes_since_check = 0
            self._lock.release()

        return self._start_new_timer()

    def _raise_or_append_exception(self):
        """The connection is presumably dead and we need to raise or
        append an exception.

            If we have a list for exceptions, append the exception and let
            the connection handle it, if not raise the exception here.

        :return:
        """
        message = (
            'Connection dead, no heartbeat or data received in >= '
            '%ds' % (
                self._interval * 2
            )
        )
        why = AMQPConnectionError(message)
        if self._exceptions is None:
            raise why
        self._exceptions.append(why)

    def _start_new_timer(self):
        """Create a timer that will be used to periodically check the
        connection for heartbeats.

        :return:
        """
        if not self._running.is_set():
            return False
        self._timer = self.timer_impl(
            interval=self._interval,
            function=self._check_for_life_signs
        )
        self._timer.daemon = True
        self._timer.start()
        return True
