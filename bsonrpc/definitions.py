# -*- coding: utf-8 -*-
'''
Definitions to match messages to JSON RPC 2.0 schema and to produce them.
Also RPC error definitions.
'''
import six

from bsonrpc.exceptions import (
    InternalError, InvalidParams, InvalidRequest, MethodNotFound,
    ParseError, ServerError, UnspecifiedPeerError)
from bsonrpc.options import NoArgumentsPresentation

__license__ = 'http://mozilla.org/MPL/2.0/'


class Definitions(object):

    def __init__(self, protocol, protocol_version, no_args):
        self.protocol = protocol
        self.protocol_version = protocol_version
        self._no_args = no_args  # Strategy to represent no args

    def _set_params(self, msg, args, kwargs):
        if not args and not kwargs:
            if self._no_args == NoArgumentsPresentation.EMPTY_ARRAY:
                msg['params'] = []
            if self._no_args == NoArgumentsPresentation.EMPTY_OBJECT:
                msg['params'] = {}
            return msg
        if args:
            msg['params'] = args
        else:
            msg['params'] = kwargs
        return msg

    def request(self, msg_id, method_name, args, kwargs):
        msg = {
            self.protocol: self.protocol_version,
            'id': msg_id,
            'method': method_name,
        }
        msg = self._set_params(msg, args, kwargs)
        return msg

    def notification(self, method_name, args, kwargs):
        msg = {
            self.protocol: self.protocol_version,
            'method': method_name,
        }
        msg = self._set_params(msg, args, kwargs)
        return msg

    def ok_response(self, msg_id, result):
        return {
            self.protocol: self.protocol_version,
            'id': msg_id,
            'result': result
        }

    def error_response(self, msg_id, error, details=None):
        msg = {
            self.protocol: self.protocol_version,
            'id': msg_id,
            'error': error
        }
        if details:
            msg['error']['data'] = details
        return msg

    def _chk_protocol(self, msg):
        return msg.get(self.protocol, None) == self.protocol_version

    def _has_method(self, msg):
        return isinstance(msg.get('method', None), six.string_types)

    def _valid_params(self, msg):
        return ('params' not in msg or isinstance(msg['params'], (list, dict)))

    def is_request(self, msg):
        return (self._chk_protocol(msg) and
                self._has_method(msg) and
                'id' in msg and
                (msg['id'] is None or
                 isinstance(msg['id'], (six.string_types, int))) and
                self._valid_params(msg))

    def is_notification(self, msg):
        return (self._chk_protocol(msg) and
                self._has_method(msg) and
                'id' not in msg and
                self._valid_params(msg))

    def is_response(self, msg):
        result_and_no_error = 'result' in msg and 'error' not in msg
        error_and_no_result = 'error' in msg and 'result' not in msg
        return (self._chk_protocol(msg) and
                isinstance(msg.get('id', None), (six.string_types, int)) and
                (result_and_no_error or error_and_no_result))

    def is_nil_id_error_response(self, msg):
        error_and_no_result = 'error' in msg and 'result' not in msg
        return (self._chk_protocol(msg) and
                error_and_no_result and
                'id' in msg and
                msg['id'] is None)

    def is_batch_request(self, msg_list):
        if not msg_list:
            return False
        for msg in msg_list:
            if not self.is_request(msg) and not self.is_notification(msg):
                return False
        return True

    def is_batch_response(self, msg_list):
        if not msg_list:
            return False
        for msg in msg_list:
            if not self.is_response(msg):
                return False
        return True


class RpcErrors(object):

    parse_error = {'code': -32700, 'message': 'Parse error'}
    invalid_request = {'code': -32600, 'message': 'Invalid Request'}
    method_not_found = {'code': -32601, 'message': 'Method not found'}
    invalid_params = {'code': -32602, 'message': 'Invalid params'}
    internal_error = {'code': -32603, 'message': 'Internal error'}
    server_error = {'code': -32000, 'message': 'Server error'}

    _promote = {
        -32700: ParseError,
        -32600: InvalidRequest,
        -32601: MethodNotFound,
        -32602: InvalidParams,
        -32603: InternalError,
        -32000: ServerError,
    }

    @classmethod
    def error_to_exception(cls, error):
        code = error.get('code', 0)
        message = error.get('message', '')
        data = error.get('data', '')
        exception_cls = cls._promote.get(code, UnspecifiedPeerError)
        return exception_cls(code, message, data)
