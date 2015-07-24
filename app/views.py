from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, send_file, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from itsdangerous import URLSafeTimedSerializer, BadSignature
from flask.ext.sqlalchemy import get_debug_queries
from flask.ext.babel import gettext
from datetime import datetime
# from guess_language import guess_language
from app import app, db, lm, babel
from .forms import  SearchForm


import sqlalchemy.sql.expression

import os.path
from sqlalchemy.sql.expression import func
from sqlalchemy import desc
from sqlalchemy.orm import joinedload

from app import AnonUser
import traceback

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
	db.session.rollback()
	print("Internal Error!")
	print(dummy_error)
	print(traceback.format_exc())
	# print("500 error!")
	return render_template('500.html'), 500




@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
	return render_template('index.html',
						   title               = 'Home',
						   )


@app.route('/view', methods=['GET'])
def view():
	req_url = request.args.get('url')
	if not req_url:
		return render_template('error.html', title = 'Home', message = "Error! No page specified!")
	return render_template('index.html', title = 'Home')

@app.route('/render', methods=['GET'])
def render():
	req_url = request.args.get('url')
	if not req_url:
		return render_template('error.html', title = 'Home', message = "Error! No page specified!")
	return render_template('index.html', title = 'Home')




@app.route('/favicon.ico')
def sendFavIcon():
	return send_file(
		"./static/favicon.ico",
		conditional=True
		)



