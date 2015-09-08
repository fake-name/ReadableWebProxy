

from flask import render_template
from flask import make_response
from flask import request

import WebMirror.Engine

from app import app


import WebMirror.API


@app.route('/search', methods=['GET'])
def search():
	scope = request.args.get('scope')
	query = request.args.get('query')
	if not (scope and query):
		return render_template('search.html')
	else:
		return search_item(scope, query)



def search_item(scope, query):
	print("scope", scope)
	print("query", query)
	req_url = request.args.get('url')
	if not req_url:
		return render_template('error.html', title = 'Home', message = "Error! No page specified!")

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


