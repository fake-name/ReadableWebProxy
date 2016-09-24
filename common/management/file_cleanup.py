

import settings
import shutil
import os.path
import os
import sys

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



	def next(self, star=False, clean=False, hashmatch=False, vlen=1):
		self.outInt += 1
		self.dlen += vlen
		#sys.stdout.write( "\r%s\r" % outStrs[self.outInt])
		if self.outInt % 80 == 0:
			sys.stdout.write("\r %7d %12d " % (self.outInt, self.dlen))
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



def sync_raw_with_filesystem():

	sess = db.get_db_session()

	print("Loading files from database...")
	spinner1 = Spinner()
	in_db = []
	for row in sess.query(db.RawWebPages).yield_per(1000).all():
		if row.fspath:
			in_db.append(row.fspath)
			spinner1.next(vlen=len(row.fspath))
		else:
			spinner1.next(star=True)

	in_db = set(in_db)

	tgtpath = settings.RAW_RESOURCE_DIR
	print("")
	print("Enumerating files from disk...")
	agg_files = []
	have_files = []
	spinner2 = Spinner()
	for root, dirs, files in os.walk(tgtpath):
		for filen in files:
			fqpath = os.path.join(root, filen)
			fpath = fqpath[len(settings.RAW_RESOURCE_DIR)+1:]

			if fpath in in_db:
				spinner2.next(star=True, vlen=0)
				have_files.append(fpath)
			else:
				spinner2.next(vlen=1)
				agg_files.append(fpath)
				fqpath = os.path.join(tgtpath, fpath)
				os.unlink(fqpath)
				print("\rDeleting: %s  " % fqpath)

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
	spinner1 = Spinner()
	in_db = []
	for row in sess.query(db.WebPages).filter(db.WebPages.file != None).yield_per(1000).all():
		if row.fspath:
			in_db.append(row.fspath)
			spinner1.next(vlen=len(row.fspath))
		else:
			spinner1.next(star=True)

	in_db = set(in_db)
	print("")
	print("Enumerating files from disk...")
	agg_files = []
	spinner2 = Spinner()
	for root, dirs, files in os.walk(tgtpath):
		for filen in files:
			fqpath = os.path.join(root, filen)
			fpath = fqpath[len(tgtpath)+1:]

			if fpath in in_db:
				spinner2.next(star=True, vlen=0)
			else:
				spinner2.next(vlen=1)
				agg_files.append(fpath)
				fqpath = os.path.join(tgtpath, fpath)
				os.unlink(fqpath)
				print("\rDeleting: %s  " % fqpath)

	print()
	print("Found %s files (%s unique)" % (len(agg_files), len(set(agg_files))))

	for filen in agg_files:
		print("Should delete: '%s'" % filen)
