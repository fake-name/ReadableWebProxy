

import common.util.webFunctions as webFunctions
import common.database as db
import common.util.urlFuncs as urlFuncs
import logging
import os.path
import settings

class Clean(object):

	def __init__(self):
		print("Clean __init__()")
		self.log = logging.getLogger("Main.Cleaner")
		super().__init__()

	def clean_files(self):

		session = db.get_db_session()
		q = session.query(db.WebFiles) \
			.filter(db.WebFiles.fspath != None)

		self.log.info("Querying for non-null filepaths...")
		have = q.all()
		self.log.info("Have %s local files.", len(have))
		count = 0
		for file in have:
			fpath = os.path.join(settings.RESOURCE_DIR, file.fspath)
			if not os.path.exists(fpath):
				self.log.error("Missing file: %s", fpath)

			count += 1
			if count % 1000 == 0:
				self.log.info("Scanned %s files.", count)

