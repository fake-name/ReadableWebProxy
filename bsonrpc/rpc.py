# -*- coding: utf-8 -*-
'''
Main module providing BSONRpc and JSONRpc.
'''
import re
import six

from bsonrpc.definitions import Definitions
from bsonrpc.exceptions import BsonRpcError, ResponseTimeout
from bsonrpc.dispatcher import Dispatcher
from bsonrpc.framing import JSONFramingRFC7464
from bsonrpc.options import DefaultOptionsMixin, MessageCodec
from bsonrpc.socket_queue import BSONCodec, JSONCodec, SocketQueue
from bsonrpc.util import BatchBuilder, PeerProxy

__license__ = 'http://mozilla.org/MPL/2.0/'


class RpcBase(DefaultOptionsMixin):

    def __init__(self, socket, codec, services=None, **options):
        assert (hasattr(services, '_request_handlers') and
                hasattr(services, '_notification_handlers'))
        for key, value in options.items():
            setattr(self, key, value)
        self.definitions = Definitions(self.protocol,
                                       self.protocol_version,
                                       self.no_arguments_presentation)
        self.services = services
        self.socket_queue = SocketQueue(socket, codec, self.threading_model)
        self.dispatcher = Dispatcher(self)

    @property
    def is_closed(self):
        '''
        :property: bool -- Closed by peer node or with ``close()``
        '''
        return self.socket_queue.is_closed

    def invoke_request(self, method_name, *args, **kwargs):
        '''
        Invoke RPC Request.

        :param method_name: Name of the request method.
        :type method_name: str
        :param args: Arguments
        :param kwargs: Keyword Arguments.
        :returns: Response value(s) from peer.
        :raises: BsonRpcError

        A timeout for the request can be set by giving a special keyword
        argument ``timeout`` (float value of seconds) which can be prefixed
        by any number of underscores - if necessary - to differentiate it from
        the actual keyword arguments going to the peer node method call.

        e.g.
        ``invoke_request('testing', [], {'_timeout': 22, '__timeout: 10.0})``
        would call a request method ``testing(_timeout=22)`` on the RPC peer
        and wait for the response for 10 seconds.

        **NOTE:**
          Use either arguments or keyword arguments. Both can't
          be used in a single call.
          (Naturally the timeout argument does not count to the rule.)
        '''
        rec = re.compile(r'^_*timeout$')
        to_keys = sorted(filter(lambda x: rec.match(x), kwargs.keys()))
        if to_keys:
            timeout = kwargs[to_keys[0]]
            del kwargs[to_keys[0]]
        else:
            timeout = None

        def _send_request(msg_id):
            try:
                promise = self.dispatcher.register(msg_id)
                self.socket_queue.put(
                    self.definitions.request(
                        msg_id, method_name, args, kwargs))
                return promise
            except Exception as e:
                self.dispatcher.unregister(msg_id)
                raise e

        msg_id = six.next(self.id_generator)
        promise = _send_request(msg_id)
        try:
            result = promise.wait(timeout)
        except RuntimeError:
            self.dispatcher.unregister(msg_id)
            raise ResponseTimeout(u'Waiting response expired.')
        if isinstance(result, Exception):
            raise result
        return result

    def invoke_notification(self, method_name, *args, **kwargs):
        '''
        Send an RPC Notification.

        :param method_name: Name of the notification method.
        :type method_name: str
        :param args: Arguments
        :param kwargs: Keyword Arguments.

        **NOTE:**
          Use either arguments or keyword arguments. Both can't
          be used simultaneously in a single call.
        '''
        self.socket_queue.put(
            self.definitions.notification(method_name, args, kwargs))

    def get_peer_proxy(self, requests=None, notifications=None, timeout=None):
        '''
        Get a RPC peer proxy object. Method calls to this object
        are delegated and executed on the connected RPC peer.

        :param requests: A list of method names which can be called and
                         will be delegated to peer node as requests.
                         Default: None -> All arbitrary attributes are
                         handled as requests to the peer.
        :type requests: list of str | None
        :param notifications: A list of method names which can be called and
                              will be delegated to peer node as notifications.
                              Default: None -> If ``requests`` is not ``None``
                              all other attributes are handled as
                              notifications.
        :type notifications: list of str | None
        :param timeout: Timeout in seconds, maximum time to wait responses
                        to each Request.
        :type timeout: float | None
        :returns: A proxy object. Attribute method calls delegated over RPC.

        ``get_peer_proxy()`` (without arguments) will return a proxy
        where all attribute method calls are turned into Requests,
        except calls via ``.n`` which are turned into Notifications.
        Example:
        ::

          proxy = rpc.get_peer_proxy()
          proxy.n.log_this('hello')          # -> Notification
          result = proxy.swap_this('Alise')  # -> Request

        But if arguments are given then the interpretation is explicit and
        ``.n``-delegator is not used:
        ::

          proxy = rpc.get_peer_proxy(['swap_this'], ['log_this'])
          proxy.log_this('hello')            # -> Notification
          result = proxy.swap_this('esilA')  # -> Request
        '''
        return PeerProxy(self, requests, notifications, timeout)

    def close(self):
        '''
        Close the connection and stop the internal dispatcher.
        '''
        # Closing the socket queue causes the dispatcher to close also.
        self.socket_queue.close()

    def join(self, timeout=None):
        '''
        Wait for the internal dispatcher to shut down.

        :param timeout: Timeout in seconds, max time to wait.
        :type timeout: float | None
        '''
        self.dispatcher.join(timeout=timeout)


