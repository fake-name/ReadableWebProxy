from amqpstorm.exception import AMQPError
from amqpstorm.exception import AMQP_ERROR_MAPPING


class ApiError(AMQPError):
    """Management Api Error"""

    def __init__(self, message=None, *args, **kwargs):
        self._message = message
        self._error_code = kwargs.pop('reply_code', None)
        super(AMQPError, self).__init__(*args, **kwargs)
        if self._error_code not in AMQP_ERROR_MAPPING:
            return
        self._error_type = AMQP_ERROR_MAPPING[self._error_code][0]
        self._documentation = AMQP_ERROR_MAPPING[self._error_code][1]

    def __str__(self):
        if self._error_code in AMQP_ERROR_MAPPING:
            return '%s - %s' % (self.error_type, self.documentation)
        return self._message


class ApiConnectionError(AMQPError):
    """Management Api Connection Error"""
    pass
