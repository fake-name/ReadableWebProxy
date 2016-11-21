# -*- coding: utf-8 -*-
'''
This module provides a collection of concurrency related
object generators. These generators will create either
native threading based or greenlet based objects depending
on which threading_model is selected.
'''
from bsonrpc.options import ThreadingModel

__license__ = 'http://mozilla.org/MPL/2.0/'


def _spawn_thread(fn, *args, **kwargs):
    from threading import Thread
    t = Thread(target=fn, args=args, kwargs=kwargs)
    t.start()
    return t


def _spawn_greenlet(fn, *args, **kwargs):
    from gevent import Greenlet
    g = Greenlet(fn, *args, **kwargs)
    g.start()
    return g


def spawn(threading_model, fn, *args, **kwargs):
    if threading_model == ThreadingModel.GEVENT:
        return _spawn_greenlet(fn, *args, **kwargs)
    if threading_model == ThreadingModel.THREADS:
        return _spawn_thread(fn, *args, **kwargs)


def _new_queue(*args, **kwargs):
    from six.moves.queue import Queue
    return Queue(*args, **kwargs)


def _new_gevent_queue(*args, **kwargs):
    from gevent.queue import Queue
    return Queue(*args, **kwargs)


def new_queue(threading_model, *args, **kwargs):
    if threading_model == ThreadingModel.GEVENT:
        return _new_gevent_queue(*args, **kwargs)
    if threading_model == ThreadingModel.THREADS:
        return _new_queue(*args, **kwargs)


def _new_thread_lock(*args, **kwargs):
    from threading import Lock
    return Lock(*args, **kwargs)


def _new_gevent_lock(*args, **kwargs):
    from gevent.lock import Semaphore
    return Semaphore(*args, **kwargs)


def new_lock(threading_model, *args, **kwargs):
    if threading_model == ThreadingModel.GEVENT:
        return _new_gevent_lock(*args, **kwargs)
    if threading_model == ThreadingModel.THREADS:
        return _new_thread_lock(*args, **kwargs)


class Promise(object):

    def __init__(self, event):
        object.__setattr__(self, '_event', event)
        object.__setattr__(self, '_value', None)

    def __getattr__(self, name):
        return getattr(self._event, name)

    def __setattr__(self, name, value):
        if hasattr(self._event, name):
            object.__setattr__(self._event, name, value)
        else:
            object.__setattr__(self, name, value)

    @property
    def value(self):
        return self._value

    def set(self, value):
        object.__setattr__(self, '_value', value)
        self._event.set()

    def wait(self, timeout=None):
        if not self._event.wait(timeout):
            raise RuntimeError(
                u'Promise timeout after %.02f seconds.' % timeout)
        return self._value


def _new_thread_event():
    from threading import Event
    return Event()


def _new_gevent_event():
    from gevent.event import Event
    return Event()


def new_promise(threading_model):
    if threading_model == ThreadingModel.GEVENT:
        return Promise(_new_gevent_event())
    if threading_model == ThreadingModel.THREADS:
        return Promise(_new_thread_event())
