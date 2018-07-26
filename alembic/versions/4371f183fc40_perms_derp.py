"""Perms derp

Revision ID: 4371f183fc40
Revises: 7dd0f20f06d4
Create Date: 2018-07-26 05:15:08.531050

"""

# revision identifiers, used by Alembic.
revision = '4371f183fc40'
down_revision = '7dd0f20f06d4'
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

	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE raw_web_pages_version_transaction_id_seq            TO webarchuser;""")
	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE raw_web_pages_version_transaction_id_seq            TO webarchuser_scrape;""")
	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE raw_web_pages_version_transaction_id_seq            TO webarchuser_web;""")
	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE raw_web_pages_version_transaction_id_seq            TO webarchuser_sched;""")
	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE raw_web_pages_version_transaction_id_seq            TO webarchuser_raw;""")

	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE web_pages_version_transaction_id_seq                TO webarchuser;""")
	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE web_pages_version_transaction_id_seq                TO webarchuser_scrape;""")
	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE web_pages_version_transaction_id_seq                TO webarchuser_web;""")
	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE web_pages_version_transaction_id_seq                TO webarchuser_sched;""")
	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE web_pages_version_transaction_id_seq                TO webarchuser_raw;""")

	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE rss_parser_feed_name_lut_version_transaction_id_seq TO webarchuser;""")
	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE rss_parser_feed_name_lut_version_transaction_id_seq TO webarchuser_scrape;""")
	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE rss_parser_feed_name_lut_version_transaction_id_seq TO webarchuser_web;""")
	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE rss_parser_feed_name_lut_version_transaction_id_seq TO webarchuser_sched;""")
	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE rss_parser_feed_name_lut_version_transaction_id_seq TO webarchuser_raw;""")

	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE rss_parser_funcs_version_transaction_id_seq         TO webarchuser;""")
	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE rss_parser_funcs_version_transaction_id_seq         TO webarchuser_scrape;""")
	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE rss_parser_funcs_version_transaction_id_seq         TO webarchuser_web;""")
	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE rss_parser_funcs_version_transaction_id_seq         TO webarchuser_sched;""")
	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE rss_parser_funcs_version_transaction_id_seq         TO webarchuser_raw;""")

	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE rss_parser_funcs_version_transaction_id_seq         TO webarchuser;""")
	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE rss_parser_funcs_version_transaction_id_seq         TO webarchuser_scrape;""")
	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE rss_parser_funcs_version_transaction_id_seq         TO webarchuser_web;""")
	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE rss_parser_funcs_version_transaction_id_seq         TO webarchuser_sched;""")
	op.execute("""GRANT ALL PRIVILEGES ON SEQUENCE rss_parser_funcs_version_transaction_id_seq         TO webarchuser_raw;""")



def downgrade():
    pass
