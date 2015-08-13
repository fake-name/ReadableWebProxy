
# import rpc

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
ischema_names['citext'] = citext.CIText

from settings import DATABASE_IP            as C_DATABASE_IP
from settings import DATABASE_DB_NAME       as C_DATABASE_DB_NAME
from settings import DATABASE_USER          as C_DATABASE_USER
from settings import DATABASE_PASS          as C_DATABASE_PASS

SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{passwd}@{host}:5432/{database}'.format(user=C_DATABASE_USER, passwd=C_DATABASE_PASS, host=C_DATABASE_IP, database=C_DATABASE_DB_NAME)


engine = create_engine(SQLALCHEMY_DATABASE_URI,
			isolation_level="REPEATABLE READ")

session = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))()
print("Creating database interface:", session)
Base = declarative_base()

dlstate_enum  = ENUM('new', 'fetching', 'processing', 'complete', 'error', 'removed', name='dlstate_enum')
itemtype_enum  = ENUM('western', 'eastern', 'unknown',            name='itemtype_enum')

class WebPages(Base):
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




Base.metadata.create_all(bind=engine, checkfirst=True)



