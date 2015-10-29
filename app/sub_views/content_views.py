

from flask import render_template
from flask import make_response
from flask import request
from flask import jsonify

import WebMirror.Engine

from app import app


import WebMirror.API


@app.route('/view', methods=['GET'])
def view():
	req_url = request.args.get('url')
	if not req_url:
		return render_template('error.html', title = 'Viewer', message = "Error! No page specified!")

	return render_template('view.html', title = 'Home', req_url = req_url)


@app.route('/render', methods=['GET'])
def render():
	req_url = request.args.get('url')
	if not req_url:
		return render_template('error.html', title = 'Markup Render', message = "Error! No page specified!")
	req_url = request.args.get('url')

	ignore_cache = request.args.get("nocache")
	# print("Rendering with nocache=", ignore_cache)
	title, content, cachestate = WebMirror.API.getPage(req_url, ignore_cache=ignore_cache)
	print("Return:", cachestate)
	return jsonify(
		title      = title,
		contents   = content,
		cachestate = cachestate,
		req_url    = req_url,
		)

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


