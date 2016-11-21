# -*- coding: utf-8 -*-
'''
Library for JSON RPC 2.0 and BSON RPC
'''
from bsonrpc.exceptions import BsonRpcError
from bsonrpc.framing import (
    JSONFramingNetstring, JSONFramingNone, JSONFramingRFC7464)
from bsonrpc.interfaces import (
    notification, request, rpc_notification, rpc_request, service_class)
from bsonrpc.options import NoArgumentsPresentation, ThreadingModel
from bsonrpc.rpc import BSONRpc, JSONRpc
from bsonrpc.util import BatchBuilder


__version__ = '0.1.2'

__license__ = 'http://mozilla.org/MPL/2.0/'

__all__ = [
    'BSONRpc',
    'BatchBuilder',
    'BsonRpcError',
    'JSONFramingNetstring',
    'JSONFramingNone',
    'JSONFramingRFC7464',
    'JSONRpc',
    'NoArgumentsPresentation',
    'ThreadingModel',
    'notification',
    'request',
    'rpc_notification',
    'rpc_request',
    'service_class',
]
