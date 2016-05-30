
import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from sqlalchemy import MetaData


import sqlalchemy as sa

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import DateTime


SQLALCHEMY_DATABASE_URI = 'sqlite:///linkwrappers.db'


engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Base = declarative_base()

class LinkWrappers(Base):

	__tablename__ = 'link_wrappers'

	id                = Column(Integer, primary_key = True, index = True)
	seriesname        = Column(Text, index = True, nullable = False)
	releaseinfo       = Column(Text, index = True, nullable = False)
	groupinfo         = Column(Text, index = True, nullable = False)
	referrer          = Column(Text, index = True, nullable = False)

	outbound_wrapper  = Column(Text, index = True, nullable = False)
	actual_target     = Column(Text, index = True)

	addtime           = Column(DateTime, default=datetime.datetime.utcnow)

sa.orm.configure_mappers()
Base.metadata.create_all(bind=engine, checkfirst=True)

# Construct a sessionmaker object
session = sessionmaker()

# Bind the sessionmaker to engine
session.configure(bind=engine)