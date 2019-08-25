"""empty message

Revision ID: 9b782438e315
Revises: 53fab90468f4
Create Date: 2018-01-03 05:48:35.565450

"""

# revision identifiers, used by Alembic.
revision = '9b782438e315'
down_revision = '53fab90468f4'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable
import sqlalchemy_utils

# Patch in knowledge of the citext type, so it reflects properly.
from sqlalchemy.dialects.postgresql.base import ischema_names
import citext
import queue
import datetime
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import TSVECTOR
ischema_names['citext'] = citext.CIText



from alembic import op
from flask_sqlalchemy import _SessionSignalEvents
import sqlalchemy as sa
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session as BaseSession, relationship


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


class NuReleaseItem(Base):
	__tablename__ = 'nu_release_item'
	id               = Column(BigInteger, primary_key=True)

	release_date     = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
	first_seen       = Column(DateTime, nullable=False, default=datetime.datetime.min)


def upgrade():
	bind = op.get_bind()
	sess = Session(bind=bind)
	print("Adding column")
	op.add_column('nu_release_item', sa.Column('release_date', sa.DateTime()))

	print("Setting value for new column")
	sess.query(NuReleaseItem).update({"first_seen" : datetime.datetime.min})
	sess.commit()

	print("Setting nullability")
	op.alter_column('nu_release_item', 'first_seen',
			   existing_type=sa.DateTime(),
			   nullable=False)

	### end Alembic commands ###


def downgrade():
	op.drop_column('nu_release_item', 'release_date')
	### end Alembic commands ###
