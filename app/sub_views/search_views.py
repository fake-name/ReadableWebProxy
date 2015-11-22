

from flask import render_template
from flask import request
import json
import urllib.parse

from app import app

import traceback
import WebMirror.database as db

from app.utilities import paginate
import sqlalchemy.exc
from sqlalchemy.sql.expression import func
from sqlalchemy.dialects import postgresql

import WebMirror.rules

def build_tsquery(in_str):
	args = in_str.split()
	args = [arg for arg in args if len(arg) >= 2]
	args = [arg.replace("!", " ").replace("?", " ").strip(",").strip() for arg in args]
	ret = " & ".join(args)
	return ret

def fetch_content(query_text, column, text_column, page, sources=None):
	session = db.get_session()
	tsq = build_tsquery(query_text)
	search = None
	if column == db.WebPages.title:
		query = session                                                                                         \
				.query(db.WebPages, func.ts_rank_cd(func.to_tsvector("english", column), func.to_tsquery(tsq))) \
				.filter(                                                                                        \
					func.to_tsvector("english", column).match(tsq, postgresql_regconfig='english')              \
					)                                                                                           \
				.order_by(func.ts_rank_cd(func.to_tsvector("english", column), func.to_tsquery(tsq)).desc())

	elif column == db.WebPages.tsv_content:
		query = session                                                                                         \
				.query(db.WebPages, func.ts_rank_cd(column, func.to_tsquery(tsq)))                              \
				.filter( column.match(tsq) )

		if "'" in query_text or '"' in query_text:
			search = query_text.replace("!", " ").replace("?", " ").replace("'", " ").replace('"', " ").replace(',', " ").replace('.', " ").strip()
			while "  " in search:
				search = search.replace("  ", " ")
			search = search.strip()
			search = '%{}%'.format(search.lower())
			query = query.filter( func.lower(text_column).like(search) )

		query = query.order_by(func.ts_rank_cd(column, func.to_tsquery(tsq)).desc())

		if sources:
			query = query.filter(db.WebPages.netloc.in_(sources))

	else:
		raise ValueError("Wat?")

	print(str(query.statement.compile(dialect=postgresql.dialect())))
	print("param: '%s', '%s', '%s'" % (tsq, sources, search))

	try:
		entries = paginate(query, page, per_page=50)

	except sqlalchemy.exc.ProgrammingError:
		traceback.print_exc()
		print("ProgrammingError - Rolling back!")
		db.get_session().rollback()
		raise
	except sqlalchemy.exc.InternalError:
		traceback.print_exc()
		print("InternalError - Rolling back!")
		db.get_session().rollback()
		raise
	except sqlalchemy.exc.OperationalError:
		traceback.print_exc()
		print("InternalError - Rolling back!")
		db.get_session().rollback()
		raise

	return entries

def render_search(query_text, column, text_column, page, title):
	print(request)
	if 'source-site' in request.args:
		try:
			request_str = request.args['source-site']
			request_str = urllib.parse.unquote(request_str)
			sources = json.loads(request_str)
		except ValueError:
			sources = None
	else:
		sources = None


	if isinstance(sources, str):
		sources = [sources]

	try:
		entries = fetch_content(query_text, column, text_column, page, sources=sources)
	except (sqlalchemy.exc.ProgrammingError,
			sqlalchemy.exc.InternalError,
			sqlalchemy.exc.OperationalError):

		return render_template('error.html', title = 'Error!', message = "Error! Invalid search string!")



	return render_template('search_results.html',
						   header          = title,
						   sequence_item   = entries,
						   page            = page
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

	if scope == "title":
		return render_search(query, db.WebPages.title, db.WebPages.title, page, "Title search for '%s'" % query)
	if scope == "content":
		return render_search(query, db.WebPages.tsv_content, db.WebPages.content, page, "Content search for '%s'" % query)

	else:
		return render_template('error.html', title = 'Error!', message = "Error! Invalid search scope!")


