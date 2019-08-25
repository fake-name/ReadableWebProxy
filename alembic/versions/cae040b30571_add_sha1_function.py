"""Add sha1 function

Revision ID: cae040b30571
Revises: ddbe2cea4c72
Create Date: 2019-08-25 04:13:54.565994

"""

# revision identifiers, used by Alembic.
revision = 'cae040b30571'
down_revision = 'ddbe2cea4c72'
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

SQL_FUNC = '''
CREATE OR REPLACE FUNCTION sha1(bytea) returns text AS $$
    SELECT encode(digest($1, 'sha1'), 'hex')
$$ LANGUAGE SQL STRICT IMMUTABLE;
'''

def upgrade():
    op.execute(SQL_FUNC)


def downgrade():
    op.execute("""DROP FUNCTION sha1;""")
    pass
