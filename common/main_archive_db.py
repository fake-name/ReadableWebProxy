

from sqlalchemy import Table

from sqlalchemy import Column
from sqlalchemy import BigInteger
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from sqlalchemy.ext.associationproxy import association_proxy
# from  sqlalchemy.sql.expression import func
# from citext import CIText

import citext
import datetime
from sqlalchemy.dialects.postgresql import ENUM


import common.db_base
import common.db_types

from common.db_engine import get_db_session
from common.db_engine import delete_db_session

class WebPages(common.db_base.Base):
	__versioned__ = {}

	__tablename__ = 'web_pages'
	name = 'web_pages'

	id                = Column(BigInteger, primary_key = True, index = True)
	state             = Column(common.db_types.dlstate_enum, default='new', index=True, nullable=False)
	errno             = Column(Integer, default='0')
	url               = Column(Text, nullable = False, index = True, unique = True)
	starturl          = Column(Text, nullable = False)
	netloc            = Column(Text, nullable = False, index = True)

	# Foreign key to the files table if needed.
	file              = Column(BigInteger, ForeignKey('web_files.id'))

	priority          = Column(Integer, default=1000000, index=True, nullable=False)
	distance          = Column(Integer, index=True, nullable=False)

	is_text           = Column(Boolean, default=False)
	limit_netloc      = Column(Boolean, default=True)

	title             = Column(citext.CIText)
	mimetype          = Column(Text)
	type              = Column(common.db_types.itemtype_enum, default='unknown')

	# Disabled due to disk-space issues.
	# raw_content       = Column(Text)

	content           = Column(Text)

	fetchtime         = Column(DateTime, default=datetime.datetime.min, index=True)
	addtime           = Column(DateTime, default=datetime.datetime.utcnow)

	ignoreuntiltime   = Column(DateTime, default=datetime.datetime.min, nullable=False)

	# Items with `normal_fetch_mode` set to false are not retreived by the normal scheduling system
	# in WebMirror\Engine.py. This is to allow external systems that need to manage their own
	# fetch scheduling to operate within the same database.
	normal_fetch_mode = Column(Boolean, default=True)


	file_item         = relationship("WebFiles")

# File table doesn't know anything about URLs, since they're kept in the
# WebPages table entirely.
class WebFiles(common.db_base.Base):
	__tablename__ = 'web_files'
	id           = Column(BigInteger, primary_key = True)
	filename     = Column(Text)

	# File hash, used for deduplicating
	fhash        = Column(Text, index = True)

	fspath       = Column(Text, nullable=False)


##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################


feed_tags_link = Table(
		'feed_tags_link', common.db_base.Base.metadata,
		Column('releases_id', BigInteger, ForeignKey('feed_pages.id'), nullable=False),
		Column('tags_id',     BigInteger, ForeignKey('feed_tags.id'),     nullable=False),
		PrimaryKeyConstraint('releases_id', 'tags_id')
	)

feed_author_link = Table(
		'feed_authors_link', common.db_base.Base.metadata,
		Column('releases_id', BigInteger, ForeignKey('feed_pages.id'), nullable=False),
		Column('author_id',   BigInteger, ForeignKey('feed_author.id'),     nullable=False),
		PrimaryKeyConstraint('releases_id', 'author_id')
	)


class Tags(common.db_base.Base):
	__tablename__ = 'feed_tags'
	id          = Column(BigInteger, primary_key=True)
	tag         = Column(citext.CIText(), nullable=False, index=True)

	__table_args__ = (
		UniqueConstraint('tag'),
		)


class Author(common.db_base.Base):
	__tablename__ = 'feed_author'
	id          = Column(BigInteger, primary_key=True)
	author      = Column(citext.CIText(), nullable=False, index=True)

	__table_args__ = (
		UniqueConstraint('author'),
		)


def tag_creator(tag):

	tmp = get_db_session().query(Tags) \
		.filter(Tags.tag == tag)    \
		.scalar()
	if tmp:
		return tmp

	return Tags(tag=tag)

def author_creator(author):
	tmp = get_db_session().query(Author)    \
		.filter(Author.author == author) \
		.scalar()
	if tmp:
		return tmp
	return Author(author=author)


class FeedItems(common.db_base.Base):
	__tablename__ = 'feed_pages'

	id          = Column(BigInteger, primary_key=True)

	type        = Column(common.db_types.itemtype_enum, default='unknown', index=True)

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
class PluginStatus(common.db_base.Base):
	__tablename__ = 'plugin_status'
	id             = Column(BigInteger, primary_key = True)

	plugin_name    = Column(Text)

	is_running     = Column(Boolean, default=False)

	last_run       = Column(DateTime)
	last_run_end   = Column(DateTime)

	last_error     = Column(DateTime)
	last_error_msg = Column(Text)



# 'seriesname'       : series.get_text().strip(),
# 'releaseinfo'      : release.get_text().strip(),
# 'groupinfo'        : group.get_text().strip(),
# 'referrer'         : currentUrl,
# 'outbound_wrapper' : release.find('a', class_='chp-release')['href'],
# 'actual_target'    : None,

# 'client_id'        : self.settings['clientid'],
# 'client_key'       : self.settings['client_key'],

# Tools for tracking plugins
class NuOutboundWrapperMap(common.db_base.Base):
	__tablename__ = 'nu_outbound_wrappers'
	id               = Column(BigInteger, primary_key = True)

	client_id        = Column(Text, index=True)
	client_key       = Column(Text, index=True)

	seriesname       = Column(Text, index=True)
	releaseinfo      = Column(Text)
	groupinfo        = Column(Text, index=True)
	referrer         = Column(Text)
	outbound_wrapper = Column(Text)
	actual_target    = Column(Text)

	released_on      = Column(DateTime, default=datetime.datetime.utcnow)

	validated        = Column(Boolean, default=False)


	__table_args__ = (
		UniqueConstraint('client_id', 'client_key', 'seriesname', 'releaseinfo', 'groupinfo', 'actual_target'),
		)


# common.db_base.Base.metadata.create_all(bind=get_engine(), checkfirst=True)



# More indexes:
#
# CREATE INDEX idx_web_pages_title ON web_pages USING gin(to_tsvector('english', title));
# CREATE INDEX idx_web_pages_content ON web_pages USING gin(to_tsvector('english', content));
#
# Essential for fast task get queries
# CREATE INDEX ix_web_pages_distance_filtered ON web_pages (priority ASC NULLS LAST) WHERE web_pages.state = 'new'::dlstate_enum AND web_pages.distance < 1000000;
# CREATE INDEX ix_web_pages_distance_filtered_2 ON web_pages (priority ASC NULLS LAST, distance, normal_fetch_mode, ignoreuntiltime) WHERE web_pages.state = 'new'::dlstate_enum AND web_pages.distance < 1000000;
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




DELETE FROM
    web_pages_version
WHERE
    url
IN
(
    SELECT
        url
    FROM
        web_pages_version
    GROUP BY
        url HAVING COUNT(url) > 1000
)


EXPLAIN
SELECT
    count(*), url
FROM
    web_pages_version
GROUP BY
    url
HAVING
    COUNT(*) > 1
ORDER BY
    COUNT(*) DESC
;

SELECT pg_terminate_backend(pid)
  FROM pg_stat_activity
 WHERE  usename='webarchuser';


'''

