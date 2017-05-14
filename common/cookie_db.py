

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
from sqlalchemy import Index
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





class WebCookieDb(common.db_base.Base):

	__tablename__     = 'web_cookie_db'
	name              = 'web_cookie_db'

	id                = Column(Integer, primary_key = True, index = True)

	age               = Column(DateTime)

	# User agent parameters
	ua_user_agent        = Column(Text)
	ua_accept_language   = Column(Text)
	ua_accept            = Column(Text)
	ua_accept_encoding   = Column(Text)

	# Cookie members
	c_version            = Column(Integer)
	c_name               = Column(Text)
	c_value              = Column(Text)
	c_port               = Column(Integer)
	c_port_specified     = Column(Boolean)
	c_domain             = Column(Text)
	c_domain_specified   = Column(Boolean)
	c_domain_initial_dot = Column(Boolean)
	c_path               = Column(Text)
	c_path_specified     = Column(Boolean)
	c_secure             = Column(Boolean)

	# So yeah... I'm having 2038 problems. NOW.
	c_expires            = Column(BigInteger)
	c_discard            = Column(Boolean)
	c_comment            = Column(Text)
	c_comment_url        = Column(Text)
	c_rest               = Column(Text)
	c_rfc2109            = Column(Boolean)



	__table_args__ = (
		UniqueConstraint(
			'ua_user_agent',
			'ua_accept_language',
			'ua_accept',
			'ua_accept_encoding',
			'c_version',
			'c_name',
			'c_value',
			'c_port',
			'c_port_specified',
			'c_domain',
			'c_domain_specified',
			'c_domain_initial_dot',
			'c_path',
			'c_path_specified',
			'c_secure',
			'c_expires',
			'c_discard',
			'c_comment',
			'c_comment_url',
			'c_rest',
			'c_rfc2109',
			),
		Index(
			'ua_user_agent',
			'ua_accept_language',
			'ua_accept',
			'ua_accept_encoding',
			)

		)
