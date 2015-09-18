
import os
import multiprocessing

DB_REALTIME_PRIORITY =    1 * 1000
DB_HIGH_PRIORITY     =   10 * 1000
DB_MED_PRIORITY      =   50 * 1000
DB_LOW_PRIORITY      =  100 * 1000

DB_DEFAULT_DIST      =   10 * 1000

MAX_DISTANCE         = 1000 * 1000

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table
# from sqlalchemy import MetaData

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import Text
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
# from  sqlalchemy.sql.expression import func
# from citext import CIText

# Patch in knowledge of the citext type, so it reflects properly.
from sqlalchemy.dialects.postgresql.base import ischema_names
import citext
import datetime
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import JSON
ischema_names['citext'] = citext.CIText

from settings import DATABASE_IP            as C_DATABASE_IP
from settings import DATABASE_DB_NAME       as C_DATABASE_DB_NAME
from settings import DATABASE_USER          as C_DATABASE_USER
from settings import DATABASE_PASS          as C_DATABASE_PASS

SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{passwd}@{host}:5432/{database}'.format(user=C_DATABASE_USER, passwd=C_DATABASE_PASS, host=C_DATABASE_IP, database=C_DATABASE_DB_NAME)


SESSIONS = {}
ENGINES = {}

ENGINE_LOCK = multiprocessing.Lock()
SESSION_LOCK = multiprocessing.Lock()

def get_engine():
	cpid = multiprocessing.current_process().name
	if not cpid in ENGINES:
		with ENGINE_LOCK:
			# Check if the engine was created while we were
			# waiting on the lock.
			if cpid in ENGINES:
				return ENGINES[cpid]

			print("Instantiating DB Engine")
			ENGINES[cpid] = create_engine(SQLALCHEMY_DATABASE_URI,
						isolation_level="REPEATABLE READ")

	return ENGINES[cpid]

def get_session():
	cpid = multiprocessing.current_process().name
	if not cpid in SESSIONS:
		with SESSION_LOCK:
			# check if the session was created while
			# we were waiting for the lock
			if cpid in SESSIONS:
				return SESSIONS[cpid]
			SESSIONS[cpid] = scoped_session(sessionmaker(bind=get_engine(), autoflush=False, autocommit=False))()
			print("Creating database interface:", SESSIONS[cpid])

	return SESSIONS[cpid]

def delete_session():
	cpid = multiprocessing.current_process().name
	if cpid in SESSIONS:
		with SESSION_LOCK:
			# check if the session was created while
			# we were waiting for the lock
			if not cpid in SESSIONS:
				return SESSIONS[cpid]
			del SESSIONS[cpid]
			print("Deleted session for id: ", cpid)


# import traceback
# traceback.print_stack()


Base = declarative_base()

dlstate_enum   = ENUM('new', 'fetching', 'processing', 'complete', 'error', 'removed', name='dlstate_enum')
itemtype_enum  = ENUM('western', 'eastern', 'unknown',            name='itemtype_enum')

class WebPages(Base):
	__tablename__ = 'web_pages'
	id           = Column(Integer, primary_key = True)
	state        = Column(dlstate_enum, default='new', index=True, nullable=False)
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

	title       = Column(citext.CIText)
	mimetype    = Column(Text)
	type        = Column(itemtype_enum, default='unknown', index=True)

	raw_content = Column(Text)
	content     = Column(Text)

	fetchtime   = Column(DateTime, default=datetime.datetime.min)
	addtime     = Column(DateTime, default=datetime.datetime.utcnow)


	file_item   = relationship("WebFiles")

# File table doesn't know anything about URLs, since they're kept in the
# WebPages table entirely.
class WebFiles(Base):
	__tablename__ = 'web_files'
	id           = Column(Integer, primary_key = True)
	filename     = Column(Text)

	# File hash, used for deduplicating
	fhash        = Column(Text, index = True)

	fspath       = Column(Text, nullable=False)


##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################


