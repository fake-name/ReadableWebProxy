
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

import WebMirror.Engine

from app import AnonUser
import traceback
from app import app

from app import lm
from app import babel
import time

import WebMirror.API


from WebMirror import database
import app.book_tree.trie_tools as trie_tools


from sqlalchemy import distinct

# This may wind up with performance issues when the DB gets HUEG. We'll see.
def getDistinctNetlocs():
	query = database.session.query(database.WebPages)                 \
		.filter(database.WebPages.is_text == True)                    \
		.filter(database.WebPages.file == None)                       \
		.filter(database.WebPages.state == 'complete')                \
		.distinct(database.WebPages.netloc)                           \
		.with_entities(database.WebPages.id, database.WebPages.netloc)
	# print(query)
	vals = query.all()
	return vals


@app.route('/pages/', defaults={'driver_netloc': None})
@app.route('/pages/<driver_netloc>')
def pages_root(driver_netloc):
	if driver_netloc:
		netlocs = [-1, driver_netloc]
	else:
		netlocs = getDistinctNetlocs()

	return render_template(
		'tree-pages/book-tree-root.html',
		netlocs = netlocs

		)


@app.route('/pages/branch/<netloc>', methods=['GET'])
def pages_branch(netloc):

	return render_template('tree-pages/book-tree-limb.html')


@app.route('/pages/leaf/<netloc>', methods=['GET'])
def pages_leaf(netloc):

	return render_template('tree-pages/book-tree-limb.html')