class DefaultServices(object):

    _request_handlers = {}

    _notification_handlers = {}


class BSONRpc(RpcBase):
    '''
    BSON RPC Connector. Follows closely `JSON-RPC 2.0`_ specification
    with only few differences:

    * Batches are not supported since BSON does not support top-level lists.
    * Keyword 'jsonrpc' has been replaced by 'bsonrpc'

    Connects via socket to RPC peer node. Provides access to the services
    provided by the peer node and makes local services available for the peer.

    To use BSONRpc you need to install ``pymongo``-package
    (see requirements.txt)

    .. _`JSON-RPC 2.0`: http://www.jsonrpc.org/specification
    '''

    #: Protocol name used in messages
    protocol = 'bsonrpc'

    #: Protocol version used in messages
    protocol_version = '2.0'

    def __init__(self, socket, services=None, **options):
        '''
        :param socket: Socket connected to the peer. (Anything behaving like
                       a socket and implementing socket methods ``close``,
                       ``recv``, ``sendall`` and ``shutdown`` is equally
                       viable)
        :type socket: socket.socket
        :param services: Object providing request handlers and
                         notification handlers to be exposed to peer.
                         See `Providing Services`_ for details.
        :type services: ``@service_class`` Class | ``None``
        :param options: Modify behavior by overriding the library defaults.

        **Available options:**

        .. include:: options.snippet
        '''
        self.codec = MessageCodec.BSON
        if not services:
            services = DefaultServices()
        super(BSONRpc, self).__init__(socket,
                                      BSONCodec(),
                                      services=services,
                                      **options)


