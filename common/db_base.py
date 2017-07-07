
import settings

if settings.DO_VERSIONING:
	from sqlalchemy_continuum import make_versioned
	make_versioned(user_cls=None)


# Patch in knowledge of the citext type, so it reflects properly.
from sqlalchemy.dialects.postgresql.base import ischema_names
import citext
ischema_names['citext'] = citext.CIText

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_searchable import make_searchable

Base = declarative_base()
make_searchable()
