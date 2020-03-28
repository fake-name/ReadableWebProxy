

import traceback
import pickle
import time
import datetime
from calendar import timegm

from flask import g
from flask import render_template
from flask import make_response
from flask import jsonify
from flask import request

from sqlalchemy.sql import text
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.expression import func
from tzlocal import get_localzone

from app import app
from app import auth
import common.database as db
import WebMirror.OfflineFilters.NewNetlocTracker as nnt

def url_state_update(sess, parameters):
	for row_updates in parameters:
		print(row_updates)

		assert 'id'  in row_updates
		assert 'old-ignore' in row_updates
		assert 'new-ignore' in row_updates

		row = sess.query(db.NewNetlocTracker).filter(db.NewNetlocTracker.id == row_updates['id']).scalar()
		assert row
		assert row.ignore == row_updates['old-ignore']

		row.ignore = row_updates['new-ignore']

	sess.commit()


	return {"error" : False,
			'message' : "Changes applied!"}


ops = {
	'update url states' : url_state_update,
	}

@app.route('/url_api/', methods=['GET', 'POST'])
@auth.login_required
def url_api():
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

	try:
		if 'op' in request.json and 'data' in request.json and request.json['op'] in ops:
			data = ops[request.json['op']](g.session, request.json['data'])
		else:
			data = {"wat": "wat"}
	except Exception as e:
		print("Failure in processing url api call!")
		traceback.print_exc()

		js = {
			"error"   : True,
			"message" : "Error: \n%s" % (traceback.format_exc(), )
		}
		resp = jsonify(js)
		resp.status_code = 200
		resp.mimetype="application/json"
		return resp

	response = jsonify(data)

	print("ResponseData: ", data)
	print("Response: ", response)

	response.status_code = 200
	response.mimetype="application/json"
	g.session.commit()
	g.session.expire_all()
	return response



@app.route('/urls/', methods=['GET'])
@auth.login_required
def url_view():

	scope   = request.args.get('scope', 'missing')
	ignored = request.args.get('ignore', 'exclude')

	nnt.filter_get_have_urls()

	# g.session.expire()
	query = g.session.query(db.NewNetlocTracker)
	if scope == 'missing':
		query = query.filter(db.NewNetlocTracker.have == False)

	if ignored == 'exclude':
		query = query.filter(db.NewNetlocTracker.ignore == False)


	items = query.all()
	g.session.commit()

	def keyf(item):
		if not item.extra:
			return (False, )
		is_wp = 1 if item.extra.get("is-wp", False) else 2
		nlr = item.netloc.split(".")
		nlr.reverse()

		flag = 7
		if "wordpress" in nlr:
			flag = 1
		if "blogspot" in nlr:
			flag = 2
		if "livejournal" in nlr:
			flag = 3
		if "dreamwidth" in nlr:
			flag = 4
		if "syosetu" in nlr:
			flag = 5
		if "wixsite" in nlr:
			flag = 6
		if "fandom" in nlr:
			flag = 7
		if "deviantart" in nlr:
			flag = 8

		ret = (is_wp, flag, nlr, item.example_url)
		print(ret)
		return ret

	items.sort(key=keyf)
	return render_template('url_listings.html',
						   netloc_items          = items,
						   # states         = states,
						   )


