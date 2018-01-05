
import calendar
import datetime
import json
import os
import os.path
import shutil
import traceback
from concurrent.futures import ThreadPoolExecutor

import urllib.error
import urllib.parse

from sqlalchemy import and_
from sqlalchemy import or_
import sqlalchemy.exc
from sqlalchemy_continuum.utils import version_table

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import common.database as db
import common.Exceptions
import common.management.file_cleanup

import Misc.HistoryAggregator.Consolidate

import flags
import pprint
import config
from config import C_RAW_RESOURCE_DIR

import WebMirror.OutputFilters.rss.FeedDataParser



def delete_internal(sess, ids):

	if ids:
		print("Doint delete. %s rows requiring update." % (len(ids), ))
	else:
		print("No rows needing deletion.")
		return

	ctbl = version_table(db.WebPages.__table__)
	chunk_size = 5000
	for chunk_idx in range(0, len(ids), chunk_size):
		chunk = ids[chunk_idx:chunk_idx+chunk_size]
		while 1:
			try:

				# Allow ids that only exist in the history table by falling back to a
				# history-table query if the main table doesn't have the ID.
				try:
					ex = sess.query(db.WebPages.url).filter(db.WebPages.id == chunk[0]).one()[0]
				except sqlalchemy.orm.exc.NoResultFound:
					ex = sess.query(ctbl.c.url).filter(ctbl.c.id == chunk[0]).all()[0][0]

				print("Example removed URL: '%s'" % (ex))


				q1 = sess.query(db.WebPages).filter(db.WebPages.id.in_(chunk))
				affected_rows_main = q1.delete(synchronize_session=False)

				q2 = sess.query(ctbl).filter(ctbl.c.id.in_(chunk))
				affected_rows_ver = q2.delete(synchronize_session=False)

				sess.commit()
				print("Deleted %s rows (%s version table rows). %0.2f%% done." %
						(affected_rows_main, affected_rows_ver,  100 * ((chunk_idx) / len(ids))))
				break
			except sqlalchemy.exc.InternalError:
				print("Transaction error (sqlalchemy.exc.InternalError). Retrying.")
				sess.rollback()
			except sqlalchemy.exc.OperationalError:
				print("Transaction error (sqlalchemy.exc.OperationalError). Retrying.")
				sess.rollback()
			except sqlalchemy.exc.IntegrityError:
				print("Transaction error (sqlalchemy.exc.IntegrityError). Retrying.")
				sess.rollback()
			except sqlalchemy.exc.InvalidRequestError:
				print("Transaction error (sqlalchemy.exc.InvalidRequestError). Retrying.")
				traceback.print_exc()
				sess.rollback()


def exposed_delete_spcnet_invalid_url_pages():
	'''
	So the spcnet.tv forum software generates THOUSANDS of garbage links somehow.
	Anyways, delete those.
	'''
	sess = db.get_db_session()
	tables = [
		db.WebPages.__table__,
		version_table(db.WebPages.__table__)
	]

	for ctbl in tables:
		# Print Querying for affected rows
		q = sess.query(ctbl.c.id) \
			.filter(ctbl.c.netloc == "www.spcnet.tv") \
			.filter(ctbl.c.content.like('%Invalid Forum specified. If you followed a valid link, please notify the%'))
		print("Query:")
		print(q)
		ids = q.all()

		ids = set(ids)

		# Returned list of IDs is each ID packed into a 1-tuple. Unwrap those tuples so it's just a list of integer IDs.
		ids = [tmp[0] for tmp in ids]

		print("Fount %s rows requring deletion. Deleting." % len(ids))
		delete_internal(sess, ids)
		sess.commit()

