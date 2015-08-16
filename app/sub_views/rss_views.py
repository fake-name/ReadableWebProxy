
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import abort
from flask.ext.babel import gettext
# from guess_language import guess_language
from app import app

from flask.ext.sqlalchemy import Pagination

import WebMirror.API
from sqlalchemy import desc

from sqlalchemy.orm import joinedload
import traceback

import WebMirror.database as db


def paginate(query, page, per_page=20, error_out=True):
	if error_out and page < 1:
		abort(404)
	items = query.limit(per_page).offset((page - 1) * per_page).all()
	if not items and page != 1 and error_out:
		abort(404)

	# No need to count if we're on the first page and there are fewer
	# items than we expected.
	if page == 1 and len(items) < per_page:
		total = len(items)
	else:
		total = query.order_by(None).count()

	return Pagination(query, page, per_page, total, items)


@app.route('/feeds/<page>')
@app.route('/feeds/<int:page>')
@app.route('/feeds/')
def renderFeedsTable(page=1):

	feeds = db.get_session().query(db.FeedItems)       \
		.order_by(desc(db.FeedItems.published))


	# feeds = feeds.options(joinedload('tags'))
	# feeds = feeds.options(joinedload('authors'))



	if feeds is None:
		flash(gettext('No feeds? Something is /probably/ broken!.'))
		return redirect(url_for('renderFeedsTable'))

	feed_entries = paginate(feeds, page, app.config['FEED_ITEMS_PER_PAGE'])

	return render_template('rss-pages/feeds.html',
						   sequence_item   = feed_entries,
						   page            = page
						   )


@app.route('/feeds/postid/<int:postid>')
def renderFeedEntry(postid):



	post = db.get_session().query(db.FeedItems) \
		.filter(db.FeedItems.id == postid)    \
		.scalar()

	# relink the feed contents.
	contents = WebMirror.API.replace_links(post.contents)

	return render_template('rss-pages/post.html',
						   entry = post,
						   contents = contents
						   )