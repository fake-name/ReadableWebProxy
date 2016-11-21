# -*- coding: utf-8 -*-
'''
Utilities such as BatchBuilder
'''
__license__ = 'http://mozilla.org/MPL/2.0/'


class PeerProxy(object):

    class NotificationProxy(object):

        def __init__(self, rpc):
            self._rpc = rpc

        def __getattr__(self, name):
            def _curried(*args, **kwargs):
                return self._rpc.invoke_notification(name, *args, **kwargs)
            return _curried

    def __init__(self, rpc, requests, notifications, timeout):
        def _item_in(item, collection):
            return collection and item in collection
        self._rpc = rpc
        self._requests = requests
        self._notifications = notifications
        self._timeout = timeout
        self._n = PeerProxy.NotificationProxy(rpc)
        if not (_item_in('n', requests) or _item_in('n', notifications)):
            self.n = self._n

    def __getattr__(self, name):
        if self._requests is None or name in self._requests:
            def _curried(*args, **kwargs):
                return self._rpc.invoke_request(
                    name, *args, _____timeout=self._timeout, **kwargs)
            return _curried
        if self._notifications is None or name in self._notifications:
            return getattr(self._n, name)
        raise AttributeError(
            "'%s' object has no attribute '%s'" %
            (self.__class__.__name__, name))


class BatchBuilder(PeerProxy):
    '''
    Simplify building batches for JSONRpc.batch_call
    '''

    class Delegator(object):

        def __init__(self, par):
            self.par = par

        def invoke_request(self, method, *args, **kwargs):
            self.par._batch_calls.append(('r', method, args, kwargs))

        def invoke_notification(self, method, *args, **kwargs):
            self.par._batch_calls.append(('n', method, args, kwargs))

    def __init__(self, requests=None, notifications=None):
        self._batch_calls = []
        super(BatchBuilder, self).__init__(
            BatchBuilder.Delegator(self), requests, notifications, None)
