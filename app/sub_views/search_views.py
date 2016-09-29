
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




def build_where_parameter(query_text, scope, sources):

	conditions = []
	params     = []

	if sources:
		tmp = []
		for source in sources:
			tmp.append("netloc = %s")
			params.append(source)
		conditions.append("(" + " or ".join(tmp) + ")")

	if scope == 'content':
		conditions.append("MATCH(%s)")
		params.append("@content " + query_text)
	else:
		conditions.append("MATCH(%s)")
		params.append("@title " + query_text)


	conditional = " and ".join(conditions)


	return conditional, params

def fetch_content(query_text, scope, sources, page_no):
	dbg = {"query_text" : query_text, "scope" : scope, "sources" : sources, "page_no" : page_no}
	print("query text: ", dbg)

	db = pymysql.connect(host   = settings.SPHINX_SERVER_IP,
						port    = settings.SPHINX_SERVER_port,
						user    = settings.SPHINX_SERVER_USER,
						passwd  = settings.SPHINX_SERVER_PASS,
						charset = 'utf8',
						db      = "")
	cur = db.cursor()


	where, params = build_where_parameter(query_text, scope, sources)

	print("Where: ", (where, params))

	qry = 'SELECT id, url, weight() FROM {db} WHERE {where} LIMIT 0, 1000 OPTION ranker=BM25, max_matches=1000'.format(db=settings.SPHINX_SERVER_TABLE, where=where)
	print("Query: ", qry)

	cur.execute(qry, params)
	rows = cur.fetchall()

	cur.close()
	db.close()

	return rows

def render_search(query_text, scope, sources, page_no):

	scopes = "Content" if scope == 'content' else 'Title'
	if isinstance(sources, str):
		sources = [sources]

	entries = fetch_content(query_text, scope, sources, page_no)

	return render_template('search_results.html',
						   header    = "%s search for '%s' - %s results" % (scopes, query_text, len(entries)),
						   results   = entries,
						   )

def render_search_page():
	print(request)
	print(request.args)
	print("test" in request.args)
	if "test" in request.args:
		print(request.args["test"])


	rules = WebMirror.rules.load_rules()

	netlocs = [item['starturls'] for item in rules if item['starturls']]
	netlocs = [list(set([urllib.parse.urlsplit(item).netloc for item in tmp])) for tmp in netlocs]

	[item.sort() for item in netlocs]
	netlocs.sort(key=lambda x: len(x))

	return render_template('search.html',
			netlocs = netlocs)


@app.route('/search/', methods=['GET'])
@app.route('/search/<int:page>', methods=['GET'])
def search(page=1):
	scope = request.args.get('scope')
	query = request.args.get('query')
	if not (scope and query):
		return render_search_page()

	if 'source-site' in request.args:
		try:
			request_str = request.args['source-site']
			request_str = urllib.parse.unquote(request_str)
			sources = json.loads(request_str)
		except ValueError:
			sources = None
	else:
		sources = None

	return render_search(query, scope, sources, page)

