# -*- coding: utf-8 -*-
'''
Option definitions and default options.
'''
from bsonrpc.misc import default_id_generator

__license__ = 'http://mozilla.org/MPL/2.0/'


class MessageCodec(object):

    BSON = 'bson'

    JSON = 'json'


class ThreadingModel(object):

    THREADS = 'threads'

    GEVENT = 'gevent'


class NoArgumentsPresentation(object):

    OMIT = 'omit'

    EMPTY_ARRAY = 'empty-array'

    EMPTY_OBJECT = 'empty-object'


class DefaultOptionsMixin(object):

    connection_id = ''

    id_generator = default_id_generator()

    concurrent_notification_handling = None

    concurrent_request_handling = ThreadingModel.THREADS

    no_arguments_presentation = NoArgumentsPresentation.OMIT

    threading_model = ThreadingModel.THREADS
