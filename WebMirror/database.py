
import os
import sys
import multiprocessing
import threading

DB_REALTIME_PRIORITY =    1 * 1000
DB_HIGH_PRIORITY     =   10 * 1000
DB_MED_PRIORITY      =   50 * 1000
DB_LOW_PRIORITY      =  100 * 1000
DB_IDLE_PRIORITY     =  500 * 1000

DB_DEFAULT_DIST      =   10 * 1000

MAX_DISTANCE         = 1000 * 1000

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table
# from sqlalchemy import MetaData

import time

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
from sqlalchemy.dialects.postgresql import TSVECTOR
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
	ctid = threading.current_thread().name
	csid = "{}-{}".format(cpid, ctid)
	if not csid in ENGINES:
		with ENGINE_LOCK:
			# Check if the engine was created while we were
			# waiting on the lock.
			if csid in ENGINES:
				return ENGINES[csid]

			print("INFO: Creating engine for process! Engine name: '%s'" % csid)
			ENGINES[csid] = create_engine(SQLALCHEMY_DATABASE_URI,
						isolation_level="REPEATABLE READ")

	return ENGINES[csid]

def get_session():
	cpid = multiprocessing.current_process().name
	ctid = threading.current_thread().name
	csid = "{}-{}".format(cpid, ctid)
	if not csid in SESSIONS:
		with SESSION_LOCK:

			# check if the session was created while
			# we were waiting for the lock
			if csid in SESSIONS:
				# Reset the "last used" time on the handle
				SESSIONS[csid][0] = time.time()
				return SESSIONS[csid][1]

			SESSIONS[csid] = [time.time(), scoped_session(sessionmaker(bind=get_engine(), autoflush=False, autocommit=False))()]
			print("Creating database interface:", SESSIONS[csid])

			# Delete the session that's oldest.
			if len(SESSIONS) > 50:
				print("WARN: More then 50 active sessions! Deleting oldest session to prevent session contention.")
				maxsz = sys.maxsize
				to_delete = None
				for key, value in SESSIONS.items():
					if value[0] < maxsz:
						to_delete = key
						maxsz = value[0]
				if to_delete:
					del SESSIONS[to_delete]

	# Reset the "last used" time on the handle
	SESSIONS[csid][0] = time.time()
	return SESSIONS[csid][1]

def delete_session():
	cpid = multiprocessing.current_process().name
	ctid = threading.current_thread().name
	csid = "{}-{}".format(cpid, ctid)
	if csid in SESSIONS:
		with SESSION_LOCK:
			# check if the session was created while
			# we were waiting for the lock
			if not csid in SESSIONS:
				return SESSIONS[csid]
			del SESSIONS[csid]
			print("Deleted session for id: ", csid)


# import traceback
# traceback.print_stack()


Base = declarative_base()

dlstate_enum   = ENUM('new', 'fetching', 'processing', 'complete', 'error', 'removed', name='dlstate_enum')
itemtype_enum  = ENUM('western', 'eastern', 'unknown',            name='itemtype_enum')

class WebPages(Base):
	__tablename__ = 'web_pages'
	id                = Column(Integer, primary_key = True)
	state             = Column(dlstate_enum, default='new', index=True, nullable=False)
	errno             = Column(Integer, default='0')
	url               = Column(Text, nullable = False, index = True, unique = True)
	starturl          = Column(Text, nullable = False)
	netloc            = Column(Text, nullable = False)

	# Foreign key to the files table if needed.
	file              = Column(Integer, ForeignKey('web_files.id'))

	priority          = Column(Integer, default=1000000, index=True, nullable=False)
	distance          = Column(Integer, index=True, nullable=False)

	is_text           = Column(Boolean, default=False)
	limit_netloc      = Column(Boolean, default=True)

	title             = Column(citext.CIText)
	mimetype          = Column(Text)
	type              = Column(itemtype_enum, default='unknown', index=True)

	# Disabled due to disk-space issues.
	# raw_content       = Column(Text)

	content           = Column(Text)

	fetchtime         = Column(DateTime, default=datetime.datetime.min)
	addtime           = Column(DateTime, default=datetime.datetime.utcnow)

	ignoreuntiltime   = Column(DateTime, default=datetime.datetime.min, index=True, nullable=False)

	# Items with `normal_fetch_mode` set to false are not retreived by the normal scheduling system
	# in WebMirror\Engine.py. This is to allow external systems that need to manage their own
	# fetch scheduling to operate within the same database.
	normal_fetch_mode = Column(Boolean, default=True)

	tsv_content       = Column(TSVECTOR)


	file_item         = relationship("WebFiles")

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

	tmp = get_session().query(Tags) \
		.filter(Tags.tag == tag)    \
		.scalar()
	if tmp:
		return tmp

	return Tags(tag=tag)

def author_creator(author):
	tmp = get_session().query(Author)    \
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


# CREATE INDEX
#     ix_web_pages_distance_filtered_nowp
# ON
#     web_pages(priority)
# WHERE
#     state = 'new'::dlstate_enum
# AND
#     distance < 1000000
# AND
#     normal_fetch_mode = true
# AND NOT
#     (
#             web_pages.netloc = 'a.wattpad.com'
#         OR
#             web_pages.netloc = 'www.wattpad.com'
#     );

# CREATE INDEX
#     ix_web_pages_distance_filtered_wp
# ON
#     web_pages(priority)
# WHERE
#     state = 'new'::dlstate_enum
# AND
#     distance < 1000000
# AND
#     normal_fetch_mode = true
# AND  (
#             web_pages.netloc = 'a.wattpad.com'
#         OR
#             web_pages.netloc = 'www.wattpad.com'
#     );


# EXPLAIN ANALYZE UPDATE web_pages SET fetchtime='now'::timestamp WHERE id=428615139;
# EXPLAIN ANALYZE UPDATE web_pages SET tsv_content = NULL WHERE id=428615139;

# SELECT  tsv_content FROM web_pages WHERE id=428615139;

'''
CREATE OR REPLACE FUNCTION web_pages_content_update_func() RETURNS TRIGGER AS $_$
BEGIN
    --
    -- Create a row in {name}changes to reflect the operation performed on emp,
    -- make use of the special variable TG_OP to work out the operation.
    --
    IF TG_OP = 'INSERT' THEN
        IF NEW.content IS NOT NULL THEN
            NEW.tsv_content = to_tsvector(coalesce(NEW.content));
        END IF;
    ELSEIF TG_OP = 'UPDATE' THEN
        IF NEW.content != OLD.content THEN
            NEW.tsv_content = to_tsvector(coalesce(NEW.content));
        END IF;
    END IF;
    RETURN NEW;
END $_$ LANGUAGE 'plpgsql';


CREATE TRIGGER
    update_row_count_trigger
BEFORE INSERT OR UPDATE ON
    web_pages
FOR EACH ROW EXECUTE PROCEDURE
    web_pages_content_update_func();
'''

