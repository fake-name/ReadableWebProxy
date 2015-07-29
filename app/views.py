
from flask import flash
from flask import redirect
from flask import session
from flask import url_for
from flask import jsonify
from flask import abort
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask.ext.login import login_required
from itsdangerous import URLSafeTimedSerializer
from itsdangerous import BadSignature
from flask.ext.babel import gettext
from datetime import datetime


# from guess_language import guess_language

import markdown
import os.path

from flask import render_template
from flask import make_response
from flask import send_file
from flask import request
from flask import g
from flask.ext.login import current_user
from flask.ext.sqlalchemy import get_debug_queries

from app import AnonUser
import traceback
from app import app

from app import lm
from app import babel
import time

import WebMirror.API

@lm.user_loader
def load_user(id):
	return AnonUser()


@babel.localeselector
def get_locale():
	return 'en'


@app.before_request
def before_request():

	g.user = current_user
	g.locale = get_locale()



@app.after_request
def after_request(response):
	for query in get_debug_queries():
		if query.duration >= app.config['DATABASE_QUERY_TIMEOUT']:
			app.logger.warning(
				"SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" %
				(query.statement, query.parameters, query.duration,
				 query.context))
	return response


@app.errorhandler(404)
def not_found_error(dummy_error):
	print("404. Wat?")
	return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(dummy_error):
	print("Internal Error!")
	print(dummy_error)
	print(traceback.format_exc())
	# print("500 error!")
	return render_template('500.html'), 500




@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():

	interesting = ""
	if os.path.exists("reading_list.txt"):
		with open("reading_list.txt", "r") as fp:
			raw_text = fp.read()
		interesting = markdown.markdown(raw_text)
	return render_template('index.html',
						   title               = 'Home',
						   interesting_links   = interesting,
						   )


@app.route('/view', methods=['GET'])
def view():
	req_url = request.args.get('url')
	if not req_url:
		return render_template('error.html', title = 'Home', message = "Error! No page specified!")
	return render_template('view.html', title = 'Home', req_url = req_url)


@app.route('/render', methods=['GET'])
def render():
	req_url = request.args.get('url')
	if not req_url:
		return render_template('error.html', title = 'Home', message = "Error! No page specified!")

	title, content, cachestate = WebMirror.API.getPage(req_url)

	return render_template('render.html',
		title      = title,
		contents   = content,
		cachestate = cachestate,
		req_url    = req_url,
		)

@app.route('/render_rsc', methods=['GET'])
def render_resource():
	req_url = request.args.get('url')
	if not req_url:
		return render_template('error.html', title = 'Home', message = "Error! No page specified!")

	mimetype, fname, content, cachestate = WebMirror.API.getResource(req_url)

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


@app.route('/favicon.ico')
def sendFavIcon():
	return send_file(
		"./static/favicon.ico",
		conditional=True
		)



