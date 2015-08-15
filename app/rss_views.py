from flask import render_template
from flask import flash
from flask import redirect
from flask import session
from flask import url_for
from flask import request
from flask import g
from flask import jsonify
from flask import send_file
from flask import abort
from flask.ext.babel import gettext
# from guess_language import guess_language
from app import app
from app import db
from app import lm
from app import babel

from app.models import Users
from app.models import Posts
from app.models import Series
from app.models import Tags
from app.models import Genres
from app.models import Author
from app.models import Illustrators
from app.models import Translators
from app.models import Releases
from app.models import Covers
from app.models import Watches
from app.models import AlternateNames
from app.models import Feeds
from app.models import Releases

from app.confirm import send_email


from app.sub_views.search import execute_search

from app.historyController import renderHistory
import os.path
from sqlalchemy.sql.expression import func
from sqlalchemy import desc

from sqlalchemy.orm import joinedload
import traceback


import WebMirror.database as db


@app.route('/feeds/<page>')
@app.route('/feeds/<int:page>')
@app.route('/feeds/')
def renderFeedsTable(page=1):

	feeds = db.get_session().query(db.Feeds)       \
		.order_by(desc(Feeds.published))


	# feeds = feeds.options(joinedload('tags'))
	# feeds = feeds.options(joinedload('authors'))



	if feeds is None:
		flash(gettext('No feeds? Something is /probably/ broken!.'))
		return redirect(url_for('renderFeedsTable'))

	feed_entries = feeds.paginate(page, app.config['SERIES_PER_PAGE'], False)

	return render_template('feeds.html',
						   sequence_item   = feed_entries,
						   page            = page
						   )