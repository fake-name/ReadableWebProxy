

import os
import sys
import hashlib
import datetime

import string
import random

try:

	from settings import DATABASE_IP            as C_DATABASE_IP
	from settings import DATABASE_DB_NAME       as C_DATABASE_DB_NAME
	from settings import DATABASE_USER          as C_DATABASE_USER
	from settings import DATABASE_PASS          as C_DATABASE_PASS

	from settings import RELINK_SECRET          as C_RELINK_SECRET
	from settings import RESOURCE_DIR           as C_RESOURCE_DIR
	from settings import RESOURCE_DIR_2         as C_RESOURCE_DIR_2
	from settings import RABBIT_ENABLED         as C_DO_RABBIT


	from settings import RABBIT_LOGIN           as C_RABBIT_LOGIN
	from settings import RABBIT_PASWD           as C_RABBIT_PASWD
	from settings import RABBIT_SRVER           as C_RABBIT_SRVER
	from settings import RABBIT_VHOST           as C_RABBIT_VHOST

	from settings import RPC_AGENT_HOST         as C_RPC_AGENT_HOST
	from settings import SYNC_RPC_SERVER        as C_SYNC_RPC_SERVER
	from settings import DO_VERSIONING          as C_DO_VERSIONING
	from settings import MAX_DB_SESSIONS        as C_MAX_DB_SESSIONS

	from settings import RAW_RESOURCE_DIR       as C_RAW_RESOURCE_DIR
	from settings import REDIS_SERVER_IP        as C_REDIS_SERVER_IP

	from settings import GRAPHITE_DB_IP         as C_GRAPHITE_DB_IP
	from settings import INFLUX_DB_URL          as C_INFLUX_DB_URL
	from settings import INFLUX_DB_PORT         as C_INFLUX_DB_PORT
	from settings import INFLUX_DB_DBNAME       as C_INFLUX_DB_DBNAME
	relink_secret = hashlib.sha1(C_RELINK_SECRET.encode("ascii")).hexdigest()

except ImportError:
	print("Running with No config!")
	C_DATABASE_IP      = None
	C_DATABASE_DB_NAME = None
	C_DATABASE_USER    = None
	C_DATABASE_PASS    = None
	C_RELINK_SECRET    = None
	C_RESOURCE_DIR     = None
	C_RESOURCE_DIR_2   = None
	C_DO_RABBIT        = None
	C_RABBIT_LOGIN     = None
	C_RABBIT_PASWD     = None
	C_RABBIT_SRVER     = None
	C_RABBIT_VHOST     = None
	C_RAW_RESOURCE_DIR = None
	C_RPC_AGENT_HOST   = None
	C_SYNC_RPC_SERVER  = None
	C_DO_VERSIONING    = None
	C_MAX_DB_SESSIONS  = None
	C_REDIS_SERVER_IP  = None

	C_GRAPHITE_DB_IP   = None
	C_INFLUX_DB_URL    = None
	C_INFLUX_DB_PORT   = None
	C_INFLUX_DB_DBNAME = None


	relink_secret      = None

random.seed()

if len(sys.argv) > 1 and "debug" in sys.argv:
	SQLALCHEMY_ECHO = True


REFETCH_INTERVAL = datetime.timedelta(days=7*3)

basedir = os.path.abspath(os.path.dirname(__file__))

def get_random(chars):
	rand = [random.choice(string.ascii_letters) for x in range(chars)]
	rand = "".join(rand)
	return rand


class BaseConfig():

	SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{passwd}@{host}:5432/{database}'.format(user=C_DATABASE_USER, passwd=C_DATABASE_PASS, host=C_DATABASE_IP, database=C_DATABASE_DB_NAME)
	SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

	CSRF_ENABLED = True
	WTF_CSRF_ENABLED = True


	# administrator list
	ADMINS = ['you@example.com']

	# slow database query threshold (in seconds)
	DATABASE_QUERY_TIMEOUT = 0.5

	SEND_FILE_MAX_AGE_DEFAULT = 60*60*12

	# pagination
	TAGS_PER_PAGE = 50
	GENRES_PER_PAGE = 50
	SERIES_PER_PAGE = 50

	POSTS_PER_PAGE = 50
	MAX_SEARCH_RESULTS = 50

	FEED_ITEMS_PER_PAGE = 150

	DATABASE_IP            = C_DATABASE_IP
	DATABASE_DB_NAME       = C_DATABASE_DB_NAME
	DATABASE_USER          = C_DATABASE_USER
	DATABASE_PASS          = C_DATABASE_PASS


	RESOURCE_DIR   = C_RESOURCE_DIR
	RESOURCE_DIR_2 = C_RESOURCE_DIR_2

	# The WTF protection doesn't have to persist across
	# execution sessions, since that'll break any
	# active sessions anyways. Therefore, just generate
	# them randomly at each start.
	SECRET_KEY             = get_random(20)
	WTF_CSRF_SECRET_KEY    = get_random(20)

