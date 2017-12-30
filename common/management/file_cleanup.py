

import settings
import shutil
import os.path
import os
import sys
from tqdm import tqdm

import common.database as db



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

		for row in sess.query(db.RawWebPages).yield_per(5000):
			if row.fspath:
				in_db.append(row.fspath)
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
					os.unlink(fqpath)
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

	sess = db.get_db_session()

	print("Loading files from database...")
	# spinner1 = Spinner()

	est = sess.execute("SELECT reltuples::BIGINT AS estimate FROM pg_class WHERE relname='raw_web_pages';")
	res = est.scalar()
	print("Estimated row-count: %s" % res)

	in_db = []
	chunk_cnt = 0
	with tqdm(total=res) as pbar:
		for row in sess.query(db.WebFiles).yield_per(10000):
			chunk_cnt += 1
			if row.fspath:
				in_db.append(row.fspath)
				# spinner1.next(vlen=len(row.fspath), output=(chunk_cnt == 10))
				pbar.update(n=1)

				if chunk_cnt == 40:
					chunk_cnt = 0

	origl = len(in_db)
	in_db = set(in_db)

	print("")
	print("%s files, %s unique" % (origl, len(in_db)))
	print("Enumerating files from disk...")
	agg_files = []
	have_files = []
	# spinner2 = Spinner()

	with tqdm(total=len(in_db)) as pbar:
		for root, dirs, files in os.walk(tgtpath):
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

	# print()
	# print("Found %s files (%s unique)" % (len(agg_files), len(set(agg_files))))

	# missing_files = set(in_db) - set(have_files)

	# for filen in agg_files:
	# 	print("Should delete: '%s'" % filen)
	# for filen in missing_files:
	# 	print("Missing: '%s'" % filen)

	# 	sess.query(db.WebPages).filter(db.WebPages.fspath == filen).update({"state" : "new", "fspath" : None})
	# 	sess.commit()
