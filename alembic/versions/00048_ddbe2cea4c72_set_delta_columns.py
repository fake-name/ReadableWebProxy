"""Set delta columns

Revision ID: ddbe2cea4c72
Revises: ea8987f915b8
Create Date: 2019-08-25 00:10:28.641130

"""

import tqdm
import time

# revision identifiers, used by Alembic.
revision = 'ddbe2cea4c72'
down_revision = 'ea8987f915b8'
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


def set_in_table(tablename):
	conn = op.get_bind()

	ret = conn.execute("SELECT min(id) FROM %s WHERE is_delta IS NULL;" % (tablename, ))
	(start, ),  = list(ret)
	ret = conn.execute("SELECT max(id) FROM %s WHERE is_delta IS NULL;" % (tablename, ))
	(stop, ),  = list(ret)
	print("ID Range: ", start, stop)
	if start is None:
		print("No items to set!")
		return

	step_size = 2500
	commit_every_seconds = 30
	last_commit = time.time()
	changed = 0
	changed_tot = 0
	pbar = tqdm.tqdm(range(start-1, stop+1, step_size))
	for x in pbar:
		ret = conn.execute("UPDATE %s SET is_delta=false WHERE is_delta IS NULL AND id >= %s AND id <= %s;" % (tablename, x, x+step_size+1))


		# processed  = idx - start
		# total_todo = stop - start
		desc = '(set_in_table) -> %6i, %6i, %6i' % (ret.rowcount, changed, changed_tot)
		pbar.set_description(desc)

		# print('\r%10i, %10i, %7.4f, %6i, %6i, %6i\r' % (idx, stop, processed/total_todo * 100, have.rowcount, changed, changed_tot), end="", flush=True)
		changed += ret.rowcount
		changed_tot += ret.rowcount

		if time.time() > (last_commit + commit_every_seconds):
			changed = 0
			last_commit = time.time()
			print("Incremental Commit!")
			conn.execute("COMMIT")


def upgrade():
	op.execute("SET statement_timeout TO 14400000;")

	print("Setting nulls in rss_parser_feed_name_lut_version")
	set_in_table("rss_parser_feed_name_lut_version")

	print("Setting nulls in rss_parser_funcs_version")
	set_in_table("rss_parser_funcs_version")

	print("Setting nulls in web_pages_version")
	set_in_table("web_pages_version")

	print("Setting nulls in raw_web_pages_version")
	set_in_table("raw_web_pages_version")

	raise

	print("adding nullable constraing on rss_parser_feed_name_lut_version")
	op.alter_column('rss_parser_feed_name_lut_version', 'is_delta', nullable=False)

	print("adding nullable constraing on rss_parser_funcs_version")
	op.alter_column('rss_parser_funcs_version',         'is_delta', nullable=False)

	print("adding nullable constraing on web_pages_version")
	op.alter_column('web_pages_version',                'is_delta', nullable=False)

	print("adding nullable constraing on raw_web_pages_version")
	op.alter_column('raw_web_pages_version',            'is_delta', nullable=False)
	print("Done!")

def downgrade():
	pass
