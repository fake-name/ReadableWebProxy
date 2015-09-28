

from flask import render_template
from flask import make_response
from flask import request

import WebMirror.Engine
from sqlalchemy import Text
from sqlalchemy.sql.expression import cast
from app import app


import WebMirror.database as db

from app.utilities import paginate
import sqlalchemy.exc
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.expression import func

import WebMirror.API

def build_tsquery(in_str):
	args = in_str.split()
	args = [arg for arg in args if len(arg) >= 2]
	args = [arg.replace("!", " ").replace("?", " ").strip(",").strip() for arg in args]
	ret = " & ".join(args)
	return ret

def fetch_content(query_text, column, page):
	session = db.get_session()
	tsq = build_tsquery(query_text)
	query = session                                                                                         \
			.query(db.WebPages, func.ts_rank_cd(func.to_tsvector("english", column), func.to_tsquery(tsq))) \
			.filter(                                                                                        \
				func.to_tsvector("english", column).match(tsq, postgresql_regconfig='english')              \
				)                                                                                           \
			.order_by(func.ts_rank_cd(func.to_tsvector("english", column), func.to_tsquery(tsq)).desc())

	print("param: '%s'" % tsq)
	print(str(query.statement.compile(dialect=postgresql.dialect())))

	try:
		entries = paginate(query, page)

	except sqlalchemy.exc.ProgrammingError:
		print("ProgrammingError - Rolling back!")
		db.get_session().rollback()
		raise
	except sqlalchemy.exc.InternalError:
		print("InternalError - Rolling back!")
		db.get_session().rollback()
		raise
	except sqlalchemy.exc.OperationalError:
		print("InternalError - Rolling back!")
		db.get_session().rollback()
		raise

	return entries

def render_search(query_text, column, page, title):

	try:
		entries = fetch_content(query_text, column, page)
	except (sqlalchemy.exc.ProgrammingError,
			sqlalchemy.exc.InternalError,
			sqlalchemy.exc.OperationalError):

		return render_template('error.html', title = 'Error!', message = "Error! Invalid search string!")



	return render_template('search_results.html',
						   header          = title,
						   sequence_item   = entries,
						   page            = page
						   )


@app.route('/search/', methods=['GET'])
@app.route('/search/<int:page>', methods=['GET'])
def search(page=1):
	scope = request.args.get('scope')
	query = request.args.get('query')
	if not (scope and query):
		return render_template('search.html')

	if scope == "title":
		return render_search(query, db.WebPages.title, page, "Title search for '%s'" % query)
	if scope == "content":
		return render_search(query, db.WebPages.content, page, "Content search for '%s'" % query)

	else:
		return render_template('error.html', title = 'Error!', message = "Error! Invalid search scope!")


