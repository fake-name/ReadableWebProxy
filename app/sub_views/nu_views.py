
from flask import g
from flask import render_template
from flask import make_response
from flask import request
from flask import jsonify

import pickle
import time
import json
import datetime
from calendar import timegm

from sqlalchemy.sql import text
from app import app


import WebMirror.database as db

from app.utilities import paginate
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.expression import func
from tzlocal import get_localzone
import WebMirror.API


def get_nu_items(sess, all_items):
	new_items = sess.query(db.NuOutboundWrapperMap)     \
		.filter(db.NuOutboundWrapperMap.validated == False) \
		.all()

	return new_items

@app.route('/nu_releases/', methods=['GET'])
def nu_view():

	all_releases = request.args.get('all')

	session = g.session
	new = get_nu_items(g.session, all_releases)
	session.commit()
	new.sort(key=lambda x: x.seriesname)

	return render_template('nu_releases.html',
						   new          = new,
						   all_releases = all_releases,
						   )

@app.route('/nu_api/', methods=['GET', 'POST'])
def nu_api():
	print("API Request!")
	print("session:", g.session)
	print("Request method: ", request.method)
	print("Request json: ", request.json)
	if not request.json:
		# print("Non-JSON request!")
		js = {
			"error"   : True,
			"message" : "This endpoint only accepts JSON POST requests."
		}
		resp = jsonify(js)
		resp.status_code = 200
		resp.mimetype="application/json"
		return resp


	data = {"wat": "wat"}
	response = jsonify(data)

	print("response", response)
	# response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
	# response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
	# response.headers["Pragma"] = "no-cache"
	# response.headers["Expires"] = "Thu, 01 Jan 1970 00:00:00"

	return response


