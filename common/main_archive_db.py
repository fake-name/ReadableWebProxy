

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


##################################################

class NuReleaseItem(common.db_base.Base):
	__tablename__ = 'nu_release_item'
	id               = Column(BigInteger, primary_key=True)

	validated        = Column(Boolean, default=False, nullable=False, index=True)
	reviewed         = Column(common.db_types.nu_item_enum, default='unverified', nullable=False, index=True)

	actual_target    = Column(Text)

	seriesname       = Column(Text, nullable=False, index=True)
	releaseinfo      = Column(Text)
	groupinfo        = Column(Text, nullable=False, index=True)
	referrer         = Column(Text, nullable=False)
	outbound_wrapper = Column(Text, nullable=False, unique=True)

	release_date     = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
	first_seen       = Column(DateTime, nullable=False, default=datetime.datetime.min)
	validated_on     = Column(DateTime, index=True)

	fetch_attempts   = Column(Integer,  index=True, default=0, nullable=False)

	resolved         = relationship("NuResolvedOutbound")

	__table_args__ = (
		UniqueConstraint('seriesname', 'releaseinfo', 'groupinfo', 'outbound_wrapper'),
		)

class NuResolvedOutbound(common.db_base.Base):
	__tablename__ = 'nu_resolved_outbound'
	id               = Column(BigInteger, primary_key=True)

	# Foreign key to the files table if needed.
	parent           = Column(BigInteger, ForeignKey('nu_release_item.id'), index=True, nullable=False)

	client_id        = Column(Text, nullable=False, index=True)
	client_key       = Column(Text, nullable=False, index=True)

	actual_target    = Column(Text, nullable=False)
	resolved_title   = Column(Text)

	fetched_on       = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

	# disabled         = Column(Boolean)

	__table_args__ = (
		UniqueConstraint('parent', 'client_id', 'client_key', 'actual_target'),
		)


# 'seriesname'       : series.get_text().strip(),
# 'releaseinfo'      : release.get_text().strip(),
# 'groupinfo'        : group.get_text().strip(),
# 'referrer'         : currentUrl,
# 'outbound_wrapper' : release.find('a', class_='chp-release')['href'],
# 'actual_target'    : None,

# 'client_id'        : self.settings['clientid'],
# 'client_key'       : self.settings['client_key'],

# # Tools for tracking plugins
# class NuOutboundWrapperMap(common.db_base.Base):
# 	__tablename__ = 'nu_outbound_wrappers'
# 	id               = Column(BigInteger, primary_key = True)

# 	client_id        = Column(Text, index=True)
# 	client_key       = Column(Text, index=True)

# 	seriesname       = Column(Text, index=True)
# 	releaseinfo      = Column(Text)
# 	groupinfo        = Column(Text, index=True)
# 	referrer         = Column(Text)
# 	outbound_wrapper = Column(Text)
# 	actual_target    = Column(Text)

# 	released_on      = Column(DateTime, default=datetime.datetime.utcnow, index=True)

# 	validated        = Column(Boolean, default=False)


# 	__table_args__ = (
# 		UniqueConstraint('client_id', 'client_key', 'seriesname', 'releaseinfo', 'groupinfo', 'actual_target'),
# 		)


# common.db_base.Base.metadata.create_all(bind=get_engine(), checkfirst=True)


