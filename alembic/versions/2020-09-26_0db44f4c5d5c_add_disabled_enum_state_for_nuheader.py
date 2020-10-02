"""Add disabled enum state for nuheader

Revision ID: 0db44f4c5d5c
Revises: 8b536bc5d716
Create Date: 2020-09-26 02:21:05.973187

"""

# revision identifiers, used by Alembic.
revision = '0db44f4c5d5c'
down_revision = '8b536bc5d716'
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
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import TSVECTOR
ischema_names['citext'] = citext.CIText



def upgrade():
    op.execute("COMMIT")
    op.execute("ALTER TYPE nu_item_enum ADD VALUE 'disabled';")


def downgrade():
    pass
