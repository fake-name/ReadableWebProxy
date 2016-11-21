# -*- coding: utf-8 -*-
'''
Dispatcher for RPC Objects. Routes messages and executes services.
'''
import logging
import six

from bsonrpc.concurrent import new_promise, spawn
from bsonrpc.definitions import RpcErrors
from bsonrpc.exceptions import BsonRpcError
from bsonrpc.options import ThreadingModel

__license__ = 'http://mozilla.org/MPL/2.0/'


class RpcForServices(object):

    def __init__(self, rpc):
        self._rpc = rpc
        self._close_after = False
        self._aborted = False

    @property
    def aborted(self):
        return self._aborted

    @property
    def close_after_response_requested(self):
        return self._close_after

    def __getattr__(self, name):
        if name in ('close', 'join',) or name.startswith('_'):
            raise AttributeError(
                "'%s' is not allowed within service handler.'" % name)
        return getattr(self._rpc, name)

    def abort(self):
        self._aborted = True
        self._rpc.close()

    def close_after_response(self):
        self._close_after = True


class Dispatcher(object):

    def __init__(self, rpc):
        '''
        :param rpc: Rpc parent object.
        :type rpc: RpcBase
        '''

        self.log = logging.getLogger("Main.RPC.Internal")

        # {"<msg_id>": <promise>, ...}
        self._responses = {}
        # { ("<msg_id>", "<msg_id>",): promise, ...}
        self._batch_responses = {}
        # Active threads
        self._active_threads = []
        self.rpc = rpc
        self.conn_label = six.text_type(
            self.rpc.connection_id and '%s: ' % self.rpc.connection_id)
        self._thread = spawn(self.rpc.threading_model, self.run)

    def __getattr__(self, name):
        return getattr(self.rpc, name)

    def _log_info(self, msg, *args, **kwargs):
        pass
        # self.log.info(self.conn_label + six.text_type(msg), *args, **kwargs)

    def _log_error(self, msg, *args, **kwargs):
        self.log.error(self.conn_label + six.text_type(msg), *args, **kwargs)

    def register(self, msg_id):
        promise = new_promise(self.rpc.threading_model)
        if isinstance(msg_id, tuple):
            self._batch_responses[msg_id] = promise
        else:
            self._responses[msg_id] = promise
        return promise

    def unregister(self, msg_id):
        if isinstance(msg_id, tuple):
            promise = self._batch_responses.get(msg_id)
            if msg_id in self._batch_responses:
                del self._batch_responses[msg_id]
        else:
            promise = self._responses.get(msg_id)
            if msg_id in self._responses:
                del self._responses[msg_id]
        if promise and not promise.is_set():
            promise.set(BsonRpcError('Timeout'))

    def _handle_parse_error(self, exception):
        try:
            self.rpc.socket_queue.put(
                self.rpc.definitions.error_response(
                    None, RpcErrors.parse_error, six.text_type(exception)))
        except:
            pass  # Effort made, success not required.
        self._log_error(exception)

    def _get_params(self, msg):
        if 'params' not in msg:
            return [], {}
        params = msg['params']
        if isinstance(params, list):
            return params, {}
        if isinstance(params, dict):
            return [], params

    def _execute_request(self, msg, rfs):
        msg_id = msg['id']
        method_name = msg['method']
        args, kwargs = self._get_params(msg)
        try:
            method = self.rpc.services._request_handlers.get(method_name)
            if method:
                result = method(self.rpc.services, rfs, *args, **kwargs)
                return self.rpc.definitions.ok_response(msg_id, result)
            else:
                return self.rpc.definitions.error_response(
                    msg_id, RpcErrors.method_not_found)
            # NOTE: Python raises TypeError in the "invalid params" case but
            #       that exception may also originate from any number of places
            #       inside the executed function. Python just does not provide
            #       enough granularity to make the distinction. (And grepping
            #       content is a messy heuristics and thus not acceptable.)
            # TODO: The inspect.signature may provide a deterministic way to
            #       correctly identify the "invalid params" case. Consider
            #       using it. Far from trivial though.
        except Exception as e:
            return self.rpc.definitions.error_response(
                msg_id, RpcErrors.server_error, six.text_type(e))

    def _handle_request(self, msg):
        def _execute():
            self._log_info(u'Received request: ' + six.text_type(msg))
            rfs = RpcForServices(self.rpc)
            response = self._execute_request(msg, rfs)
            if rfs.aborted:
                self._log_info(u'Connection aborted in request handler.')
                return
            self.rpc.socket_queue.put(response)
            self._log_info(u'Sent response: ' + six.text_type(response))
            if rfs.close_after_response_requested:
                self.rpc.close()
                self._log_info(
                    u'RPC closed due to invocation by Request handler.')
        tm = self.rpc.concurrent_request_handling
        if tm is None:
            _execute()
        else:
            self._active_threads.append(spawn(tm, _execute))

    def _handle_batch_request(self, msg, rfs):
        def _execute(promise):
            self._log_info(u'Handling batch request: ' + six.text_type(msg))
            response = self._execute_request(msg, rfs)
            self._log_info(
                u'Generated batch response: ' + six.text_type(response))
            promise.set(response)
        tm = self.rpc.concurrent_request_handling
        if tm is None:
            promise = new_promise(ThreadingModel.THREADS)
            _execute(promise)
        else:
            promise = new_promise(tm)
            self._active_threads.append(spawn(tm, _execute, promise))
        return promise

    def _execute_notification(self, msg, rfs, after_effects):
        def _execute():
            method_name = msg['method']
            args, kwargs = self._get_params(msg)
            method = self.rpc.services._notification_handlers.get(method_name)
            if method:
                try:
                    self._log_info(
                        u'Received notification: ' + six.text_type(msg))
                    method(self.rpc.services, rfs, *args, **kwargs)
                except Exception as e:
                    self._log_error(e)
                if (after_effects and not rfs.aborted and
                        rfs.close_after_response_requested):
                    self.rpc.close()
                    self._log_info(
                        u'RPC closed due to invocation by '
                        u'Notification handler.')
            else:
                self._log_error(
                    u'Unrecognized notification from peer: ' +
                    six.text_type(msg))
        tm = self.rpc.concurrent_notification_handling
        if tm is None:
            _execute()
            return None
        else:
            thr = spawn(tm, _execute)
            self._active_threads.append(thr)
            return thr

    def _handle_notification(self, msg):
        rfs = RpcForServices(self.rpc)
        self._execute_notification(msg, rfs, True)

    def _handle_response(self, msg):
        msg_id = msg['id']
        promise = self._responses.get(msg_id)
        if promise:
            if 'result' in msg:
                promise.set(msg['result'])
            else:
                promise.set(RpcErrors.error_to_exception(msg['error']))
        else:
            self._log_error(
                u'Unrecognized/expired response from peer: ' +
                six.text_type(msg))

    def _handle_nil_id_error_response(self, msg):
        self._log_error(msg)

    def _handle_schema_error(self, msg):
        msg_id = None
        if isinstance(msg.get('id'), (six.string_types, int)):
            msg_id = msg['id']
        self.rpc.socket_queue.put(
            self.rpc.definitions.error_response(
                msg_id, RpcErrors.invalid_request))
        self._log_error(u'Invalid Request: ' + six.text_type(msg))

    def _dispatch_batch(self, msgs):
        def _process():
            self._log_info(u'Received batch: ' + six.text_type(msgs))
            rfs = RpcForServices(self.rpc)
            promises = []
            nthreads = []
            for msg in msgs:
                if 'id' in msg:
                    promises.append(self._handle_batch_request(msg, rfs))
                else:
                    nthreads.append(
                        self._execute_notification(msg, rfs, False))
            results = list(map(lambda p: p.wait(), promises))
            if results:
                if rfs.aborted:
                    self._log_info(
                        'Connection aborted during batch processing.')
                    return
                self.rpc.socket_queue.put(results)
                self._log_info(
                    u'Sent batch response: ' + six.text_type(results))
            else:
                self._log_info(u'Notification-only batch processed.')
            if not rfs.close_after_response_requested:
                for nthread in [t for t in nthreads if t]:
                    nthread.join()
            if rfs.close_after_response_requested:
                self.rpc.close()
                self._log_info(
                    u'RPC closed due to invocation by Request or '
                    u'Notification handler.')
        self._active_threads.append(spawn(self.rpc.threading_model, _process))

    def _handle_batch_response(self, msgs):
        def _extract_msg_content(msg):
            if 'result' in msg:
                return msg['result']
            else:
                return RpcErrors.error_to_exception(msg['error'])

        without_id_msgs = list(filter(lambda x: x.get('id') is None, msgs))
        with_id_msgs = list(filter(lambda x: x.get('id') is not None, msgs))
        resp_map = dict(map(lambda x: (x['id'], x), with_id_msgs))
        msg_ids = set(resp_map.keys())
        resolved = False
        for idtuple, promise in self._batch_responses.items():
            if msg_ids.issubset(set(idtuple)):
                batch_response = []
                for req_id in idtuple:
                    if req_id in resp_map:
                        batch_response.append(
                            _extract_msg_content(resp_map[req_id]))
                    elif without_id_msgs:
                        batch_response.append(
                            _extract_msg_content(without_id_msgs.pop(0)))
                    else:
                        batch_response.append(
                            BsonRpcError(
                                'Peer did not respond to this request!'))
                promise.set(batch_response)
                resolved = True
                break
        if not resolved:
            self._log_error(
                u'Unrecognized/expired batch response from peer: ' +
                six.text_type(msgs))

    def run(self):
        def _otherwise(*_):
            return True

        def _is_alive(thr):
            try:
                return not thr.ready()
            except AttributeError:
                return thr.is_alive()

        rpcd = self.rpc.definitions
        dispatch = {
            dict: [
                (rpcd.is_request, self._handle_request),
                (rpcd.is_notification, self._handle_notification),
                (rpcd.is_response, self._handle_response),
                (rpcd.is_nil_id_error_response,
                    self._handle_nil_id_error_response),
                (_otherwise, self._handle_schema_error),
            ],
            list: [
                (rpcd.is_batch_request, self._dispatch_batch),
                (rpcd.is_batch_response, self._handle_batch_response),
                (_otherwise, self._handle_schema_error),
            ]
        }

        self._log_info(u'Start RPC message dispatcher.')
        while True:
            try:
                msg = self.rpc.socket_queue.get()
                self._active_threads = list(
                    filter(lambda t: _is_alive(t), self._active_threads))
                if msg is None:
                    break
                self._log_info(u'Dispatch message.')
                if isinstance(msg, Exception):
                    self._handle_parse_error(msg)
                else:
                    for match_fn, handler_fn in dispatch.get(
                            type(msg),
                            [(_otherwise, self._handle_schema_error)]):
                        if match_fn(msg):
                            handler_fn(msg)
                            break
            except Exception as e:
                self._log_error(e)
        self._log_info(u'Exit RPC message dispatcher.')

    def join(self, timeout=None):
        def _totaljoiner():
            self._thread.join()
            for thr in self._active_threads:
                thr.join()
        joiner_thread = spawn(self.rpc.threading_model, _totaljoiner)
        joiner_thread.join(timeout)
