import logging

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from amqpstorm.exception import AMQPError

logging.basicConfig(level=logging.DEBUG)


class ExceptionTests(unittest.TestCase):
    def test_exception_documentation_matching(self):
        exception = AMQPError('error', reply_code=312)

        self.assertEqual(str(exception), 'error')

        self.assertEqual(exception.documentation,
                         'Undocumented AMQP Soft Error')

    def test_exception_error_type_matching(self):
        exception = AMQPError('error', reply_code=404)

        self.assertEqual(str(exception), 'error')

        self.assertEqual(exception.error_type,
                         'NOT-FOUND')

    def test_exception_error_code_matching(self):
        exception = AMQPError('error', reply_code=406)

        self.assertEqual(str(exception), 'error')

        self.assertEqual(exception.error_code, 406)

    def test_exception_invalid_error_code(self):
        exception = AMQPError('error', reply_code=123)

        self.assertEqual(str(exception), 'error')
        self.assertEqual(exception.error_code, 123)

        self.assertFalse(exception.error_type)
        self.assertFalse(exception.documentation)

    def test_exception_no_error_code(self):
        exception = AMQPError('error')

        self.assertEqual(str(exception), 'error')

        self.assertFalse(exception.error_type)
        self.assertFalse(exception.error_code)
        self.assertFalse(exception.documentation)
