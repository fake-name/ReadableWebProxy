"""can we add autoincrement?

Revision ID: 7dd0f20f06d4
Revises: b21ea54b22a2
Create Date: 2018-07-26 04:46:09.870394

"""

# revision identifiers, used by Alembic.
revision = '7dd0f20f06d4'
down_revision = 'b21ea54b22a2'
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

# raw_web_pages_version
# web_pages_version
# rss_parser_feed_name_lut_version
# rss_parser_funcs_version

def upgrade():


	op.execute("""CREATE SEQUENCE raw_web_pages_version_transaction_id_seq OWNED BY raw_web_pages_version.transaction_id;""")
	op.execute("""SELECT setval('raw_web_pages_version_transaction_id_seq', (SELECT max(transaction_id) FROM raw_web_pages_version));""")
	op.execute("""ALTER TABLE raw_web_pages_version ALTER COLUMN transaction_id SET DEFAULT nextval('raw_web_pages_version_transaction_id_seq');""")

	op.execute("""CREATE SEQUENCE web_pages_version_transaction_id_seq OWNED BY web_pages_version.transaction_id;""")
	op.execute("""SELECT setval('web_pages_version_transaction_id_seq', (SELECT max(transaction_id) FROM web_pages_version));""")
	op.execute("""ALTER TABLE web_pages_version ALTER COLUMN transaction_id SET DEFAULT nextval('web_pages_version_transaction_id_seq');""")

	op.execute("""CREATE SEQUENCE rss_parser_feed_name_lut_version_transaction_id_seq OWNED BY rss_parser_feed_name_lut_version.transaction_id;""")
	op.execute("""SELECT setval('rss_parser_feed_name_lut_version_transaction_id_seq', (SELECT max(transaction_id) FROM rss_parser_feed_name_lut_version));""")
	op.execute("""ALTER TABLE rss_parser_feed_name_lut_version ALTER COLUMN transaction_id SET DEFAULT nextval('rss_parser_feed_name_lut_version_transaction_id_seq');""")

	op.execute("""CREATE SEQUENCE rss_parser_funcs_version_transaction_id_seq OWNED BY rss_parser_funcs_version.transaction_id;""")
	op.execute("""SELECT setval('rss_parser_funcs_version_transaction_id_seq', (SELECT max(transaction_id) FROM rss_parser_funcs_version));""")
	op.execute("""ALTER TABLE rss_parser_funcs_version ALTER COLUMN transaction_id SET DEFAULT nextval('rss_parser_funcs_version_transaction_id_seq');""")



	pass


def downgrade():
	pass
