

# import WebMirror.OutputFilters.AmqpInterface
import config
import common.get_rpyc
import traceback
import sqlalchemy.exc
import urllib.parse
import datetime
import time
import common.database as db
from WebMirror.processor.ProcessorBase import PageProcessor

class FilterBase(PageProcessor):

	# Filters don't return anything, so turn off that checking.
	_no_ret = True
	_needs_amqp = True

	def __init__(self, **kwargs):
		super().__init__()
		# if self._needs_amqp and kwargs.get('connect', True):
		# 	if "message_q" in kwargs and kwargs['message_q']:
		# 		# print("Filter has a queue, not connecting directly.")
		# 		self.msg_q = kwargs['message_q']
		# 	else:
		# 		# print()
		# 		if config.C_DO_RABBIT:
		# 			print("No message queue! Doing independent RabbitMQ connection!")
		# 			# traceback.print_stack()
		# 			# print("Wat?")
		# 			# print()
		# 			self.msg_q = False
		# 			amqp_settings = {
		# 				"RABBIT_LOGIN" : config.C_RABBIT_LOGIN,
		# 				"RABBIT_PASWD" : config.C_RABBIT_PASWD,
		# 				"RABBIT_SRVER" : config.C_RABBIT_SRVER,
		# 				"RABBIT_VHOST" : config.C_RABBIT_VHOST,
		# 				'taskq_task'     : 'task.master.q',
		# 				'taskq_response' : 'response.master.q',
		# 			}

		self.rpc_interface = common.get_rpyc.RemoteJobInterface("FeedUpdater")
		self.rpc_interface.check_ok()

		self._no_ret = True

		self.kwargs = kwargs
		self.db_sess = kwargs['db_sess']
		# 'pageUrl'         : url,
		# 'pgContent'       : content,
		# 'mimeType'        : mimeType,
		# 'db_sess'         : self.db_sess,
		# 'baseUrls'        : self.start_url,
		# 'loggerPath'      : self.loggerPath,
		# 'badwords'        : self.rules['badwords'],
		# 'decompose'       : self.rules['decompose'],
		# 'decomposeBefore' : self.rules['decomposeBefore'],
		# 'fileDomains'     : self.rules['fileDomains'],
		# 'allImages'       : self.rules['allImages'],
		# 'ignoreBadLinks'  : self.rules['IGNORE_MALFORMED_URLS'],
		# 'stripTitle'      : self.rules['stripTitle'],
		# 'relinkable'      : self.relinkable,
		# 'destyle'         : self.rules['destyle'],
		# 'preserveAttrs'   : self.rules['preserveAttrs'],
		# 'type'            : self.rules['type'],
		# 'message_q'       : self.response_queue,
		# 'job'             : self.job,

	def put_page_link(self, link):
		if 'message_q' in self.kwargs and self.kwargs['message_q'] != None and False:
			start = urllib.parse.urlsplit(link).netloc

			assert link.startswith("http")
			assert start
			new = {
				'url'       : link,
				'starturl'  : self.kwargs['job'].starturl,
				'netloc'    : start,
				'distance'  : self.kwargs['job'].distance+1,
				'is_text'   : True,
				'priority'  : self.kwargs['job'].priority,
				'type'      : self.kwargs['job'].type,
				'state'     : "new",
				'fetchtime' : datetime.datetime.now(),
				}
			self.kwargs['message_q'].put(("new_link", new))


	def amqp_put_many(self, items):

		if not self._needs_amqp:
			raise ValueError("Plugin declared to not require AMQP connectivity, and yet AMQP call used?")


		if config.C_DO_RABBIT:
			self.rpc_interface.put_many_feed_job(items)
		else:
			self.log.info("NOT Putting item in to AMQP queue!")


	def amqp_put_item(self, item):


		if not self._needs_amqp:
			raise ValueError("Plugin declared to not require AMQP connectivity, and yet AMQP call used?")

		if config.C_DO_RABBIT:
			self.rpc_interface.put_feed_job(item)
		else:
			self.log.info("NOT Putting item in to AMQP queue!")

		# if config.C_DO_RABBIT:
		# 	self.log.info("Putting item in to AMQP queue!")
		# 	if self.msg_q:
		# 		items_in_queue = self.msg_q.qsize()
		# 		if items_in_queue > 100:
		# 			self.log.warning("AMQP Message queue too large? Items in queue: %s", items_in_queue)

		# 		self.msg_q.put(("amqp_msg", item))

		# 	else:
		# 		self._amqpint.put_item(item)
		# else:
		# 	self.log.info("NOT Putting item in to AMQP queue!")


	def retrigger_page(self, release_url):

		trigger_priority = db.DB_HIGH_PRIORITY

		if self.db_sess is None:
			return
		while 1:
			try:
				have = self.db_sess.query(db.WebPages) \
					.filter(db.WebPages.url == release_url)   \
					.scalar()

				# If we don't have the page, ignore
				# it as the normal new-link upsert mechanism
				# will add it.
				if not have:
					self.log.info("New: '%s'", release_url)
					break

				# Also, don't reset if it's in-progress
				if (
						have.state in ['new', 'fetching', 'processing', 'removed']
						and have.priority <= trigger_priority
						and have.distance > 1
						and have.ignoreuntiltime > datetime.datetime.now() - datetime.timedelta(hours=1)
					):
					self.log.info("Skipping: '%s' (%s, %s)", release_url, have.state, have.priority)
					break

				self.log.info("Retriggering page '%s' (%s, %s)", release_url, have.state, have.priority)
				have.state           = 'new'
				have.ignoreuntiltime = datetime.datetime.now() - datetime.timedelta(days=1)
				have.distance        = 1
				have.priority        = trigger_priority
				self.db_sess.commit()
				break


			except sqlalchemy.exc.InvalidRequestError:
				print("InvalidRequest error!")
				self.db_sess.rollback()
				traceback.print_exc()
			except sqlalchemy.exc.OperationalError:
				print("InvalidRequest error!")
				self.db_sess.rollback()
			except sqlalchemy.exc.IntegrityError:
				print("[upsertRssItems] -> Integrity error!")
				traceback.print_exc()
				self.db_sess.rollback()

