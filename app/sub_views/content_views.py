

import io
import urllib.parse

from flask import render_template
from flask import make_response
from flask import request
from flask import jsonify
from flask import g

from sqlalchemy_continuum.utils import version_table

import common.database as db
from app import app
from app import utilities
import pprint
import ast


import WebMirror.rules
import common.global_constants

import WebMirror.API

from PIL import Image

def build_error_response(message):
	response = jsonify(
		title      = "Error rendering content!",
		contents   = "Error message:<br> {}".format(message),
		cachestate = "Error!",
		req_url    = "None",
		error      = True,
		)
	return response

def set_cache_control_headers(response, allow_inline=False):

	response.headers['X-UA-Compatible']         = 'IE=Edge,chrome=1'
	response.headers["Cache-Control"]           = "no-cache, no-store, must-revalidate, max-age=0"
	response.headers["Pragma"]                  = "no-cache"
	response.headers["Expires"]                 = "Thu, 01 Jan 1970 00:00:00"

	response.headers["X-XSS-Protection"]        = "1; mode=block"
	response.headers["X-Frame-Options"]         = "deny"

	# Urrrrgh, I need to fix this
	response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self'; script-src 'self' {}".format("" if allow_inline is False else "'unsafe-inline'")

	return response


@app.route('/view', methods=['GET'])
def view():
	req_url = request.args.get('url')
	if not req_url:
		return render_template('error.html', title = 'Viewer', message = "Error! No page specified!")
	version = request.args.get('version')

	if version:
		return render_template('error.html', title = 'Error', message = "Historical views must be routed through the /history route!")

	response = make_response(render_template('view.html', title = 'Rendering Content', req_url = req_url, version=None))
	return set_cache_control_headers(response, allow_inline=True)

def do_history_delete(versions, version, delete_id, delete):

	ctbl = version_table(db.WebPages.__table__)

	if delete != "True":
		return render_template('error.html', title = 'Error when deleting!', message = "Delete param not true?")
	try:
		version = int(version)
	except ValueError:
		return render_template('error.html', title = 'Error when deleting!', message = "Cannot convert version value to integer!")
	try:
		delete_id = int(delete_id)
	except ValueError:
		return render_template('error.html', title = 'Error when deleting!', message = "Cannot convert delete_id value to integer!")

	versions = dict(versions)

	if delete_id == -1 and version == -1:
		maxid = max(versions.keys())

		for vid, version in versions.items():
			if vid != maxid:
				rid, tid = version.id, version.transaction_id
				print("Deleting:", version, rid, tid)
				g.session.query(ctbl)                     \
					.filter(ctbl.c.id             == rid) \
					.filter(ctbl.c.transaction_id == tid) \
					.delete(synchronize_session=False)
		g.session.commit()
		return render_template('error.html', title = 'All old versions deleted', message = "All old versions deleted")

	else:
		if not version in versions:
			return render_template('error.html', title = 'Error when deleting!', message = "Version value doesn't exist? ('%s', '%s')" % (version, type(version) ))
		target = versions[version]
		if not target.id == delete_id:
			return render_template('error.html', title = 'Error when deleting!', message = "Delete row PK Id doesn't match specified delete ID?")

		print("Deleting:", target)
		g.session.query(ctbl)                                       \
			.filter(ctbl.c.id == target.id)                         \
			.filter(ctbl.c.transaction_id == target.transaction_id) \
			.delete(synchronize_session=False)
		g.session.commit()

		return render_template('error.html', title = 'Row deleted', message = "Row: '%s', '%s'" % (delete_id, version))


