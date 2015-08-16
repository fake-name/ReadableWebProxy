

from settings import DATABASE_IP            as C_DATABASE_IP
from settings import DATABASE_DB_NAME       as C_DATABASE_DB_NAME
from settings import DATABASE_USER          as C_DATABASE_USER
from settings import DATABASE_PASS          as C_DATABASE_PASS
from settings import SECRET_KEY             as C_SECRET_KEY
from settings import WTF_CSRF_SECRET_KEY    as C_WTF_CSRF_SECRET_KEY
from settings import SECURITY_PASSWORD_SALT as C_SECURITY_PASSWORD_SALT

from settings import RELINK_SECRET          as C_RELINK_SECRET
from settings import RESOURCE_DIR           as C_RESOURCE_DIR


from settings import RABBIT_LOGIN           as C_RABBIT_LOGIN
from settings import RABBIT_PASWD           as C_RABBIT_PASWD
from settings import RABBIT_SRVER           as C_RABBIT_SRVER
from settings import RABBIT_VHOST           as C_RABBIT_VHOST



import os
import sys
import hashlib
import datetime
if len(sys.argv) > 1 and "debug" in sys.argv:
	SQLALCHEMY_ECHO = True


REFETCH_INTERVAL = datetime.timedelta(days=7*3)
relink_secret = hashlib.sha1(C_RELINK_SECRET.encode("ascii")).hexdigest()

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):

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
	SECRET_KEY             = C_SECRET_KEY
	WTF_CSRF_SECRET_KEY    = C_WTF_CSRF_SECRET_KEY

	SECURITY_PASSWORD_SALT = C_SECURITY_PASSWORD_SALT

	RESOURCE_DIR = C_RESOURCE_DIR

