
from flask import g
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
# from flask.ext.babel import gettext
# from guess_language import guess_language
from app import app


import WebMirror.API
from sqlalchemy import desc

from sqlalchemy.orm import joinedload
import traceback

from app.utilities import paginate
import common.database as db


from WebMirror.processor.RssProcessor import RssProcessor

@app.route('/feeds/<page>')
@app.route('/feeds/<int:page>')
@app.route('/feeds/')
def renderFeedsTable(page=1):

	feeds = g.session.query(db.RssFeedPost)       \
		.order_by(desc(db.RssFeedPost.published))


	feeds = feeds.options(joinedload('tag_rel'))
	feeds = feeds.options(joinedload('author_rel'))



	if feeds is None:
		flash('No feeds? Something is /probably/ broken!.')
		return redirect(url_for('renderFeedsTable'))

	feed_entries = paginate(feeds, page, app.config['FEED_ITEMS_PER_PAGE'])

	return render_template('rss-pages/feeds.html',
						   subheader = "",
						   sequence_item   = feed_entries,
						   page            = page
						   )



@app.route('/feeds/tag/<tag>/<page>')
@app.route('/feeds/tag/<tag>/<int:page>')
@app.route('/feeds/tag/<tag>/')
def renderFeedsTagTable(tag, page=1):
	query = g.session.query(db.RssFeedPost)
	# query = query.join(db.Tags)
	query = query.filter(db.RssFeedPost.tags.contains(tag))
	query = query.order_by(desc(db.RssFeedPost.published))

	feeds = query

	if feeds is None:
		flash('No feeds? Something is /probably/ broken!.')
		return redirect(url_for('renderFeedsTable'))

	feed_entries = paginate(feeds, page, app.config['FEED_ITEMS_PER_PAGE'])

	return render_template('rss-pages/feeds.html',
						   subheader = "Tag = '%s'" % tag,
						   sequence_item   = feed_entries,
						   page            = page
						   )

@app.route('/feeds/source/<source>/<page>')
@app.route('/feeds/source/<source>/<int:page>')
@app.route('/feeds/source/<source>/')
def renderFeedsSourceTable(source, page=1):
	feeds = g.session.query(db.RssFeedPost) \
		.filter(db.RssFeedPost.srcname == source)  \
		.order_by(desc(db.RssFeedPost.published))

	if feeds is None:
		flash('No feeds? Something is /probably/ broken!.')
		return redirect(url_for('renderFeedsTable'))

	feed_entries = paginate(feeds, page, app.config['FEED_ITEMS_PER_PAGE'])

	return render_template('rss-pages/feeds.html',
						   subheader = "Source = '%s'" % source,
						   sequence_item   = feed_entries,
						   page            = page
						   )




@app.route('/feeds/postid/<int:postid>')
def renderFeedEntry(postid):



	post = g.session.query(db.RssFeedPost) \
		.filter(db.RssFeedPost.id == postid)    \
		.scalar()

	# relink the feed contents.
	contents = WebMirror.API.replace_links(post.contents)

	return render_template('rss-pages/post.html',
						   entry = post,
						   contents = contents
						   )



def proto_process_releases(feed):
	ret_dict = {
			"successful" : [],
			"missed"     : [],
			"ignored"    : [],
	}

	dp = RssProcessor(
			db_sess=g.session,
			loggerPath="Main.WebProto",
			pageUrl=None,
			pgContent=None,
			type=None,
			)

	for item in feed.releases:
		proc_tmp = {}
		proc_tmp['feedtype']  = item.type
		proc_tmp['title']     = item.title
		proc_tmp['guid']      = item.contentid
		proc_tmp['linkUrl']   = item.contenturl
		proc_tmp['updated']   = item.updated
		proc_tmp['published'] = item.published
		proc_tmp['contents']  = item.contents
		proc_tmp['tags']      = item.tags
		proc_tmp['authors']   = item.author
		proc_tmp['srcname']   = feed.feed_name

		ret = dp.dispatchReleaseDbBacked(proc_tmp)

		# False means not caught. None means intentionally ignored.
		if ret:
			ret_dict["successful"].append((ret, proc_tmp))
		elif ret is False:
			ret_dict["missed"].append((ret, proc_tmp))
		elif ret is None:
			ret_dict["ignored"].append((ret, proc_tmp))
		else:
			raise RuntimeError("Wat? Unknown ret ({}) for release: {}".format(ret, proc_tmp))

	print("Returning: ", ret_dict)
	return ret_dict

@app.route('/feed-filters/feedid-process-results/<int:feedid>')
def feedLoadFilteredData(feedid):

	feed = g.session.query(db.RssFeedEntry) \
		.filter(db.RssFeedEntry.id == feedid)    \
		.scalar()
	items = proto_process_releases(feed)

	return render_template('rss-pages/feed_items_processed_block.html',
						   items         = items,
						   )


@app.route('/feed-filters/feedid/<int:feedid>')
def feedIdView(feedid):

	feed = g.session.query(db.RssFeedEntry) \
		.filter(db.RssFeedEntry.id == feedid)    \
		.scalar()
	rellist = list(feed.releases)

	return render_template('rss-pages/feed_filter_item.html',
						   feed          = feed,
						   feedid        = feedid,
						   release_count = len(rellist),
						   )





@app.route('/feed-filters/')
def feedFiltersRoot():


	feeds = g.session.query(db.RssFeedEntry) \
		.order_by(db.RssFeedEntry.feed_name) \
		.all()



	return render_template('rss-pages/feed_filter_base.html',
						   feeds = feeds,
						   )


