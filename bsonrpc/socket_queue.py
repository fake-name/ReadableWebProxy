# -*- coding: utf-8 -*-
'''
JSON & BSON codecs and the SocketQueue class which uses them.
'''
from socket import error as socket_error
from struct import unpack

from bsonrpc.concurrent import new_lock, new_queue, spawn
from bsonrpc.exceptions import (
    BsonRpcError, DecodingError, EncodingError, FramingError)

__license__ = 'http://mozilla.org/MPL/2.0/'


class BSONCodec(object):
    '''
    Encode/Decode message to/from BSON format.

    Pros:
      * Explicit type for binary data
          * No string piggypacking.
          * No size penalties.
      * Explicit type for datetime.
    Cons:
      * No top-level arrays -> no batch support.
    '''

    def __init__(self):
        import bson
        self._loads = lambda raw: bson.BSON.decode(bson.BSON(raw))
        self._dumps = lambda msg: bytes(bson.BSON.encode(msg))

    def loads(self, b_msg):
        try:
            return self._loads(b_msg)
        except Exception as e:
            raise DecodingError(e)

    def dumps(self, msg):
        try:
            return self._dumps(msg)
        except Exception as e:
            raise EncodingError(e)

    def extract_message(self, raw_bytes):
        rb_len = len(raw_bytes)
        if rb_len < 4:
            return None, raw_bytes
        try:
            msg_len = unpack('<i', raw_bytes[:4])[0]
            if msg_len < 5:
                raise FramingError('Minimum valid message length is 5.')
            if rb_len < msg_len:
                return None, raw_bytes
            else:
                return raw_bytes[:msg_len], raw_bytes[msg_len:]
        except Exception as e:
            raise FramingError(e)

    def into_frame(self, message_bytes):
        return message_bytes


class JSONCodec(object):
    '''
    Encode/Decode messages to/from JSON format.
    '''

    def __init__(self, extractor, framer):
        import json
        self._loads = json.loads
        self._dumps = json.dumps
        self._extractor = extractor
        self._framer = framer

    def loads(self, b_msg):
        try:
            return self._loads(b_msg.decode('utf-8'))
        except Exception as e:
            raise DecodingError(e)

    def dumps(self, msg):
        try:
            return self._dumps(msg,
                               separators=(',', ':'),
                               sort_keys=True).encode('utf-8')
        except Exception as e:
            raise EncodingError(e)

    def extract_message(self, raw_bytes):
        try:
            return self._extractor(raw_bytes)
        except Exception as e:
            raise FramingError(e)

    def into_frame(self, message_bytes):
        try:
            return self._framer(message_bytes)
        except Exception as e:
            raise FramingError(e)


class SocketQueue(object):
    '''
    SocketQueue is a duplex Queue connected to a given socket and
    internally takes care of the conversion chain:

    python-data <-> queue-interface <-> codec <-> socket <-:net:-> peer node.
    '''

    BUFSIZE = 4096

    SHUT_RDWR = 2

    def __init__(self, socket, codec, threading_model):
        '''
        :param socket: Socket connected to rpc peer node.
        :type socket: socket.socket
        :param codec: Codec converting python data to/from binary data
        :type codec: BSONCodec or JSONCodec
        :param threading_model: Threading model
        :type threading_model: bsonrpc.options.ThreadingModel.GEVENT or
                               bsonrpc.options.ThreadingModel.THREADS
        '''
        self.socket = socket
        self.codec = codec
        self._queue = new_queue(threading_model)
        self._lock = new_lock(threading_model)
        self._receiver_thread = spawn(threading_model, self._receiver)
        self._closed = False

    @property
    def is_closed(self):
        '''
        :property: bool -- Closed by peer node or with ``close()``
        '''
        return self._closed

    def close(self):
        '''
        Close this queue and the underlying socket.
        '''
        if not self._closed:
            self._closed = True
            self.socket.shutdown(self.SHUT_RDWR)

    def put(self, item):
        '''
        Put item to queue -> codec -> socket.

        :param item: Message object.
        :type item: dict, list or None
        '''
        if self._closed:
            raise BsonRpcError('Attempt to put items to closed queue.')
        msg_bytes = self.codec.into_frame(self.codec.dumps(item))
        with self._lock:
            self.socket.sendall(msg_bytes)

    def get(self):
        '''
        Get message items  <- codec <- socket.

        :returns: Normally a message object (python dict or list) but
                  if socket is closed by peer and queue is drained then
                  ``None`` is returned.
                  May also be Exception object in case of parsing or
                  framing errors.
        '''
        return self._queue.get()

    def _to_queue(self, bbuffer):
        b_msg, bbuffer = self.codec.extract_message(bbuffer)
        while b_msg is not None:
            self._queue.put(self.codec.loads(b_msg))
            b_msg, bbuffer = self.codec.extract_message(bbuffer)
        return bbuffer

    def _receiver(self):
        bbuffer = b''
        while True:
            try:
                chunk = self.socket.recv(self.BUFSIZE)
                bbuffer = self._to_queue(bbuffer + chunk)
                if chunk == b'':
                    break
            except DecodingError as e:
                self._queue.put(e)
            except (OSError, socket_error) as e:
                # shutdown() from another greenlet
                if e.errno != 9:
                    self._queue.put(e)
                break
            except Exception as e:
                self._queue.put(e)
                break
        self._closed = True
        self._queue.put(None)
        try:  # Just in case somehow socket is still open:
            self.socket.shutdown(self.SHUT_RDWR)
        except:
            pass  # Probably already was shut down.
        self.socket.close()

    def join(self, timeout=None):
        '''
        Wait for internal socket receiver thread to finish.
        '''
        self._receiver_thread.join(timeout)
