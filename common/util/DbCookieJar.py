
import http.cookiejar
import atexit
import copy
import logging
import datetime
import traceback
import json
import sqlalchemy.exc
import common.database as db



class DatabaseCookieJar(http.cookiejar.CookieJar):
	"""CookieJar that can be loaded from and saved to a file."""

	def __init__(self, db, session, policy=None):
		http.cookiejar.CookieJar.__init__(self, policy)

		self.log = logging.getLogger("Main.DbCookieJar")

		self.headers = None
		self.db      = db

		self.exit_saved = False
		atexit.register(self._save_at_exit)

	def __del__(self):
		atexit.unregister(self._save_at_exit)

	def init_agent(self, new_headers):
		# self.log.info("Cookiejar inited with headers:")
		# for key, value in new_headers:
		# 	self.log.info("	%s -> %s", key, value)

		self.headers = dict(new_headers)
		self.sync_cookies()


	def __insert_update_cookie(self, sess, cookie):
		have = sess.query(db.WebCookieDb)                                           \
			.filter(db.WebCookieDb.ua_user_agent        == self.headers['User-Agent'])      \
			.filter(db.WebCookieDb.ua_accept_language   == self.headers['Accept-Language']) \
			.filter(db.WebCookieDb.ua_accept            == self.headers['Accept'])          \
			.filter(db.WebCookieDb.ua_accept_encoding   == self.headers['Accept-Encoding']) \
			.filter(db.WebCookieDb.c_name               == cookie.name)                     \
			.filter(db.WebCookieDb.c_domain             == cookie.domain)                   \
			.filter(db.WebCookieDb.c_path               == cookie.path)                     \
			.scalar()

		if have:

			have.c_value              = cookie.value
			have.c_expires            = cookie.expires
			have.c_discard            = cookie.discard
			have.c_comment            = cookie.comment
			have.c_comment_url        = cookie.comment_url
			have.c_rfc2109            = cookie.rfc2109
			have.c_rest               = json.dumps(cookie._rest, sort_keys=True)
			# Already saved cookie, no need to do anything.
			return


		new = db.WebCookieDb(
				age                  = datetime.datetime.now(),
				ua_user_agent        = self.headers['User-Agent'],
				ua_accept_language   = self.headers['Accept-Language'],
				ua_accept            = self.headers['Accept'],
				ua_accept_encoding   = self.headers['Accept-Encoding'],
				c_version            = cookie.version,
				c_name               = cookie.name,
				c_value              = cookie.value,
				c_port               = cookie.port,
				c_port_specified     = cookie.port_specified,
				c_domain             = cookie.domain,
				c_domain_specified   = cookie.domain_specified,
				c_domain_initial_dot = cookie.domain_initial_dot,
				c_path               = cookie.path,
				c_path_specified     = cookie.path_specified,
				c_secure             = cookie.secure,
				c_expires            = cookie.expires,
				c_discard            = cookie.discard,
				c_comment            = cookie.comment,
				c_comment_url        = cookie.comment_url,
				c_rfc2109            = cookie.rfc2109,
				c_rest               = json.dumps(cookie._rest),
			)
		sess.add(new)

	def __save_cookies(self, sess):

		if not len(list(self)):
			return

		self.log.info("Saving %s cookies......", len(list(self)))
		tries = 0
		while 1:
			try:
				for cookie in self:
					self.__insert_update_cookie(sess, cookie)
				sess.commit()
				break
			except sqlalchemy.exc.OperationalError:
				tries += 1
				self.log.warning("Operational error when saving cookies to database")
				sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				tries += 1
				self.log.warning("InvalidRequestError when saving cookies to database")
				sess.rollback()

			except Exception as e:

				for line in traceback.format_exc().split("\n"):
					self.log.error("%s", line.rstrip())
				raise e

			if tries > 10:
				self.log.error("Failure saving cookies!")
			if tries > 11:
				self.log.error("Giving up saving cookies.")
				return

		distinct = set(((c.name, c.domain, c.path) for c in self))

		# print(distinct)

		self.log.info("Saved %s cookies to db (%s distinct).", len(list(self)), len(distinct))


	def __load_cookies(self, sess):

		have = sess.query(db.WebCookieDb)                                           \
			.filter(db.WebCookieDb.ua_user_agent        == self.headers['User-Agent'])      \
			.filter(db.WebCookieDb.ua_accept_language   == self.headers['Accept-Language']) \
			.filter(db.WebCookieDb.ua_accept            == self.headers['Accept'])          \
			.filter(db.WebCookieDb.ua_accept_encoding   == self.headers['Accept-Encoding']) \
			.all()

		for cookie in have:
			new_ck = http.cookiejar.Cookie(
				version            = cookie.c_version,
				name               = cookie.c_name,
				value              = cookie.c_value,
				port               = cookie.c_port,
				port_specified     = cookie.c_port_specified,
				domain             = cookie.c_domain,
				domain_specified   = cookie.c_domain_specified,
				domain_initial_dot = cookie.c_domain_initial_dot,
				path               = cookie.c_path,
				path_specified     = cookie.c_path_specified,
				secure             = cookie.c_secure,
				expires            = cookie.c_expires,
				discard            = cookie.c_discard,
				comment            = cookie.c_comment,
				comment_url        = cookie.c_comment_url,
				rest               = json.loads(cookie.c_rest),
				rfc2109            = cookie.c_rfc2109,
				)
			self.set_cookie(new_ck)

		self.log.info("Loaded %s cookies from db.", len(have))

		sess.commit()

	def sync_cookies(self):
		assert self.headers != None
		with self.db.session_context("cookiejar") as sess:
			self.__save_cookies(sess)
			self.__load_cookies(sess)
			sess.commit()

	def save(self, filename=None, ignore_discard=False, ignore_expires=False):
		if self.exit_saved:
			return

		assert self.headers != None
		for _ in range(10):
			try:
				with self.db.session_context("cookiejar") as sess:
					self.__save_cookies(sess)
					sess.commit()
				return
			except sqlalchemy.exc.SQLAlchemyError:
				pass

	def load(self, filename=None, ignore_discard=False, ignore_expires=False):
		if self.exit_saved:
			return

		assert self.headers != None
		for _ in range(10):
			try:
				with self.db.session_context("cookiejar") as sess:
					self.__load_cookies(sess)
					sess.commit()
				return
			except sqlalchemy.exc.SQLAlchemyError:
				pass


	def revert(self, filename=None, ignore_discard=False, ignore_expires=False):
		self.sync_cookies()


	def _save_at_exit(self):
		self.save()
		self.exit_saved = True

