"""Hash table rows

Revision ID: b5a43cfd5967
Revises: 5552dfae2cb0
Create Date: 2019-09-14 06:42:03.399675

"""


# revision identifiers, used by Alembic.
revision = 'b5a43cfd5967'
down_revision = '5552dfae2cb0'
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
import time
import tqdm
import queue
import datetime
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import TSVECTOR
ischema_names['citext'] = citext.CIText


# Gah, so I got the function input type wrong
SQL_FUNC = '''
CREATE OR REPLACE FUNCTION sha_row_hash(bigint, bigint, text) returns uuid AS $$
    SELECT substring(
            encode(
                digest(
                    $1::text || ' ' || $2::text || ' ' || $3,
                'sha1'),
            'hex')
        from 0 for 33)::uuid;
$$ LANGUAGE SQL STRICT IMMUTABLE;
'''



def set_in_table(tablename):
	conn = op.get_bind()

	ret = conn.execute("SELECT min(id), max(id) FROM %s;" % (tablename, ))
	start, stop = list(ret)[0]
	print("Total Range: ", start, stop)

	# ret = conn.execute("SELECT min(id) FROM %s WHERE is_delta IS NULL;" % (tablename, ))
	# start, = list(ret)[0]
	# print("Got start range: ", start)
	# if start is None:
	# 	print("No items to set!")
	# 	return
	# ret = conn.execute("SELECT max(id) FROM %s WHERE is_delta IS NULL;" % (tablename, ))
	# stop, = list(ret)[0]
	# print("ID Range: ", start, stop)
	# if start is None:
	# 	print("No items to set!")
	# 	return



	# start, stop = 2062433413, 8023669082


	step_size = 10
	commit_every_seconds = 30
	last_commit = time.time()
	changed = 0
	changed_tot = 0
	pbar = tqdm.tqdm(range(start-1, stop+1, step_size))
	for x in pbar:
		ret = conn.execute("UPDATE %s SET data_hash=sha_row_hash(id, transaction_id, content) WHERE (content IS NOT NULL AND data_hash IS NULL AND id >= %s AND id <= %s);" % (tablename, x, x+step_size+1))
		rete = ret.rowcount
		# print(rete)
		# processed  = idx - start
		# total_todo = stop - start
		desc = '(set_in_table) -> %6i, %6i, %6i, %10i' % (ret.rowcount, changed, changed_tot, x)
		pbar.set_description(desc)

		# print('\r%10i, %10i, %7.4f, %6i, %6i, %6i\r' % (idx, stop, processed/total_todo * 100, have.rowcount, changed, changed_tot), end="", flush=True)
		changed += rete
		changed_tot += rete

		if time.time() > (last_commit + commit_every_seconds):
			changed = 0
			last_commit = time.time()
			print("Incremental Commit!")
			conn.execute("COMMIT;")


def upgrade():
	op.execute("SET statement_timeout TO 144000000;")

	op.execute('''DROP FUNCTION IF EXISTS sha_row_hash''')
	op.execute(SQL_FUNC)


	print("Setting nulls in web_pages_version")
	set_in_table("web_pages_version")

	print("Done!")

def downgrade():
	pass
