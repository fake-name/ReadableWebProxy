
from app import db
from app import app
from app.models import Series
from app.models import Tags
from app.models import Genres
from app.models import Covers
from app.models import Author
from app.models import Illustrators
from app.models import Translators
from app.models import Watches
from app.models import AlternateNames
from app.models import AlternateTranslatorNames
import markdown
import bleach
import os.path
import os
import hashlib
from data_uri import DataURI
from flask.ext.login import current_user
import datetime
import app.nameTools as nt



def updateTags(series, tags, deleteother=True):
	havetags = Tags.query.filter((Tags.series==series.id)).all()
	havetags = {item.tag.lower() : item for item in havetags}

	tags = [tag.lower().strip().replace(" ", "-") for tag in tags]
	tags = [tag for tag in tags if tag.strip()]
	for tag in tags:
		if tag in havetags:
			havetags.pop(tag)
		else:
			newtag = Tags(series=series.id, tag=tag, changetime=datetime.datetime.now(), changeuser=current_user.id)
			db.session.add(newtag)
	if deleteother:
		for key, value in havetags.items():
			db.session.delete(value)
	db.session.commit()

def updateGenres(series, genres, deleteother=True):
	havegenres = Genres.query.filter((Genres.series==series.id)).all()
	havegenres = {item.genre.lower() : item for item in havegenres}

	genres = [genre.lower().strip().replace(" ", "-") for genre in genres]
	genres = [genre for genre in genres if genre.strip()]
	for genre in genres:
		if genre in havegenres:
			havegenres.pop(genre)
		else:
			newgenre = Genres(series=series.id, genre=genre, changetime=datetime.datetime.now(), changeuser=current_user.id)
			db.session.add(newgenre)
	if deleteother:
		for key, value in havegenres.items():
			db.session.delete(value)
	db.session.commit()


def updateAltNames(series, altnames, deleteother=True):
	# print("Alt names:", altnames)
	altnames = [name.strip() for name in altnames]
	cleaned = {}
	for name in altnames:
		if name.lower().strip():
			cleaned[name.lower().strip()] = name

	havenames = AlternateNames.query.filter(AlternateNames.series==series.id).order_by(AlternateNames.name).all()
	havenames = {name.name.lower().strip() : name for name in havenames}

	for name in cleaned.keys():
		if name in havenames:
			havenames.pop(name)
		else:
			newname = AlternateNames(
					name       = cleaned[name],
					cleanname  = nt.prepFilenameForMatching(cleaned[name]),
					series     = series.id,
					changetime = datetime.datetime.now(),
					changeuser = current_user.id
				)
			db.session.add(newname)

	if deleteother:
		for key, value in havenames.items():
			db.session.delete(value)
	db.session.commit()



def setAuthorIllust(series, author=None, illust=None, deleteother=True):
	if author and illust:
		return {'error' : True, 'message' : "How did both author and illustrator get passed here?"}
	elif author:
		table = Author
		values = author
	elif illust:
		table = Illustrators
		values = illust
	else:
		return {'error' : True, 'message' : "No parameters?"}

	have = table.query.filter(table.series==series.id).all()
	# print(have)

	haveitems = {item.name.lower().strip() : item for item in have}
	initems   = {    value.lower().strip() : value for value in values}


	for name in initems.keys():
		if name in haveitems:
			haveitems.pop(name)
		else:
			newentry = table(
					series     = series.id,
					name       = initems[name],
					changetime = datetime.datetime.now(),
					changeuser = current_user.id
				)
			db.session.add(newentry)

	if deleteother:
		for key, value in haveitems.items():
			db.session.delete(value)

	db.session.commit()



def updateGroupAltNames(group, altnames, deleteother=True):
	print("Alt names:", altnames)
	altnames = [name.strip() for name in altnames]
	cleaned = {}
	for name in altnames:
		if name.lower().strip():
			cleaned[name.lower().strip()] = name

	havenames = AlternateTranslatorNames.query.filter(AlternateTranslatorNames.group==group.id).order_by(AlternateTranslatorNames.name).all()
	havenames = {name.name.lower().strip() : name for name in havenames}

	for name in cleaned.keys():
		if name in havenames:
			havenames.pop(name)
		else:
			newname = AlternateTranslatorNames(
					name       = cleaned[name],
					cleanname  = nt.prepFilenameForMatching(cleaned[name]),
					group     = group.id,
					changetime = datetime.datetime.now(),
					changeuser = current_user.id
				)
			db.session.add(newname)

	if deleteother:
		for key, value in havenames.items():
			db.session.delete(value)
	db.session.commit()


def getHash(filecont):
	m = hashlib.md5()
	m.update(filecont)
	fHash = m.hexdigest()
	return fHash

def saveCoverFile(filecont, filename):
	fHash = getHash(filecont)
	# use the first 3 chars of the hash for the folder name.
	# Since it's hex-encoded, that gives us a max of 2^12 bits of
	# directories, or 4096 dirs.
	fHash = fHash.upper()
	dirName = fHash[:3]

	dirPath = os.path.join(app.config['COVER_DIR_BASE'], dirName)
	if not os.path.exists(dirPath):
		os.makedirs(dirPath)

	ext = os.path.splitext(filename)[-1]
	ext   = ext.lower()

	# The "." is part of the ext.
	filename = '{filename}{ext}'.format(filename=fHash, ext=ext)


	# The "." is part of the ext.
	filename = '{filename}{ext}'.format(filename=fHash, ext=ext)

	# Flask config values have specious "/./" crap in them. Since that gets broken through
	# the abspath canonization, we pre-canonize the config path so it compares
	# properly.
	confpath = os.path.abspath(app.config['COVER_DIR_BASE'])

	fqpath = os.path.join(dirPath, filename)
	fqpath = os.path.abspath(fqpath)

	if not fqpath.startswith(confpath):
		raise ValueError("Generating the file path to save a cover produced a path that did not include the storage directory?")

	locpath = fqpath[len(confpath):]
	if not os.path.exists(fqpath):
		print("Saving cover file to path: '{fqpath}'!".format(fqpath=fqpath))
		with open(fqpath, "wb") as fp:
			fp.write(filecont)
	else:
		print("File '{fqpath}' already exists!".format(fqpath=fqpath))

	if locpath.startswith("/"):
		locpath = locpath[1:]
	return locpath
