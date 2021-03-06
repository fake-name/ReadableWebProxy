"""Adding table for tracking when versioning items were flattened

Revision ID: b21ea54b22a2
Revises: 49308bd51717
Create Date: 2018-07-07 07:44:47.984194

"""

# revision identifiers, used by Alembic.
revision = 'b21ea54b22a2'
down_revision = '49308bd51717'
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
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('version_checked_table',
    sa.Column('url', sa.Text(), nullable=False),
    sa.Column('checked', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('url')
    )
    op.create_index(op.f('ix_version_checked_table_checked'), 'version_checked_table', ['checked'], unique=False)
    op.create_index(op.f('ix_version_checked_table_url'), 'version_checked_table', ['url'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_version_checked_table_url'), table_name='version_checked_table')
    op.drop_index(op.f('ix_version_checked_table_checked'), table_name='version_checked_table')
    op.drop_table('version_checked_table')
    # ### end Alembic commands ###
