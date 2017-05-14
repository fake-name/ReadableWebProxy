
from flask import g
from flask import render_template
from flask import request
import json
import urllib.parse

from app import app

import traceback
import common.database as db

from app.utilities import paginate
import sqlalchemy.exc
from sqlalchemy.sql.expression import func
from sqlalchemy.dialects import postgresql

import WebMirror.rules

import pymysql
import settings




def get_random_url_group(num_items):
	dat = g.session.execute('''SELECT url FROM web_pages TABLESAMPLE SYSTEM(:percentage);''', {'percentage' : num_items})
	ret = list(dat)
	return ret


@app.route('/random-urls/', methods=['GET'])
def random_urls_view():
	entries = get_random_url_group(0.003)

	return render_template('misc/random-urls.html',
		header    = "Random URL Subset",
						   results   = entries,
						   )