"""Add manual validate enum state for nuheader

Revision ID: 47d2fbfacf1b
Revises: 0db44f4c5d5c
Create Date: 2020-10-02 09:57:32.225254

"""

# revision identifiers, used by Alembic.
revision = '47d2fbfacf1b'
down_revision = '0db44f4c5d5c'
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
    op.execute("ALTER TYPE nu_item_enum ADD VALUE 'manual_validate';")


def downgrade():
    pass
