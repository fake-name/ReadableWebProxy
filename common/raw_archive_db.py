

from sqlalchemy import Table

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import Text
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
# from  sqlalchemy.sql.expression import func
# from citext import CIText

from sqlalchemy_utils.types import TSVectorType

import citext
import datetime
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import TSVECTOR


import common.db_base
import common.db_types



class RawWebPages(common.db_base.Base):
	__versioned__ = {}

	__tablename__     = 'raw_web_pages'
	name              = 'raw_web_pages'

	id                = Column(Integer, primary_key = True, index = True)
	state             = Column(common.db_types.dlstate_enum, default='new', index=True, nullable=False)
	errno             = Column(Integer, default='0')
	url               = Column(Text, nullable = False, index = True, unique = True)
	starturl          = Column(Text, nullable = False)
	netloc            = Column(Text, nullable = False, index = True)

	priority          = Column(Integer, default=1000000, index=True, nullable=False)
	distance          = Column(Integer, index=True, nullable=False)

	is_text           = Column(Boolean, default=False)

	mimetype          = Column(Text)

	# Disabled due to disk-space issues.
	# raw_content       = Column(Text)

	filename     = Column(Text)

	fspath       = Column(Text, nullable=False)

	fetchtime         = Column(DateTime, default=datetime.datetime.min)
	addtime           = Column(DateTime, default=datetime.datetime.utcnow)

	ignoreuntiltime   = Column(DateTime, default=datetime.datetime.min, nullable=False)