class JSONRpc(RpcBase):
    '''
    JSON RPC Connector. Implements the `JSON-RPC 2.0`_ specification.

    Connects via socket to RPC peer node. Provides access to the services
    provided by the peer node. Optional ``services`` parameter will take an
    object of which methods are accessible to the peer node.

    Various methods of JSON message framing are available for the stream
    transport.

    .. _`JSON-RPC 2.0`: http://www.jsonrpc.org/specification
    '''

    #: Protocol name used in messages
    protocol = 'jsonrpc'

    #: Protocol version used in messages
    protocol_version = '2.0'

    #: Default choice for JSON Framing
    framing_cls = JSONFramingRFC7464

    def __init__(self, socket, services=None, **options):
        '''
        :param socket: Socket connected to the peer. (Anything behaving like
                       a socket and implementing socket methods ``close``,
                       ``recv``, ``sendall`` and ``shutdown`` is equally
                       viable)
        :type socket: socket.socket
        :param services: Object providing request handlers and
                         notification handlers to be exposed to peer.
                         See `Providing Services`_ for details.
        :type services: ``@service_class`` Class | ``None``
        :param options: Modify behavior by overriding the library defaults.

        **Available options:**

        **framing_cls**
          Selection of framing method implementation.
          Either select one of the following:

          * ``bsonrpc.JSONFramingNetstring``
          * ``bsonrpc.JSONFramingNone``
          * ``bsonrpc.JSONFramingRFC7464`` (Default)

          Or provide your own implementation class for some other framing type.
          See `bsonrpc.framing`_ for details.

        .. include:: options.snippet
        '''
        self.codec = MessageCodec.JSON
        if not services:
            services = DefaultServices()
        framing_cls = options.get('framing_cls', self.framing_cls)
        super(JSONRpc, self).__init__(socket,
                                      JSONCodec(framing_cls.extract_message,
                                                framing_cls.into_frame),
                                      services=services,
                                      **options)

    def batch_call(self, batch_calls, timeout=None):
        '''
        :param batch_calls: Batch of requests/notifications to be executed on
                            the peer node. Use ``BatchBuilder()`` and pass the
                            object here as a parameter.

                            Example:

                            .. code-block:: python

                              bb = BatchBuilder(['swapit', 'times'], ['logit'])
                              bb.swapit('hello')    # request
                              bb.times(3, 5)        # request
                              bb.logit('world')     # notification
                              results = jsonrpc.batch_call(bb, timeout=15.0)
                              # results: ['olleh', 15]

                            Note that ``BatchBuilder`` is used and behaves like
                            the peer-proxy returned by ``.get_peer_proxy()``.

                            Instead of BatchBuilder you may give a simple list
                            argument which must be in the following format:
                            [("r"/"n", "<method-name>", args, kwargs), ...]
        :type batch_calls: bsonrpc.BatchBuilder | list of 4-tuples
        :param timeout: Timeout in seconds for waiting results. Default: None
        :type timeout: float | None
        :returns: * list of results to requests, in order of original requests.
                    Each result may be:

                    * a single return value or
                    * a tuple of return values or
                    * an Exception object

                  * ``None`` if ``batch_calls`` contained only notifications.
        :raises: ResponseTimeout in case batch_calls contains requests,
                 for which response batch did not arrive within timeout.
        '''
        def _compose_batch(batch_calls):
            request_ids = []
            batch = []
            try:
                for call_type, method_name, args, kwargs in batch_calls:
                    if call_type.lower().startswith('n'):
                        batch.append(
                            self.definitions.notification(
                                method_name, args, kwargs))
                    else:
                        msg_id = six.next(self.id_generator)
                        batch.append(
                            self.definitions.request(
                                msg_id, method_name, args, kwargs))
                        request_ids.append(msg_id)
            except Exception as e:
                raise BsonRpcError(
                    u'Malformed batch call: ' + six.text_type(e))
            return request_ids, batch

        def _send_batch_expect_response(request_ids, batch):
            try:
                promise = self.dispatcher.register(tuple(request_ids))
                self.socket_queue.put(batch)
                return promise
            except Exception as e:
                self.dispatcher.unregister(tuple(request_ids))
                raise e

        if isinstance(batch_calls, BatchBuilder):
            batch_calls = batch_calls._batch_calls
        if not batch_calls:
            raise BsonRpcError(u'Refusing to send an empty batch.')
        format_info = (
            u'Argument "batch_calls"(list) is expected to contain '
            u'4-tuples of (str, str, list, dict) -types.')
        for item in batch_calls:
            assert len(item) == 4, format_info
            assert isinstance(item[0], six.string_types), format_info
            assert isinstance(item[1], six.string_types), format_info
            assert isinstance(item[2], (list, tuple)), format_info
            assert isinstance(item[3], dict), format_info
        request_ids, batch = _compose_batch(batch_calls)
        # Notifications only:
        if not request_ids:
            self.socket_queue.put(batch)
            return None
        # At least one request in the batch:
        promise = _send_batch_expect_response(request_ids, batch)
        try:
            results = promise.wait(timeout)
        except RuntimeError:
            self.dispatcher.unregister(tuple(request_ids))
            raise ResponseTimeout(u'Timeout for waiting batch result.')
        if isinstance(results, Exception):
            raise results
        return results
