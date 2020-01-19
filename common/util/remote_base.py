
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
import abc
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



class RpcBaseClass():
	logname = "Main.RemoteExec.Base"

	def __init__(self, wg):
		self.out_buffer = []
		self.local_logger = logging.getLogger(self.logname)
		self.wg = wg

		self.__install_logproxy()
		self.log.info("RemoteExecClass Instantiated")

	def _go(self, *args, **kwargs):
		raise RuntimeError
		return "What?"

	def __install_logproxy(self):
		# pylint: disable=W0212
		class LogProxy():
			def __init__(self, parent_logger, log_prefix):
				self.parent_logger = parent_logger
				self.log_prefix    = log_prefix
			def debug(self, msg, *args):
				self.parent_logger._debug   (" [{}] -> ".format(self.log_prefix) + msg, *args)
			def info(self, msg, *args):
				self.parent_logger._info    (" [{}] -> ".format(self.log_prefix) + msg, *args)
			def error(self, msg, *args):
				self.parent_logger._error   (" [{}] -> ".format(self.log_prefix) + msg, *args)
			def critical(self, msg, *args):
				self.parent_logger._critical(" [{}] -> ".format(self.log_prefix) + msg, *args)
			def warning(self, msg, *args):
				self.parent_logger._warning (" [{}] -> ".format(self.log_prefix) + msg, *args)
			def warn(self, msg, *args):
				self.parent_logger._warning (" [{}] -> ".format(self.log_prefix) + msg, *args)

		self.wg.log = LogProxy(self, "WebGet")
		self.log    = LogProxy(self, "MainRPCAgent")


	def _debug(self, msg, *args):
		tmp = self.logname + " [DEBUG] ->" + msg % args
		self.local_logger.debug(tmp)
		self.out_buffer.append(tmp)
	def _info(self, msg, *args):
		tmp = self.logname + " [INFO] ->" + msg % args
		self.local_logger.info(tmp)
		self.out_buffer.append(tmp)
	def _error(self, msg, *args):
		tmp = self.logname + " [ERROR] ->" + msg % args
		self.local_logger.error(tmp)
		self.out_buffer.append(tmp)
	def _critical(self, msg, *args):
		tmp = self.logname + " [CRITICAL] ->" + msg % args
		self.local_logger.critical(tmp)
		self.out_buffer.append(tmp)
	def _warning(self, msg, *args):
		tmp = self.logname + " [WARNING] ->" + msg % args
		self.local_logger.warning(tmp)
		self.out_buffer.append(tmp)


	def go(self, *args, **kwargs):
		print("RPC Running!")
		print("Args, kwargs: ", (args, kwargs))
		try:
			ret = self._go(*args, **kwargs)  # pylint: disable=W0212
			ret = (self.out_buffer, ret)
			print("RPC Done! Ret: ", ret)
			return ret
		except Exception as e:
			import sys
			log_txt = '\n	'.join(self.out_buffer)
			exc_message = '{}\nLog report:\n	{}'.format(str(e), log_txt)
			rebuilt = type(e)(exc_message).with_traceback(sys.exc_info()[2])
			rebuilt.log_data = self.out_buffer
			print("RPC encountered error!")
			raise rebuilt
