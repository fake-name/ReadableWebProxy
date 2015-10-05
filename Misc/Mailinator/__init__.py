

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
		inbox_ctnt = self.wg.getJson(inbox_json)
		assert "messages" in inbox_ctnt

		return inbox_ctnt['messages']
		# for message in inbox_ctnt['messages']:
		# 	print(message)
		# 	self.get_mail(message['id'])
		# print(inbox_ctnt)

	def get_mail(self, mail_id):
		fetch_ts = int(time.time() * 1000)
		head_url = "https://www.mailinator.com/renderhead.jsp?msgid={msgid}&time={time}".format(msgid=mail_id, time=fetch_ts)
		mail_url = "https://www.mailinator.com/rendermail.jsp?msgid={msgid}&time={time}".format(msgid=mail_id, time=fetch_ts)
		self.log.info("Fetching mail for id: '%s'", mail_id)
		referer_url = "https://www.mailinator.com/inbox.jsp?to={name}".format(name=self.prefix)
		dummy_hdr = self.wg.getpage(head_url, addlHeaders={'Referer': referer_url})
		mail_ctnt = self.wg.getpage(mail_url, addlHeaders={'Referer': referer_url})
		return mail_ctnt


