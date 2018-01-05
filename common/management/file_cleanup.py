

import settings
import shutil
import os.path
import os
import sys
from tqdm import tqdm

import common.database as db
from sqlalchemy_continuum.utils import version_table



class Spinner(object):
	def __init__(self):
		# outStr = "-\\|/"
		self.outStr  = "|-"
		self.outStar = "*x"
		self.outMatch = r"\/"
		self.outClean = "Dd"
		self.outInt = 0
		self.x = 0

		self.dlen = 0
		self.itemLen = len(self.outStr)

		self.prints = 0

	def next(self, star=False, clean=False, hashmatch=False, vlen=1, output=True):
		self.outInt += 1
		self.dlen += vlen
		#sys.stdout.write( "\r%s\r" % outStrs[self.outInt])

		if output:
			if self.prints % 80 == 0:
				sys.stdout.write("\r %9d %9d " % (self.outInt, self.dlen))
				self.x = (self.x + 1) % self.itemLen

			if star:
				sys.stdout.write(self.outStar[self.x])
			elif clean:
				sys.stdout.write(self.outClean[self.x])
			elif hashmatch:
				sys.stdout.write(self.outMatch[self.x])
			else:
				sys.stdout.write(self.outStr[self.x])


			sys.stdout.flush()
			self.prints += 1


def sync_raw_with_filesystem():

	sess = db.get_db_session()

	print("Loading files from database...")
	est = sess.execute("SELECT reltuples::BIGINT AS estimate FROM pg_class WHERE relname='raw_web_pages';")
	res = est.scalar()
	print("Estimated row-count: %s" % res)

	in_db = []
	with tqdm(total=res) as pbar:

		for fspath,  in sess.query(db.RawWebPages.fspath).yield_per(5000):
			if fspath:
				in_db.append(fspath)
			pbar.update(n=1)

	in_db = set(in_db)

	tgtpath = settings.RAW_RESOURCE_DIR
	print("")
	print("Enumerating files from disk...")
	agg_files = []
	have_files = []
	with tqdm(total=len(in_db)) as pbar:

		for root, dirs, files in os.walk(tgtpath):
			for filen in files:
				fqpath = os.path.join(root, filen)
				fpath = fqpath[len(tgtpath)+1:]

				if fpath in in_db:

					have_files.append(fpath)
				else:

					agg_files.append(fpath)
					fqpath = os.path.join(tgtpath, fpath)
					# os.unlink(fqpath)
					print("\rDeleting: %s  " % fqpath)
				pbar.update(n=1)


	print()
	print("Found %s files (%s unique)" % (len(agg_files), len(set(agg_files))))

	missing_files = set(in_db) - set(have_files)

	for filen in agg_files:
		print("Should delete: '%s'" % filen)
	for filen in missing_files:
		print("Missing: '%s'" % filen)

		sess.query(db.RawWebPages).filter(db.RawWebPages.fspath == filen).update({"state" : "new", "fspath" : None})
		sess.commit()



def sync_filtered_with_filesystem():
	tgtpath = settings.RESOURCE_DIR
	ctbl = version_table(db.RawWebPages.__table__)

	sess = db.get_db_session()

	print("Loading files from database...")
	# spinner1 = Spinner()

	est = sess.execute("SELECT reltuples::BIGINT AS estimate FROM pg_class WHERE relname='raw_web_pages';")
	res = est.scalar()

	vest = sess.execute("SELECT reltuples::BIGINT AS estimate FROM pg_class WHERE relname='raw_web_pages_version';")
	vres = vest.scalar()

	print("Estimated row-count: %s, version table: %s" % (res, vres))

	in_main_db = []
	with tqdm(total=res) as pbar:
		for row in sess.query(db.WebFiles).yield_per(10000):
			if row.fspath:
				in_main_db.append(row.fspath)
				pbar.update(n=1)



	in_history_db = []

	with tqdm(total=vres) as pbar:
		for rfspath, in sess.query(ctbl.c.fspath).yield_per(1000):
			if rfspath:
				in_history_db.append(rfspath)
				pbar.update(n=1)


	origl_main = len(in_main_db)
	origl_hist = len(in_history_db)
	in_db_main = set(in_main_db)
	in_db_hist = set(in_history_db)

	in_db = in_db_main + in_db_hist

	print("")
	print("%s files, %s unique" % ((origl_main, origl_hist), (len(in_db_main), len(in_db_hist))))
	print("Enumerating files from disk...")
	agg_files = []
	have_files = []
	# spinner2 = Spinner()

	with tqdm(total=len(in_db)) as pbar:
		for root, _, files in os.walk(tgtpath):
			for filen in files:
				fqpath = os.path.join(root, filen)
				fpath = fqpath[len(tgtpath)+1:]

				if fpath in in_db:
					pbar.update(n=1)
					# spinner2.next(star=True, vlen=0)
					have_files.append(fpath)
				else:
					pbar.update(n=1)
					# spinner2.next(vlen=1)
					agg_files.append(fpath)
					fqpath = os.path.join(tgtpath, fpath)
					# os.unlink(fqpath)
					print("\rDeleting: %s  " % fqpath)

