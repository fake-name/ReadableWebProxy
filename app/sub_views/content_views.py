

from flask import render_template
from flask import make_response
from flask import request
from flask import jsonify

import WebMirror.Engine

from app import app


import WebMirror.API

def build_error_response(message):
	response = jsonify(
		title      = "Error rendering content!",
		contents   = "Error message:<br> {}".format(message),
		cachestate = "Error!",
		req_url    = "None",
		)
	return response

@app.route('/view', methods=['GET'])
def view():
	req_url = request.args.get('url')
	if not req_url:
		return render_template('error.html', title = 'Viewer', message = "Error! No page specified!")
	version = request.args.get('version')

	if version == "None":
		version = None

	return render_template('view.html', title = 'Rendering Content', req_url = req_url, version=version)


@app.route('/history', methods=['GET'])
def view_history():
	req_url = request.args.get('url')
	if not req_url:
		return render_template('error.html', title = 'Viewer', message = "Error! No page specified!")


	version = request.args.get('version')
	if version:
		return render_template('view.html', title = 'Rendering Content', req_url = req_url, version=version)

	with WebMirror.API.getPageRow(req_url) as page:
		versions = []

		rev = page.job.versions[0]
		while rev:
			versions.append(rev)
			rev = rev.next

		versions = list(enumerate(versions))
		versions.reverse()

		return render_template('history.html', title = 'Item History', page = page, req_url = req_url, versions=versions)


@app.route('/render', methods=['GET'])
def render():
	req_url = request.args.get('url')
	if not req_url:
		return build_error_response(message = "Error! No page specified!")
	req_url = request.args.get('url')

	version = request.args.get('version')
	ignore_cache = request.args.get("nocache")

	try:
		if version == "None":
			version = None
		else:
			version = int(version)
	except ValueError:
		return build_error_response(message = "Error! Historical version number must be an integer!")

	if version and ignore_cache:
		return build_error_response(message = "Error! Cannot render a historical version with nocache!")

	title, content, cachestate = WebMirror.API.getPage(req_url, ignore_cache=ignore_cache, version=version)

	# print("Render-Version: ", version, type(version))
	# print("Rendering with nocache=", ignore_cache)
	# print("Return:", cachestate)
	response = jsonify(
		title      = title,
		contents   = content,
		cachestate = cachestate,
		req_url    = req_url,
		)

	response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
	response.headers["Pragma"] = "no-cache"
	response.headers["Expires"] = "Thu, 01 Jan 1970 00:00:00"

	return response

@app.route('/render_rsc', methods=['GET'])
def render_resource():
	req_url = request.args.get('url')
	if not req_url:
		return render_template('error.html', title = 'Resource Render', message = "Error! No page specified!")

	ignore_cache = request.args.get("nocache")

	mimetype, fname, content, cachestate = WebMirror.API.getResource(req_url, ignore_cache=ignore_cache)

	response = make_response(content)
	response.headers['Content-Type'] = mimetype
	response.headers["Content-Disposition"] = "attachment; filename={}".format(fname)

	return response
	# return render_template('render.html',
	# 	title      = title,
	# 	contents   = content,
	# 	cachestate = cachestate,
	# 	req_url    = req_url,
	# 	)


