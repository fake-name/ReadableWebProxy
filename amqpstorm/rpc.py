"""AMQP-Storm Rpc."""

import threading
import time
from uuid import uuid4

from amqpstorm.base import IDLE_WAIT
from amqpstorm.exception import AMQPChannelError


class Rpc(object):
    """AMQP Channel.rpc"""

    def __init__(self, adapter, timeout=360):
        """
        :param Stateful adapter: Connection or Channel.
        :param int|float timeout: Rpc timeout.
        """
        self._lock = threading.Lock()
        self._adapter = adapter
        self._timeout = timeout
        self._response = {}
        self._request = {}

    @property
    def lock(self):
        return self._lock

    def on_frame(self, frame_in):
        """On RPC Frame.

        :param pamqp_spec.Frame frame_in: Amqp frame.
        :return:
        """
        if frame_in.name not in self._request:
            return False

        uuid = self._request[frame_in.name]
        if self._response[uuid]:
            self._response[uuid].append(frame_in)
        else:
            self._response[uuid] = [frame_in]
        return True

    def register_request(self, valid_responses):
        """Register a RPC request.

        :param list valid_responses: List of possible Responses that
                                     we should be waiting for.
        :return:
        """
        uuid = str(uuid4())
        self._response[uuid] = []
        for action in valid_responses:
            self._request[action] = uuid
        return uuid

    def remove(self, uuid):
        """Remove any data related to a specific RPC request.

        :param str uuid: Rpc Identifier.
        :return:
        """
        self.remove_request(uuid)
        self.remove_response(uuid)

    def remove_request(self, uuid):
        """Remove any RPC request(s) using this uuid.

        :param str uuid: Rpc Identifier.
        :return:
        """
        for key in list(self._request):
            if self._request[key] == uuid:
                del self._request[key]

    def remove_response(self, uuid):
        """Remove a RPC Response using this uuid.

        :param str uuid: Rpc Identifier.
        :return:
        """
        if uuid in self._response:
            del self._response[uuid]

    def get_request(self, uuid, raw=False, multiple=False):
        """Get a RPC request.

        :param str uuid: Rpc Identifier
        :param bool raw: If enabled return the frame as is, else return
                         result as a dictionary.
        :param bool multiple: Are we expecting multiple frames.
        :return:
        """
        if uuid not in self._response:
            return
        self._wait_for_request(uuid)
        frame = self._get_response_frame(uuid)
        if not multiple:
            self.remove(uuid)
        result = None
        if raw:
            result = frame
        elif frame is not None:
            result = dict(frame)
        return result

    def _get_response_frame(self, uuid):
        """Get a response frame.

        :param str uuid: Rpc Identifier
        :return:
        """
        frame = None
        frames = self._response.get(uuid, None)
        if frames:
            frame = frames.pop(0)
        return frame

    def _wait_for_request(self, uuid):
        """Wait for RPC request to arrive.

        :param str uuid: Rpc Identifier.
        :return:
        """
        start_time = time.time()
        while not self._response[uuid]:
            self._adapter.check_for_errors()
            if time.time() - start_time > self._timeout:
                self._raise_rpc_timeout_error(uuid)
            time.sleep(IDLE_WAIT)

    def _raise_rpc_timeout_error(self, uuid):
        """Gather information and raise an Rpc exception.

        :param str uuid: Rpc Identifier.
        :return:
        """
        requests = []
        for key, value in self._request.items():
            if value == uuid:
                requests.append(key)
        self.remove(uuid)
        message = ('rpc requests %s (%s) took too long'
                   % (uuid, ', '.join(requests)))
        raise AMQPChannelError(message)
