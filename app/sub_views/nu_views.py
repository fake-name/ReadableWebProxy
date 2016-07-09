
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

def aggregate_nu_items(in_rows):
	agg = {}
	for row in in_rows:
		uniq = (row.seriesname, row.releaseinfo, row.actual_target)
		if not uniq in agg:
			agg[uniq] = []
		agg[uniq].append(row)

	for rowset in agg.values():
		assert(all([rowset[0].seriesname == row.seriesname for row in rowset]))
		assert(all([rowset[0].outbound_wrapper == row.outbound_wrapper for row in rowset]))
		assert(all([rowset[0].groupinfo == row.groupinfo for row in rowset]))
		assert(all([rowset[0].releaseinfo == row.releaseinfo for row in rowset]))
		assert(all([rowset[0].actual_target == row.actual_target for row in rowset]))

	return list(agg.values())


def get_nu_items(sess, selector):
	new_items = sess.query(db.NuOutboundWrapperMap)
	if selector == "unverified" or selector == None:
		new_items = new_items.filter(db.NuOutboundWrapperMap.validated == False)
	elif selector == "verified":
		new_items = new_items.filter(db.NuOutboundWrapperMap.validated == True)
	elif selector == "all":
		pass

	new_items = new_items.all()

	new_items = aggregate_nu_items(new_items)

	return new_items

def toggle_row(sess, rid, oldv, newv):

	row = sess.query(db.NuOutboundWrapperMap)     \
		.filter(db.NuOutboundWrapperMap.id == rid) \
		.one()
	assert(row.validated == oldv)
	assert(oldv != newv)
	row.validated = newv

def release_validity_toggle(sess, data):
	sess.expire_all()
	for change in data:
		toggle_row(sess, change['id'], change['old'], change['new'])
		print("Change:", change)

	sess.commit()

	sess.expire_all()

	return {"error" : False,
			'message' : "Changes applied!"}

ops = {
	'nu release validity update' : release_validity_toggle,
	}


@app.route('/nu_releases/', methods=['GET'])
def nu_view():

	release_selector = request.args.get('view')

	session = g.session
	session.expire_all()
	session.commit()
	new = get_nu_items(g.session, release_selector)
	session.commit()
	new.sort(key=lambda x: x[0].seriesname)
	new.sort(key=lambda x: '...' in x[0].seriesname)
	new.sort(key=lambda x: 'https://www.novelupdates.com' in x[0].actual_target)

	response = make_response(render_template('nu_releases.html',
						   new          = new,
						   release_selector = release_selector,
						   ))
	session.expire_all()

	response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
	response.headers["Pragma"] = "no-cache"
	response.headers["Expires"] = "Thu, 01 Jan 1970 00:00:00"
	return response

@app.route('/nu_api/', methods=['GET'])
def nu_api_get():
	response = make_response(jsonify({"error" : True, "message" : "This endpoint only accepts POST requests."}))
	response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
	response.headers["Pragma"] = "no-cache"
	response.headers["Expires"] = "Thu, 01 Jan 1970 00:00:00"
	return response


@app.route('/nu_api/', methods=['POST'])
def nu_api():
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

	print("API Request!")
	print("session:", g.session)
	print("Request method: ", request.method)
	print("Request json: ", request.json)

	if 'op' in request.json and 'data' in request.json and request.json['op'] in ops:
		data = ops[request.json['op']](g.session, request.json['data'])

	else:

		data = {"wat": "wat"}

	g.session.expire_all()
	# response = make_response(jsonify(data))
	response = jsonify(data)

	print("response", response)
	response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
	response.headers["Pragma"] = "no-cache"
	response.headers["Expires"] = "Thu, 01 Jan 1970 00:00:00"

	return response


