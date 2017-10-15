
import runStatus
import threading
import traceback
import queue
import sys
import time
import common.LogBase as LogBase


import socket
from bsonrpc import BatchBuilder, BSONRpc
from bsonrpc import request, notification, service_class


from bsonrpc.definitions import Definitions
from bsonrpc.exceptions import BsonRpcError, ResponseTimeout
from bsonrpc.dispatcher import Dispatcher
from bsonrpc.framing import JSONFramingRFC7464
from bsonrpc.options import DefaultOptionsMixin, MessageCodec
from bsonrpc.socket_queue import BSONCodec, JSONCodec, SocketQueue
from bsonrpc.util import BatchBuilder, PeerProxy

from bsonrpc.socket_queue import BSONCodec
from bsonrpc.rpc import RpcBase
from bsonrpc.rpc import DefaultServices
import bson


class BetterBSONCodec(BSONCodec):

	def __init__(self):
		self._loads = bson.loads
		self._dumps = bson.dumps


class Fixed_BSONRpc(RpcBase):
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
		super().__init__(socket, BetterBSONCodec(), services=services, **options)

