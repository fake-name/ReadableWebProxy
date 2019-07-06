
import sys
import multiprocessing
import threading
import logging
import contextlib
import time
import traceback
import queue


import sqlalchemy.exc
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker



from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy


from settings import DATABASE_IP            as C_DATABASE_IP
from settings import DATABASE_DB_NAME       as C_DATABASE_DB_NAME
from settings import DATABASE_USER          as C_DATABASE_USER
from settings import DATABASE_PASS          as C_DATABASE_PASS

from flask import g

from settings import MAX_DB_SESSIONS
import flags

if '__pypy__' in sys.builtin_module_names:
	SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2cffi://{user}:{passwd}@{host}:5432/{database}'.format(user=C_DATABASE_USER, passwd=C_DATABASE_PASS, host=C_DATABASE_IP, database=C_DATABASE_DB_NAME)
else:
	SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{passwd}@{host}:5432/{database}'.format(user=C_DATABASE_USER, passwd=C_DATABASE_PASS, host=C_DATABASE_IP, database=C_DATABASE_DB_NAME)


log = logging.getLogger("Main.DB-Engine")

SESSIONS = {}
ENGINES  = {}
POOL    = None


ENGINE_LOCK = multiprocessing.Lock()
SESSION_LOCK = multiprocessing.Lock()

def get_engine():
	cpid = multiprocessing.current_process().name
	ctid = threading.current_thread().name
	csid = "{}-{}".format(cpid, ctid)
	if not csid in ENGINES:
		with ENGINE_LOCK:
			# Check if the engine was created while we were
			# waiting on the lock.
			if csid in ENGINES:
				return ENGINES[csid]

			log.info("INFO: Creating engine for process! Engine name: '%s'" % csid)
			ENGINES[csid] = create_engine(SQLALCHEMY_DATABASE_URI,
						isolation_level="REPEATABLE READ")
						# isolation_level="READ COMMITTED")

	return ENGINES[csid]



def get_db_session(postfix="", flask_sess_if_possible=True):
	if flags.IS_FLASK and flask_sess_if_possible:
		return g.session


	cpid = multiprocessing.current_process().name
	ctid = threading.current_thread().name
	csid = "{}-{}-{}".format(cpid, ctid, postfix)

	# print("Getting session for thread: %s" % csid)
	# print(traceback.print_stack())
	# print("==========================")


	if not csid in SESSIONS:
		acquired = False

		# This is horrible, but it works around a context holding the lock going away.
		# Apparently that has actually happened.
		while True:
			acquired = SESSION_LOCK.acquire(timeout=5)
			if acquired:
				break
			else:
				print("Error!")
				print("Error!")
				print("SESSION_LOCK TIMEOUT!")
				print("Error!")
				print("Error!")
				print("Clearing lock as last-resort!")
				SESSION_LOCK.release()

		try:
			# check if the session was created while
			# we were waiting for the lock
			if csid in SESSIONS:
				# Reset the "last used" time on the handle
				SESSIONS[csid][0] = time.time()
				ret = SESSIONS[csid][1]

				# Attempt to probe the connection to make sure it's alive before returning it.
				_ = ret.connection().connection.isolation_level
				assert ret.connection().connection.closed == 0
				return ret

			SESSIONS[csid] = [time.time(), scoped_session(sessionmaker(bind=get_engine(), autoflush=False, autocommit=False))()]
			# print("Creating database interface:", SESSIONS[csid])

			# Delete the session that's oldest.
			if len(SESSIONS) > MAX_DB_SESSIONS:
				log.info("WARN: More then %s active sessions! Deleting oldest session to prevent session contention." % MAX_DB_SESSIONS)
				maxsz = sys.maxsize
				to_delete = None
				for key, value in SESSIONS.items():
					if value[0] < maxsz:
						to_delete = key
						maxsz = value[0]
				if to_delete:
					del SESSIONS[to_delete]
		finally:
			SESSION_LOCK.release()

	# Reset the "last used" time on the handle
	SESSIONS[csid][0] = time.time()
	return SESSIONS[csid][1]

def delete_db_session(postfix="", flask_sess_if_possible=True):
	if flags.IS_FLASK and flask_sess_if_possible:
		# No need to do anything with flask sess
		return

	cpid = multiprocessing.current_process().name
	ctid = threading.current_thread().name
	csid = "{}-{}-{}".format(cpid, ctid, postfix)


	# print("Releasing session for thread: %s" % csid)
	# print(traceback.print_stack())
	# print("==========================")

	if csid in SESSIONS:
		with SESSION_LOCK:
			# check if the session was created while
			# we were waiting for the lock
			if not csid in SESSIONS:
				return
			SESSIONS[csid][1].close()
			del SESSIONS[csid]
			# print("Deleted session for id: ", csid)

@contextlib.contextmanager
def session_context(name="", override_timeout_ms=False):
	sess = get_db_session(postfix=name + 'context-sess')
	try:
		if override_timeout_ms:
			log.warning("Query timeout overridden to be %0.2f seconds!", override_timeout_ms / 1000.0, )
			sess.execute("""SET statement_timeout TO :new_timeout;""", { 'new_timeout' : override_timeout_ms, })
		yield sess

	except sqlalchemy.exc.InternalError:
		log.warning("Transaction error (sqlalchemy.exc.InternalError). Retrying.")
		sess.rollback()
		raise
	except sqlalchemy.exc.OperationalError:
		log.warning("Transaction error (sqlalchemy.exc.OperationalError). Retrying.")
		sess.rollback()
		raise
	except sqlalchemy.exc.IntegrityError:
		log.warning("Transaction error (sqlalchemy.exc.IntegrityError). Retrying.")
		sess.rollback()
		raise
	except sqlalchemy.exc.InvalidRequestError:
		log.warning("Transaction error (sqlalchemy.exc.InvalidRequestError). Retrying.")
		traceback.print_exc()
		sess.rollback()
		raise

	finally:
		if override_timeout_ms:
			sess.execute("""RESET statement_timeout;""")
		delete_db_session(postfix='context-sess')


# import traceback
# traceback.print_stack()




