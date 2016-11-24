

from flask import g
from flask import render_template
from flask import make_response
from flask import request
from flask import jsonify

import pickle
import time
import json
import string
import datetime
import urllib.parse
from calendar import timegm

from sqlalchemy.sql import text
from app import app

from Misc.NuForwarder import NuHeader

import common.database as db

from app.utilities import paginate
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.expression import func
from tzlocal import get_localzone
import WebMirror.API
from sqlalchemy import desc
from sqlalchemy.sql.expression import nullslast



def abbreviate(instr):
	instr = "".join([char for char in instr if char in string.ascii_letters + " "])
	segs = instr.split(" ")
	segs = [seg[0] for seg in segs if seg]
	ret = "".join(segs).lower()
	return "" if len(ret) < 2 else ret

def add_highlight(from_name, from_chp, from_group, namestr):
	t1 = abbreviate(from_group)
	t2 = abbreviate(from_name)

	from_name  = from_name.replace("'", " ")  + " " + from_name.replace("'", "")
	from_chp   = from_chp.replace("'", " ")   + " " + from_chp.replace("'", "")
	from_chp   = from_chp + " " + "".join([letter if letter in "01234567890." else " " for letter in from_chp])


	from_group = from_group.replace("'", " ") + " " + from_group.replace("'", "")
	splitstr = from_name + " " + from_group + " " + from_chp + " " + "".join([char for char in from_chp if char in " 0123456789"]) + \
		" " + "".join([char for char in from_chp if char in string.ascii_letters + " "]) + \
		" " + t1 + " " + t2
	highlights = [val for val in splitstr.lower().split(" ") if val and (len(val) > 1 or any([char for char in val if char in "0123456789"]))]

	highlights.sort(key=lambda x: len(x), reverse=True)

	namestr = namestr.lower()

	for highlight in highlights:
		if highlight in namestr:
			splitted = namestr.split(highlight)
			if len(splitted) > 1:
				namestr = ("<b>"+highlight+"</b>").join(namestr.split(highlight))

	return namestr


def get_nu_items(sess, selector):

	intf = NuHeader.NuHeader()
	intf.fix_names()


	new_items = sess.query(db.NuReleaseItem)
	new_items = new_items.filter(db.NuReleaseItem.validated == True)

	if selector == "verified":
		new_items = new_items.filter(db.NuReleaseItem.reviewed == True)
		new_items = new_items.filter(db.NuReleaseItem.actual_target != None)
	elif selector == "all":
		new_items = new_items.filter(db.NuReleaseItem.actual_target != None)
	elif selector == "unverified" or selector == None:
		new_items = new_items.filter(db.NuReleaseItem.reviewed == False)
		new_items = new_items.filter(db.NuReleaseItem.actual_target != None)

	new_items = new_items.order_by(nullslast(desc(db.NuReleaseItem.validated_on)))
	new_items = new_items.limit(200).all()


	return new_items

def toggle_row(sess, rid, oldv, newv):

	row = sess.query(db.NuReleaseItem)     \
		.filter(db.NuReleaseItem.id == rid) \
		.scalar()

	if not row:
		print("Row missing!")
	else:
		assert(row.reviewed == oldv)
		assert(oldv != newv)
		print("Row: ", rid, oldv, newv, row.seriesname, row.releaseinfo)
		row.reviewed = newv


def release_validity_toggle(sess, data):
	sess.expire_all()
	for change in data:
		toggle_row(sess, change['id'], change['old'], change['new'])
		print("Change:", change)

	sess.commit()
	sess.expire_all()

	return {"error" : False,
			'message' : "Changes applied!"}


def delete_row(sess, del_id):

	row = sess.query(db.NuReleaseItem)     \
		.filter(db.NuReleaseItem.id == del_id) \
		.scalar()
	if not row:
		print("Row missing!")
	else:
		print("Row: ", row)
		for subitem in row.resolved:
			sess.delete(subitem)
		row.validated_on = None
		row.validated = False
		row.actual_target = None


def release_delete(sess, data):
	sess.expire_all()
	for change in data:
		delete_row(sess, change['del_id'])
		print("Change:", change)

	sess.commit()

	sess.expire_all()

	return {"error" : False,
			'message' : "Changes applied!"}

ops = {
	'nu release validity update' : release_validity_toggle,
	'nu release delete' : release_delete,
	}


@app.route('/nu_releases/', methods=['GET'])
def nu_view():

	release_selector = request.args.get('view')

	session = g.session
	session.expire_all()
	session.commit()
	session.expire_all()
	new = get_nu_items(g.session, release_selector)
	session.commit()
	new.sort(key=lambda x: x.seriesname)
	new.sort(key=lambda x: '...' in x.seriesname)
	new.sort(key=lambda x: ('http://www.novelupdates.com' in x.actual_target if x.actual_target else False))

	new_with_markup = []
	for row in new:
		highlight = add_highlight(row.seriesname, row.releaseinfo, row.groupinfo, row.actual_target)
		new_with_markup.append((highlight, row))

	response = make_response(render_template('nu_releases.html',
						   new              = new_with_markup,
						   release_selector = release_selector,
						   ))
	session.expire_all()

	response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
	response.headers["Pragma"] = "no-cache"
	response.headers["Expires"] = "Thu, 01 Jan 1970 00:00:00"

	session.commit()
	session.expire_all()
	return response

@app.route('/nu_api/', methods=['GET', 'POST'])
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

	# print("response", response)
	# response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
	# response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
	# response.headers["Pragma"] = "no-cache"
	# response.headers["Expires"] = "Thu, 01 Jan 1970 00:00:00"

	print("ResponseData: ", data)
	print("Response: ", response)

	response.status_code = 200
	response.mimetype="application/json"
	g.session.commit()
	return response


