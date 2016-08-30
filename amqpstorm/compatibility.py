"""Python 2/3 Compatibility layer."""

import sys

try:
    import ssl
except ImportError:
    ssl = None

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

PYTHON3 = sys.version_info >= (3, 0, 0)

if PYTHON3:
    RANGE = range
else:
    RANGE = xrange

SSL_CERT_MAP = {}
SSL_VERSIONS = {}
SSL_OPTIONS = [
    'keyfile',
    'certfile',
    'cert_reqs',
    'ssl_version',
    'ca_certs'
]


def get_default_ssl_version():
    """Get the highest support TLS version, if none is available, return None.

    :rtype: bool|None
    """
    if not ssl:
        return None
    elif hasattr(ssl, 'PROTOCOL_TLSv1_2'):
        return ssl.PROTOCOL_TLSv1_2
    elif hasattr(ssl, 'PROTOCOL_TLSv1_1'):
        return ssl.PROTOCOL_TLSv1_1
    elif hasattr(ssl, 'PROTOCOL_TLSv1'):
        return ssl.PROTOCOL_TLSv1
    return None


DEFAULT_SSL_VERSION = get_default_ssl_version()
SSL_SUPPORTED = DEFAULT_SSL_VERSION is not None
if SSL_SUPPORTED:
    if hasattr(ssl, 'PROTOCOL_TLSv1_2'):
        SSL_VERSIONS['protocol_tlsv1_2'] = ssl.PROTOCOL_TLSv1_2
    if hasattr(ssl, 'PROTOCOL_TLSv1_1'):
        SSL_VERSIONS['protocol_tlsv1_1'] = ssl.PROTOCOL_TLSv1_1
    if hasattr(ssl, 'PROTOCOL_TLSv1'):
        SSL_VERSIONS['protocol_tlsv1'] = ssl.PROTOCOL_TLSv1

    SSL_CERT_MAP = {
        'cert_none': ssl.CERT_NONE,
        'cert_optional': ssl.CERT_OPTIONAL,
        'cert_required': ssl.CERT_REQUIRED
    }


def is_string(obj):
    """Is this a string.

    :param object obj:
    :rtype: bool
    """
    if PYTHON3:
        str_type = (bytes, str)
    else:
        str_type = (bytes, str, unicode)
    return isinstance(obj, str_type)


def is_integer(obj):
    """Is this an integer.

    :param object obj:
    :return:
    """
    if PYTHON3:
        return isinstance(obj, int)
    return isinstance(obj, (int, long))


def is_unicode(obj):
    """Is this a unicode string.

        This always returns False if running Python 3.x.

    :param object obj:
    :rtype: bool
    """
    if PYTHON3:
        return False
    return isinstance(obj, unicode)


def try_utf8_decode(value):
    """Try to decode an object.

    :param value:
    :return:
    """
    if not value or not is_string(value):
        return value
    elif PYTHON3 and not isinstance(value, bytes):
        return value
    elif not PYTHON3 and not isinstance(value, unicode):
        return value

    try:
        return value.decode('utf-8')
    except UnicodeDecodeError:
        pass

    return value


def patch_uri(uri):
    """If a custom uri schema is used with python 2.6 (e.g. amqps),
    it will ignore some of the parsing logic.

        As a work-around for this we change the amqp/amqps schema
        internally to use http/https.

    :param str uri: AMQP Connection string
    :rtype: str
    """
    index = uri.find(':')
    if uri[:index] == 'amqps':
        uri = uri.replace('amqps', 'https', 1)
    elif uri[:index] == 'amqp':
        uri = uri.replace('amqp', 'http', 1)
    return uri
