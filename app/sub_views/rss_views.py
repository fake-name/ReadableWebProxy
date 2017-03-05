
from flask import g
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import make_response
from flask import request
from flask import jsonify
# from flask.ext.babel import gettext
# from guess_language import guess_language
from app import app


import WebMirror.API
from sqlalchemy import desc

from sqlalchemy.orm import joinedload
import traceback
import datetime
import collections
import astor

from app.utilities import paginate
import app.sub_views.content_views as content_views
import common.database as db
import common.rss_func_db as rfdb

from WebMirror.OutputFilters.util.TitleParsers import extractVolChapterFragmentPostfix
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



def proto_process_releases(feed_releases):
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

	for item in feed_releases:
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
		proc_tmp['srcname']   = item.feed_entry.feed_name
		proc_tmp['feed_id']   = item.feed_entry.id

		proc_tmp['vcfp']      = extractVolChapterFragmentPostfix(item.title)

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

	return ret_dict

@app.route('/feed-filters/feedid-process-results/<int:feedid>')
def feedLoadFilteredData(feedid):

	feed = g.session.query(db.RssFeedEntry)   \
		.filter(db.RssFeedEntry.id == feedid) \
		.options(joinedload('releases'))  \
		.scalar()

	items = proto_process_releases(feed.releases)

	return render_template('rss-pages/feed_items_processed_block.html',
						   items         = items,
						   release_count = len(feed.releases),
						   )


@app.route('/feed-filters/feedid/<int:feedid>')
def feedIdView(feedid):

	feed = g.session.query(db.RssFeedEntry)   \
		.filter(db.RssFeedEntry.id == feedid) \
		.scalar()

	return render_template('rss-pages/feed_filter_item.html',
						   feed          = feed,
						   feedid        = feedid,
						   )





@app.route('/feed-filters/')
def feedFiltersRoot():

	feeds = g.session.query(db.RssFeedEntry) \
		.order_by(db.RssFeedEntry.feed_name) \
		.all()

	return render_template('rss-pages/feed_filter_base.html',
						   feeds = feeds,
						   )




@app.route('/feed-filters/recent')
def feedFiltersRecent():

	valid_scopes = ["day", "week", "month", "all"]
	scope = 'day'
	if "scope" in request.args and request.args['scope'] in valid_scopes:
		scope = request.args['scope']

	if   scope == "day":
		item_scope_str   = "Last day"
		item_scope_limit = datetime.datetime.now() - datetime.timedelta(days=1)
	elif scope == "week":
		item_scope_str   = "Last Week"
		item_scope_limit = datetime.datetime.now() - datetime.timedelta(days=7)
	elif scope == "month":
		item_scope_str   = "Last Month"
		item_scope_limit = datetime.datetime.now() - datetime.timedelta(days=45)
	elif scope == "all":
		item_scope_str   = "All"
		item_scope_limit = datetime.datetime.min
	else:
		return render_template('error.html', title = 'Viewer', message = "Error! Invalid history scope!")



	feeds = g.session.query(db.RssFeedPost)                  \
		.filter(db.RssFeedPost.published > item_scope_limit) \
		.all()

	items = proto_process_releases(feeds)

	release_count = len(feeds)
	missed_count  = len(items['missed'])

	bykey = {}
	for dummy_ret, item in items['missed']:
		if not item['srcname'] in bykey:
			bykey[item['srcname']] = []

		bykey[item['srcname']].append(item)

	sortable = []
	for key in bykey:
		# 1e9 subtraction inverts the ordering of the first item.
		sortable.append((1e9 - len(bykey[key]), key.lower(), key, len(bykey[key]), bykey[key][0]['feed_id'], bykey[key]))

	sortable.sort()

	sorted_items = collections.OrderedDict()
	for dummy_1, dummy_2, source_name, count, source_id, item in sortable:
		key = (source_name, count, source_id)
		if key not in sorted_items:
			sorted_items[key] = []
		sorted_items[key].extend(item)

	return render_template('rss-pages/feeds_only_results.html',
						   release_count = release_count,
						   missed_count  = missed_count,
						   items         = sorted_items,
						   item_scope    = item_scope_str,
						   )


def update_function_text(feedrow, new_func):
	current = feedrow.func.strip()
	new_func = new_func.strip()
	print("New function:", new_func)
	print("Current function:", current)

	if current == new_func:
		return {
			'error'   : True,
			'message' : "Function has not changed? Nothing to do!",
			'reload'  : False,
		}

	try:
		rfdb.str_to_function(new_func, "testing_compile")
	except Exception:
		resp  = '<div class="center-block text-center"><h4>New function failed to compile!</h4></div>'
		resp += "<pre><code>"+ traceback.format_exc() + "</code></pre>"
		return {
			'error'   : True,
			'message' : resp,
			'reload'  : False,
		}

	feedrow.func = new_func

	return {
		'error'   : False,
		'message' : "Function updated successfully!",
		'reload'  : True,
	}

@app.route('/feed-filters/api/', methods=['GET', 'POST'])
def feedFiltersApi():
	if not request.json:
		# print("Non-JSON request!")
		js = {
			"error"   : True,
			"message" : "This endpoint only accepts JSON POST requests."
		}
		resp = jsonify(js)
		resp.status_code = 200
		resp.mimetype="application/json"
		return resp


	print("API Request!")
	print("session:", g.session)
	print("Request method: ", request.method)
	print("Request json: ", request.json)

	assert "mode"    in request.json
	assert "data"    in request.json
	assert "feed_id" in request.json

	try:
		mode    =     request.json["mode"]
		data    =     request.json["data"]
		feed_id = int(request.json["feed_id"])
	except ValueError:
		return content_views.build_error_response("Feed ID must be an integer!")

	feed = g.session.query(db.RssFeedEntry)    \
		.filter(db.RssFeedEntry.id == feed_id) \
		.scalar()

	if not feed:
		return content_views.build_error_response("Feed ID not found!")

	if mode == "update_feed_parse_func":
		raw_resp = update_function_text(feed, data)

	response = jsonify(raw_resp)

	response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
	response.headers["Pragma"] = "no-cache"
	response.headers["Expires"] = "Thu, 01 Jan 1970 00:00:00"

	response.status_code = 200
	response.mimetype="application/json"
	g.session.commit()
	g.session.expire_all()

	print("ResponseData: ", raw_resp)
	print("Response: ", response)

	return response


