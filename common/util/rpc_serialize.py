
import dill
import logging
import urllib.parse
import socket
import traceback
import threading
import multiprocessing
import queue
import time
import json
import mimetypes
import re
import bs4
import copy
import sys
import base64
import urllib.request
import urllib.parse
import urllib.error

import WebRequest



# Note: The imports in *this* file determine what's available when
# a rpc call is executed.
def serialize_class(tgt_class, exec_method='go'):
	from common.util import remote_base
	ret = {
		'source'      : dill.source.getsource(remote_base.RpcBaseClass) + "\n\n" + dill.source.getsource(tgt_class),
		'callname'    : tgt_class.__name__,
		'exec_method' : exec_method,
	}
	return ret

def deserialize_class(class_blob):
	assert 'source'      in class_blob
	assert 'callname'     in class_blob
	assert 'exec_method' in class_blob

	code = compile(class_blob['source'], "no filename", "exec")
	exec(code)   # pylint: disable=W0122

	cls_def = locals()[class_blob['callname']]
	# This call relies on the source that was exec()ed having defined the class
	# that will now be unserialized.
	return cls_def, class_blob['exec_method']