feed_tags_link = Table(
		'feed_tags_link', Base.metadata,
		Column('releases_id', Integer, ForeignKey('feed_pages.id'), nullable=False),
		Column('tags_id',     Integer, ForeignKey('feed_tags.id'),     nullable=False),
		PrimaryKeyConstraint('releases_id', 'tags_id')
	)

feed_author_link = Table(
		'feed_authors_link', Base.metadata,
		Column('releases_id', Integer, ForeignKey('feed_pages.id'), nullable=False),
		Column('author_id',   Integer, ForeignKey('feed_author.id'),     nullable=False),
		PrimaryKeyConstraint('releases_id', 'author_id')
	)


class Tags(Base):
	__tablename__ = 'feed_tags'
	id          = Column(Integer, primary_key=True)
	tag         = Column(citext.CIText(), nullable=False, index=True)

	__table_args__ = (
		UniqueConstraint('tag'),
		)


class Author(Base):
	__tablename__ = 'feed_author'
	id          = Column(Integer, primary_key=True)
	author      = Column(citext.CIText(), nullable=False, index=True)

	__table_args__ = (
		UniqueConstraint('author'),
		)


def tag_creator(tag):

	tmp = get_session().query(Tags)         \
		.filter(Tags.tag == tag) \
		.scalar()
	if tmp:
		return tmp

	return Tags(tag=tag)

def author_creator(author):
	tmp = get_session().query(Author)                  \
		.filter(Author.author == author) \
		.scalar()
	if tmp:
		return tmp
	return Author(author=author)


class FeedItems(Base):
	__tablename__ = 'feed_pages'

	id          = Column(Integer, primary_key=True)

	type        = Column(itemtype_enum, default='unknown', index=True)

	srcname      = Column(Text, nullable=False, index=True)
	feedurl      = Column(Text, nullable=False, index=True)
	contenturl   = Column(Text, nullable=False, index=True)
	contentid    = Column(Text, nullable=False, index=True, unique=True)

	title        = Column(Text)
	contents     = Column(Text)
	author       = Column(Text)


	updated      = Column(DateTime, default=datetime.datetime.min)
	published    = Column(DateTime, nullable=False)

	tag_rel       = relationship('Tags',       secondary=feed_tags_link,   backref='feed_pages')
	author_rel    = relationship('Author',     secondary=feed_author_link, backref='feed_pages')


	tags          = association_proxy('tag_rel',      'tag',       creator=tag_creator)
	author        = association_proxy('author_rel',   'author',    creator=author_creator)


# Tools for tracking plugins
class PluginStatus(Base):
	__tablename__ = 'plugin_status'
	id             = Column(Integer, primary_key = True)

	plugin_name    = Column(Text)

	is_running     = Column(Boolean, default=False)

	last_run       = Column(DateTime)
	last_run_end   = Column(DateTime)

	last_error     = Column(DateTime)
	last_error_msg = Column(Text)



Base.metadata.create_all(bind=get_engine(), checkfirst=True)



# More indexes:
#
# CREATE INDEX idx_web_pages_title ON web_pages USING gin(to_tsvector('english', title));
# CREATE INDEX idx_web_pages_content ON web_pages USING gin(to_tsvector('english', content));
#
# Essential for fast task get queries
# CREATE INDEX ix_web_pages_distance_filtered ON web_pages (priority ASC NULLS LAST) WHERE web_pages.state = 'new'::dlstate_enum AND web_pages.distance < 1000000;
#


# SELECT relname AS "relation", pg_size_pretty(pg_relation_size(C.oid)) AS "size"
#   FROM pg_class C LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
#   WHERE nspname NOT IN ('pg_catalog', 'information_schema')
#   ORDER BY pg_relation_size(C.oid) DESC;

# SELECT relname AS "relation",
#     pg_size_pretty(pg_total_relation_size(C.oid)) AS "total_size"
#   FROM pg_class C
#   LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
#   WHERE nspname NOT IN ('pg_catalog', 'information_schema')
#     AND C.relkind <> 'i'
#     AND nspname !~ '^pg_toast'
#   ORDER BY pg_total_relation_size(C.oid) DESC;
