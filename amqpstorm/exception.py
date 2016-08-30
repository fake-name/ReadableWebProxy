"""AMQPStorm Exception."""

AMQP_ERROR_MAPPING = {
    311: ('CONTENT-TOO-LARGE',
          'The client attempted to transfer content larger than the '
          'server could accept at the present time. The client may '
          'retry  at a later time.'),
    312: ('NO-ROUTE', 'Undocumented AMQP Soft Error'),
    313: ('NO-CONSUMERS',
          'When the exchange cannot deliver to a consumer when the '
          'immediate flag is set. As a result of pending data on '
          'the queue or the absence of any consumers of the queue.'),
    320: ('CONNECTION-FORCED',
          'An operator intervened to close the connection for some reason. '
          'The client may retry at some later date.'),
    402: ('INVALID-PATH',
          'The client tried to work with an unknown virtual host.'),
    403: ('ACCESS-REFUSED',
          'The client attempted to work with a server entity to which '
          'has no access due to security settings.'),
    404: ('NOT-FOUND',
          'The client attempted to work with a server '
          'entity that does not exist.'),
    405: ('RESOURCE-LOCKED',
          'The client attempted to work with a server entity to which it '
          'has no access because another client is working with it.'),
    406: ('PRECONDITION-FAILED',
          'The client requested a method that was not '
          'allowed because some precondition failed.'),
    501: ('FRAME-ERROR',
          'The sender sent a malformed frame that the recipient could '
          'not decode. This strongly implies a programming error in '
          'the sending peer.'),
    502: ('SYNTAX-ERROR',
          'The sender sent a frame that contained illegal values for '
          'one or more fields. This strongly implies a programming '
          'error in the sending peer.'),
    503: ('COMMAND-INVALID',
          'The client sent an invalid sequence of frames, attempting to '
          'perform an operation that was considered invalid by the server. '
          'This usually implies a programming error in the client.'),
    504: ('CHANNEL-ERROR',
          'The client attempted to work with a channel that had not '
          'been correctly opened. This most likely indicates a '
          'fault in the client layer.'),
    505: ('UNEXPECTED-FRAME',
          'The peer sent a frame that was not expected, usually in the '
          'context of a content header and body. This strongly '
          'indicates a fault in the peer\'s content processing.'),
    506: ('RESOURCE-ERROR',
          'The server could not complete the method because it lacked '
          'sufficient resources. This may be due to the client '
          'creating too many of some type of entity.'),
    530: ('NOT-ALLOWED',
          'The client tried to work with some entity in a manner '
          'that is prohibited by the server, due to security '
          'settings or by some other criteria.'),
    540: ('NOT-IMPLEMENTED',
          'The client tried to use functionality that is '
          'notimplemented in the server.'),
    541: ('INTERNAL-ERROR',
          'The server could not complete the method because of an '
          'internal error. The server may require intervention by '
          'an operator in order to resume normal operations.')
}


class AMQPError(IOError):
    """General AMQP Error"""
    _documentation = None
    _error_code = None
    _error_type = None

    @property
    def documentation(self):
        """AMQP Documentation string."""
        return self._documentation or bytes()

    @property
    def error_code(self):
        """AMQP Error Code - A 3-digit reply code."""
        return self._error_code

    @property
    def error_type(self):
        """AMQP Error Type e.g. NOT-FOUND."""
        return self._error_type

    def __init__(self, *args, **kwargs):
        self._error_code = kwargs.pop('reply_code', None)
        super(AMQPError, self).__init__(*args, **kwargs)
        if self._error_code not in AMQP_ERROR_MAPPING:
            return
        self._error_type = AMQP_ERROR_MAPPING[self._error_code][0]
        self._documentation = AMQP_ERROR_MAPPING[self._error_code][1]


class AMQPConnectionError(AMQPError):
    """AMQP Connection Error"""
    pass


class AMQPChannelError(AMQPError):
    """AMQP Channel Error"""
    pass


class AMQPMessageError(AMQPChannelError):
    """AMQP Message Error"""
    pass


class AMQPInvalidArgument(AMQPError):
    """AMQP Argument Error"""
