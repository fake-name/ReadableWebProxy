
import os
import os.path
import urllib.parse

from flask import g
from flask import render_template
from flask import make_response
from flask import request
from flask import redirect
from flask import send_file

import settings

from app import app


import common.database as db

def render_ebook_directory(fpath):
	print("Invoking scandir")
	items = os.scandir(fpath)
	items = [
		{
			'name'      : item.name,
			'fullpath'  : os.path.join(fpath, item.name),
			'directory' : fpath,
			'is_dir'    : item.is_dir(),
			'is_file'   : item.is_file(),
			'relp'      : urllib.parse.urljoin("/epub-reader/", urllib.parse.quote(os.path.relpath(os.path.join(fpath, item.name), settings.EBOOK_STORAGE_DIR)))
		}
		for item in items
	]

	items.sort(key=lambda x: x['name'])
	print("Query done. Rendering with %s items" % (len(items), ))
	return render_template('book-reader/reader-dir.html',
		fpath = fpath,
		items = items,
		)

def render_ebook_reader(fpath):
	ext = os.path.splitext(fpath)[-1]
	furl = urllib.parse.urljoin("/epub-content/", urllib.parse.quote(os.path.relpath(fpath, settings.EBOOK_STORAGE_DIR)))
	if ext == ".pdf":
		return redirect("/static/ext/pdfjs/web/viewer.html?file=%s" % (urllib.parse.quote(furl)))

	if ext == ".epub":
		if "bibi" in request.args:
			return render_template('book-reader/reader-epub-bibi.html', furl = furl)
		else:
			return render_template('book-reader/reader-epub-epubjs.html', furl = furl)
			# return redirect("/static/ext/bib/i/index.html?book=%s" % (urllib.parse.quote(furl)))
	else:

		return render_template('error.html', title = 'Ebook Reader', message = "render_ebook_file on '%s' with unknown type: %s" % (fpath, ext))


def render_ebook_file(fpath):
	return render_template('error.html', title = 'Ebook Reader', message = "render_ebook_file for unknown format file: : %s" % fpath)

def render_ebook_error(fpath):
	return render_template('error.html', title = 'Ebook Reader', message = "Could not find content at %s" % fpath)



@app.route('/epub-content/<path:fpath>', methods=['GET'])
@app.route('/static/ext/bib/bookshelf/epub-content/<path:fpath>', methods=['GET'])
@app.route('/static/ext/bib/bookshelf//epub-content/<path:fpath>', methods=['GET'])
def ebook_file_content(fpath=None):
	if fpath is None:
		fpath = ""

	fpath = os.path.join(settings.EBOOK_STORAGE_DIR, fpath)
	fpath = os.path.abspath(fpath)
	assert fpath.startswith(settings.EBOOK_STORAGE_DIR)

	print("Fpath request:", fpath)

	if not os.path.exists(fpath):
		return render_ebook_error(fpath)

	if os.path.isfile(fpath):
		return send_file(fpath)

	else:
		return render_ebook_error(fpath)



@app.route('/epub-reader/', methods=['GET'])
@app.route('/epub-reader/<path:fpath>', methods=['GET'])
def ebook_root_view(fpath=None):
	if fpath is None:
		fpath = ""

	fpath = os.path.join(settings.EBOOK_STORAGE_DIR, fpath)
	fpath = os.path.abspath(fpath)
	assert fpath.startswith(settings.EBOOK_STORAGE_DIR)

	if not os.path.exists(fpath):
		return render_ebook_error(fpath)

	if os.path.isdir(fpath):
		return render_ebook_directory(fpath)
	elif os.path.isfile(fpath):
		return render_ebook_reader(fpath)
	else:
		return render_ebook_error(fpath)
