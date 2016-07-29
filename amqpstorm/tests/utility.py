import logging

from amqpstorm.base import Stateful


class SslTLSv1_2(object):
    """Fake SSL Class with TLS v1_2 support used for Unit-Testing."""
    PROTOCOL_TLSv1_2 = 5


class SslTLSv1_1(object):
    """Fake SSL Class with TLS v1_1 support used for Unit-Testing."""
    PROTOCOL_TLSv1_1 = 4


class SslTLSv1(object):
    """Fake SSL Class with TLS v1 support used for Unit-Testing."""
    PROTOCOL_TLSv1 = 3


class SslTLSNone(object):
    """Fake SSL Class with no TLS support used for Unit-Testing."""
    pass


class FakeConnection(Stateful):
    """Fake Connection for Unit-Testing."""

    def __init__(self, state=Stateful.OPEN, on_write=None):
        super(FakeConnection, self).__init__()
        self.frames_out = []
        self.parameters = {
            'hostname': 'localhost',
            'port': 1234,
            'heartbeat': 60,
            'timeout': 30,
            'ssl': False,
            'ssl_options': {}
        }
        self.set_state(state)
        self.on_write = on_write

    def write_frame(self, channel_id, frame_out):
        if self.on_write:
            self.on_write(channel_id, frame_out)
        self.frames_out.append((channel_id, frame_out))

    def write_frames(self, channel_id, frames_out):
        if self.on_write:
            self.on_write(channel_id, frames_out)
        self.frames_out.append((channel_id, frames_out))


class FakeChannel(Stateful):
    """Fake Channel for Unit-Testing."""
    result = list()

    def __init__(self, state=Stateful.OPEN):
        super(FakeChannel, self).__init__()
        self.set_state(state)
        self.basic = FakeBasic(self)

    def close(self):
        self.set_state(self.CLOSED)


class FakeBasic(object):
    """Fake Basic for Unit-Testing."""

    def __init__(self, channel):
        self.channel = channel

    def ack(self, delivery_tag=None, multiple=False):
        self.channel.result.append((delivery_tag, multiple))

    def nack(self, delivery_tag=None, multiple=False, requeue=True):
        self.channel.result.append((delivery_tag, multiple, requeue))

    def reject(self, delivery_tag=None, requeue=True):
        self.channel.result.append((delivery_tag, requeue))


class FakePayload(object):
    """Fake Payload for Unit-Testing."""
    __slots__ = ['name', 'value']

    def __init__(self, name, value=''):
        self.name = name
        self.value = value


class FakeFrame(object):
    """Fake Frame for Unit-Testing."""
    __slots__ = ['name', '_data_1']

    def __init__(self, name='FakeFrame'):
        self.name = name
        self._data_1 = 'hello world'

    def __iter__(self):
        for attribute in ['_data_1']:
            yield (attribute[1::], getattr(self, attribute))


class MockLoggingHandler(logging.Handler):
    """Mock Logging Handler for Unit-Testing."""

    def __init__(self, *args, **kwargs):
        self.messages = {
            'debug': [],
            'info': [],
            'warning': [],
            'error': [],
            'critical': [],
        }
        logging.Handler.__init__(self, *args, **kwargs)

    def emit(self, record):
        self.messages[record.levelname.lower()].append(record.getMessage())


def fake_function():
    """Fake Function used for Unit-Testing."""
    pass
