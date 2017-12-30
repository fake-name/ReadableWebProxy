
import settings

# Patch in knowledge of the citext type, so it reflects properly.
from sqlalchemy.dialects.postgresql.base import ischema_names
import citext
ischema_names['citext'] = citext.CIText

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()