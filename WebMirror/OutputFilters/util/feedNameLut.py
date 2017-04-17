
import urllib.parse
from common import database as db
from sqlalchemy.orm import joinedload


def patch_blogspot(innetloc):
	# Blogspot domains are coerced to ".com" since they seem to localize their TLD,
	# and somehow it all points to the same place in the end.
	if ".blogspot." in innetloc and not innetloc.endswith(".blogspot.com"):
		prefix = innetloc.split(".blogspot.")[0]
		innetloc = prefix + ".blogspot.com"
	return innetloc


def get_name_for_netloc_db(db_sess, netloc):

	row = db_sess.query(db.RssFeedUrlMapper) \
		.filter(db.RssFeedUrlMapper.feed_netloc == netloc) \
		.options(joinedload('feed_entry')) \
		.all()

	if not row:
		return False

	if len(row) > 1:
		print("ERROR: Multiple solutions for netloc %s?" % netloc)

	feedname = row[0].feed_entry.feed_name
	if feedname:
		return feedname
	else:
		return False

def getNiceName(session, srcurl, netloc=None, debug=False):
	if netloc:
		srcnetloc = netloc
	else:
		srcnetloc = urllib.parse.urlparse(srcurl).netloc

	srcnetloc = patch_blogspot(srcnetloc)

	val = get_name_for_netloc_db(session, srcnetloc)

	return val