@app.route('/history', methods=['GET'])
def view_history():
	req_url = request.args.get('url')
	if not req_url:
		return render_template('error.html', title = 'Viewer', message = "Error! No page specified!")


	version    = request.args.get('version')
	delete_id  = request.args.get("delete_id")
	delete     = request.args.get("delete")

	print(version, delete_id, delete)

	if version and not (delete_id or delete):
		return render_template('view.html', title = 'Rendering Content', req_url = req_url, version=version)

	versions = []

	ctbl = version_table(db.WebPages.__table__)


	versions = g.session.query(ctbl.c.id, ctbl.c.state, ctbl.c.fetchtime, ctbl.c.transaction_id) \
		.filter(ctbl.c.url == req_url)                                    \
		.order_by(ctbl.c.fetchtime)                                       \
		.all()

	versions = list(enumerate(versions))
	versions.reverse()

	if delete_id and delete:
		return do_history_delete(versions, version, delete_id, delete)


	return render_template('history.html', title = 'Item History', req_url = req_url, versions=versions)


def get_filter_state_for_url(url):
	url = url.lower()
	nl = urllib.parse.urlsplit(url).netloc

	if any([tmp.lower() in url for tmp in common.global_constants.GLOBAL_BAD_URLS]):
		return "Global badword filtered!"

	had_ruleset = False
	for ruleset in WebMirror.rules.load_rules():
		if not ruleset['netlocs']:
			continue

		if nl in ruleset['netlocs']:
			print("Have rule file!")
			had_ruleset = True
			if any([badword.lower() in url for badword in ruleset['badwords']]):
				return "Badword from ruleset!"
		# return "Rulefile badword filtered!"

	if had_ruleset:
		return "Not filtered, had ruleset!"
	return "Not Filtered, no ruleset."

 # @no_cache
@app.route('/render', methods=['GET'])
def render():
	req_url = request.args.get('url')
	if not req_url:
		return build_error_response(message = "Error! No page specified!")
	req_url = request.args.get('url')

	version = request.args.get('version')
	ignore_cache = request.args.get("nocache")

	filterstate = get_filter_state_for_url(req_url)

	try:
		if version == "None":
			version = None
		else:
			version = ast.literal_eval(version)
	except ValueError:
		return build_error_response(message = "Error! Historical version number must be an integer!")


	if version and ignore_cache:
		return build_error_response(message = "Error! Cannot render a historical version with nocache!")

	if version:
		rid, tid = version

		print("Historical row id: ", rid, tid)

		ctbl = version_table(db.WebPages.__table__)

		rows = g.session.query(ctbl.c.title, ctbl.c.content) \
			.filter(ctbl.c.id == rid)                        \
			.filter(ctbl.c.transaction_id == tid)            \
			.all()

		if rows:
			row = rows.pop()
			title, content = row
			content = utilities.replace_links(content)
			cachestate = "Historical version: %s" % (version, )
	else:
		title, content, cachestate = WebMirror.API.getPage(req_url, ignore_cache=ignore_cache, version=version)

	# print("Render-Version: ", version, type(version))
	# print("Rendering with nocache=", ignore_cache)
	# print("Return:", cachestate)
	response = jsonify(
		title       = title,
		contents    = content,
		cachestate  = cachestate,
		filterstate = filterstate,
		req_url     = req_url,
		)
	return set_cache_control_headers(response)


@app.route('/render_rsc', methods=['GET'])
def render_resource():
	req_url = request.args.get('url')
	if not req_url:
		return render_template('error.html', title = 'Resource Render', message = "Error! No page specified!")

	ignore_cache = request.args.get("nocache")

	mimetype, fname, content, cachestate = WebMirror.API.getResource(req_url, ignore_cache=ignore_cache)

	# Deal with internet explorer being garbage.
	if mimetype == 'image/webp':
		img = Image.open(io.BytesIO(content))
		out = io.BytesIO()
		img.save(out, format="png")
		content = out.getvalue()
		mimetype = 'img/png'
		fname = fname + ".png"

	response = make_response(content)
	response.headers['Content-Type'] = mimetype
	response.headers["Content-Disposition"] = "attachment; filename={}".format(fname)


	return set_cache_control_headers(response)

	# return render_template('render.html',
	# 	title      = title,
	# 	contents   = content,
	# 	cachestate = cachestate,
	# 	req_url    = req_url,
	# 	)


