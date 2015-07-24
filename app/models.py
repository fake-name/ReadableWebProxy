
# import rpc

DB_REALTIME_PRIORITY =   1 * 1000
DB_HIGH_PRIORITY     =  10 * 1000
DB_MED_PRIORITY      =  50 * 1000
DB_LOW_PRIORITY      = 100 * 1000

DB_DEFAULT_DIST      =  10 * 1000

# import task_exceptions
# import deps.ExContentLoader
# import deps.ContentLoader
# import deps.LibraryContentEnqueue
# import deps.LibraryContentEnqueue
# import deps.ExExtract
# import deps.nameTools as nt
# import os.path
# import traceback
# import string
# import settings
# import time
# import pprint
# import traceback
import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

# from  sqlalchemy.sql.expression import func
# from citext import CIText

from sqlalchemy.dialects.postgresql import ENUM

from app import db


dlstate_enum  = ENUM('new', 'fetching', 'processing', 'complete', 'error', 'removed', name='dlstate_enum')
itemtype_enum  = ENUM('western', 'eastern', 'unknown',            name='itemtype_enum')

class WebPages(db.Model):
	__tablename__ = 'web_pages'
	id           = Column(Integer, primary_key = True)
	state        = Column(dlstate_enum, default='new', index=True)
	errno        = Column(Integer, default='0')
	url          = Column(Text, nullable = False, index = True, unique = True)
	starturl     = Column(Text, nullable = False)
	netloc       = Column(Text, nullable = False)

	# Foreign key to the files table if needed.
	file         = Column(Integer, ForeignKey('web_files.id'))

	priority     = Column(Integer, default=1000000, index=True, nullable=False)
	distance     = Column(Integer, index=True, nullable=False)

	is_text      = Column(Boolean, default=False)
	limit_netloc = Column(Boolean, default=True)

	title       = Column(Text)
	mimetype    = Column(Text)
	type        = Column(itemtype_enum, default='unknown', index=True)

	raw_content = Column(Text)
	content     = Column(Text)

	fetchtime   = Column(DateTime, default=datetime.datetime.min)
	addtime     = Column(DateTime, default=datetime.datetime.utcnow)



# File table doesn't know anything about URLs, since they're kept in the
# WebPages table entirely.
class WebFiles(db.Model):
	__tablename__ = 'web_files'
	id           = Column(Integer, primary_key = True)
	filename     = Column(Text)

	# File hash, used for deduplicating
	fhash        = Column(Text, index = True)

	fspath       = Column(Text, nullable=False)







