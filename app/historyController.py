from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, send_file, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from itsdangerous import URLSafeTimedSerializer, BadSignature
from flask.ext.sqlalchemy import get_debug_queries
from flask.ext.babel import gettext
from datetime import datetime
# from guess_language import guess_language
from app import app, db, lm, babel
from .models import Users, Posts, SeriesChanges, TagsChanges, GenresChanges, AuthorChanges, IllustratorsChanges, TranslatorsChanges, ReleasesChanges, Covers, AlternateNamesChanges

from .confirm import send_email

from .apiview import handleApiPost, handleApiGet

import config
import os.path
from sqlalchemy.sql.expression import func


dispatch_table = {
	'description'  : SeriesChanges,
	'demographic'  : SeriesChanges,
	'type'         : SeriesChanges,
	'origin_loc'   : SeriesChanges,
	'orig_lang'    : SeriesChanges,
	'region'       : SeriesChanges,
	'license_en'   : SeriesChanges,
	'author'       : AuthorChanges,
	'illustrators' : IllustratorsChanges,
	'tag'          : TagsChanges,
	'genre'        : GenresChanges,
	'altnames'     : AlternateNamesChanges,
}

def rowToDict(row):
	return {x.name: getattr(row, x.name) for x in row.__table__.columns}

maskedRows = ['id', 'operation', 'srccol', 'changeuser', 'changetime']


def generateSeriesHistArray(inRows):
	inRows = [rowToDict(row) for row in inRows]
	inRows.sort(key = lambda x: x['id'])

	# Generate the list of rows we actually want to process by extracting out
	# the keys in the passed row, and masking out the ones we specifically don't want.
	if inRows:
		processKeys = [key for key in inRows[0].keys() if key not in maskedRows]
		processKeys.sort()
	else:
		processKeys = []

	# Prime the loop by building an empty dict to compare against
	previous = {key: None for key in processKeys}


	ret = []
	for row in inRows:
		rowUpdate = []
		for key in processKeys:
			if (row[key] != previous[key]) and (row[key] or previous[key]):
				item = {
					'changetime' : row['changetime'],
					'changeuser' : row['changeuser'],
					'operation'  : row['operation'],
					'item'       : key,
					'value'      : row[key]
					}
				previous[key] = row[key]
				# print(item)
				rowUpdate.append(item)
		if rowUpdate:
			ret.append(rowUpdate)

	return ret



# {
# 	'id': 2299,
# 	'changeuser': 2,
# 	'operation': 'U',
# 	'srccol': 2200,
# 	'changetime': datetime.datetime(2015, 5, 4, 19, 53, 6, 993234),

# 	'origin_loc': 'Japan',
# 	'demographic': '',
# 	'orig_lang': None,
# 	'title': 'Jinsei Reset Button',
# 	'type': 'Novel',
# 	'description': '<p>Based on the popular Vocaloid song "<a href="http://vocadb.net/S/8250">\nJinsei Reset Button</a>" by kemu.</p>'
# }


def renderHistory(histType, contentId):
	if histType not in dispatch_table:
		return render_template('not-implemented-yet.html', message='Error! Invalid history type.')

	table = dispatch_table[histType]

	if table == SeriesChanges:
		conditional = (table.srccol==contentId)
	else:
		conditional = (table.series==contentId)


	data = table                                   \
			.query                                 \
			.filter(conditional)                   \
			.order_by(table.changetime).all()


	seriesHist = None
	authorHist = None
	illustHist = None
	tagHist    = None
	genreHist  = None
	nameHist   = None

	if table == SeriesChanges:
		seriesHist = generateSeriesHistArray(data)
	if table == AuthorChanges:
		authorHist = data
	if table == IllustratorsChanges:
		illustHist = data
	if table == TagsChanges:
		tagHist = data
	if table == GenresChanges:
		genreHist = data
	if table == AlternateNamesChanges:
		nameHist = data

	return render_template('history.html',
			seriesHist = seriesHist,
			authorHist = authorHist,
			illustHist = illustHist,
			tagHist    = tagHist,
			genreHist  = genreHist,
			nameHist   = nameHist)
