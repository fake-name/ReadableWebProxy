"""Add has function and dependent pgcrpyto

Revision ID: 5552dfae2cb0
Revises: c225ea8fbf5e
Create Date: 2019-09-14 06:19:36.520447

"""

# revision identifiers, used by Alembic.
revision = '5552dfae2cb0'
down_revision = 'c225ea8fbf5e'
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

# We use a UUID column because it's a performant in-table 8-byte storage mechanism with nice printing facilities.
# SHA-1 has a 160 bit output, so we need to truncate the input

SQL_FUNC = '''
CREATE OR REPLACE FUNCTION sha_row_hash(bytea) returns uuid AS $$
    SELECT substring(encode(digest($1, 'sha1'), 'hex') from 0 for 33)::uuid;
$$ LANGUAGE SQL STRICT IMMUTABLE;
'''

def upgrade():
    op.execute("""CREATE EXTENSION IF NOT EXISTS pgcrypto""")
    op.execute(SQL_FUNC)


def downgrade():
    op.execute("""DROP FUNCTION sha1;""")
    pass
