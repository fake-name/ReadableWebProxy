"""RSS moar columns

Revision ID: 1dc0fe0d793f
Revises: 3389071120cb
Create Date: 2017-02-28 06:49:26.443860

"""

# revision identifiers, used by Alembic.
revision = '1dc0fe0d793f'
down_revision = '3389071120cb'
branch_labels = None
depends_on = None


# Patch in knowledge of the citext type, so it reflects properly.
import citext
from sqlalchemy.dialects.postgresql.base import ischema_names
ischema_names['citext'] = citext.CIText

from sqlalchemy.dialects import postgresql

import sqlalchemy as sa
import sqlalchemy_utils
import urllib.parse


from alembic import op
from flask_sqlalchemy import _SessionSignalEvents
import sqlalchemy as sa
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session as BaseSession, relationship
from sqlalchemy.orm import joinedload


from sqlalchemy import Table

from sqlalchemy import Column
from sqlalchemy import BigInteger
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint


Session = sessionmaker()

Base = declarative_base()





class RssFeedPost(Base):
	__tablename__ = 'feed_pages'

	id          = Column(BigInteger, primary_key=True)

	feed_id     = Column(BigInteger, ForeignKey('rss_parser_funcs.id'), index = True, nullable=False)

	srcname      = Column(Text, nullable=False, index=True)

	feedurl      = Column(Text, nullable=False, index=True)


class RssFeedUrlMapper(Base):
	__versioned__ = {}

	__tablename__     = 'rss_parser_feed_name_lut'
	name              = 'rss_parser_feed_name_lut'

	id                = Column(BigInteger, primary_key = True, index = True)
	feed_netloc       = Column(Text, nullable = False, index = True)
	feed_url          = Column(Text, nullable = False, index = True)
	feed_id           = Column(BigInteger, ForeignKey('rss_parser_funcs.id'), nullable = False, index = True)

	__table_args__ = (
		UniqueConstraint('feed_netloc', 'feed_id'),
		)

class RssFeedEntry(Base):
	__versioned__ = {}

	__tablename__     = 'rss_parser_funcs'
	name              = 'rss_parser_funcs'

	id                = Column(BigInteger, primary_key = True, index = True)
	version           = Column(Integer, default='0')

	feed_name         = Column(Text, nullable = False, index = True, unique = True)

	enabled           = Column(Boolean, default=True)

	func              = Column(Text)

	urls              = relationship('RssFeedUrlMapper', backref='rss_parser_funcs')
	releases          = relationship('RssFeedPost',      backref='rss_parser_funcs')



