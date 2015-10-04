

import WebMirror.util.webFunctions
import uuid
import base64
import os
import random
random.seed()

import time
import logging
import WebMirror.util.webFunctions as webFunc

SUFFIXES = [
	'@sogetthis.com',
	'@spamthisplease.com',
	'@zippymail.info',
	'@bobmail.info',
	'@sendspamhere.com',
	'@mailinater.com',
	'@binkmail.com',
	'@tradermail.info',
	'@notmailinator.com',
	'@mailinator2.com',
	'@spambooger.com',
	'@spamherelots.com',
	'@chammy.info',
]

class MailinatorClient(object):

	def __init__(self, override=None):
		self.log = logging.getLogger("Main.Mailinator")
		if override:
			self.prefix = override
		else:
			self.prefix = base64.b32encode(os.urandom(8)).decode("ascii")
			self.prefix = self.prefix.rstrip("=").lower()

		self.postfix = random.choice(SUFFIXES)
		self.log.info("email: '%s%s'" % (self.prefix, self.postfix))

		self.wg = webFunc.WebGetRobust()

	def get_address(self):
		return "%s%s" % (self.prefix, self.postfix)


	def get_available_inbox(self):
		inbox_addr = 'https://www.mailinator.com/inbox.jsp?to={}'.format(self.prefix)
		dummy = self.wg.getpage(inbox_addr)

		# Fake the real client delay
		time.sleep(1)
		inbox_json = 'https://www.mailinator.com/api/webinbox?to={}&time={}'.format(self.prefix, int(time.time() * 1000))
		inbox_ctnt = self.wg.getpage(inbox_json)
		print(inbox_ctnt)


