

from flask import render_template
from flask import make_response
from flask import request
from flask import jsonify
from flask import g

import WebMirror.Engine

from app import app
import pprint


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

	if version:
		return render_template('error.html', title = 'Error', message = "Historical views must be routed through the /history route!")

	if not req_url:
		return render_template('error.html', title = 'Resource Render', message = "Error! No page specified!")

	ignore_cache = request.args.get("nocache")

	title, content, cachestate, mimetype, fname = WebMirror.API.getPage(req_url, ignore_cache=ignore_cache)

	response = make_response(content)
	response.headers['Content-Type'] = mimetype
	# response.headers["Content-Disposition"] = "attachment; filename={}".format(fname)

	return response

def do_history_delete(versions, version, delete_id, delete):
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
				g.session.delete(version)
		g.session.commit()
		return render_template('error.html', title = 'All old versions deleted', message = "All old versions deleted")

	else:
		if not version in versions:
			return render_template('error.html', title = 'Error when deleting!', message = "Version value doesn't exist? ('%s', '%s')" % (version, type(version) ))
		target = versions[version]
		if not target.id == delete_id:
			return render_template('error.html', title = 'Error when deleting!', message = "Delete row PK Id doesn't match specified delete ID?")

		g.session.delete(target)
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

	with WebMirror.API.getPageRow(req_url) as page:
		versions = []

		rev = page.job.versions[0]
		while rev:
			versions.append(rev)
			rev = rev.next

		versions = list(enumerate(versions))
		versions.reverse()

		if delete_id and delete:
			return do_history_delete(versions, version, delete_id, delete)


		return render_template('history.html', title = 'Item History', page = page, req_url = req_url, versions=versions)

