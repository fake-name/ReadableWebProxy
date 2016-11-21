# -*- coding: utf-8 -*-
'''
Miscellaneous helper functions.
'''
__license__ = 'http://mozilla.org/MPL/2.0/'


def default_id_generator():
    msg_id = 0
    while True:
        msg_id += 1
        yield msg_id
