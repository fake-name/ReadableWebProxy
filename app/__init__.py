import os
from flask import Flask
from flask.json import JSONEncoder
from flask.ext.login import LoginManager

from flask.ext.babel import Babel, lazy_gettext
from flask_wtf.csrf import CsrfProtect
from flask_debugtoolbar import DebugToolbarExtension
from config import basedir
import datetime
from babel.dates import format_datetime

import urllib.parse

class AnonUser():
	def is_authenticated(self):
		return False
	def is_active(self):
		return False
	def is_admin(self):
		return False
	def is_mod(self):
		return False
	def is_anonymous(self):
		return True
	def get_id(self):
		return None



app = Flask(__name__)

import sys
if "debug" in sys.argv:
	print("Flask running in debug mode!")
	app.debug = True
app.config.from_object('config.BaseConfig')

lm = LoginManager()
lm.anonymous_user = AnonUser
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = lazy_gettext('Please log in to access this page.')

babel = Babel(app)
CsrfProtect(app)

if "debug" in sys.argv:
	print("Installing debug toolbar!")
	toolbar = DebugToolbarExtension(app)

if not app.debug:
	import logging
	from logging.handlers import RotatingFileHandler
	file_handler = RotatingFileHandler('tmp/wlnupdates.log', 'a', 1 * 1024 * 1024, 10)
	file_handler.setLevel(logging.INFO)
	file_handler.setFormatter(logging.Formatter(
		'%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	app.logger.addHandler(file_handler)
	app.logger.setLevel(logging.INFO)
	app.logger.info('wlnupdates startup')


from app import views


@app.context_processor
def utility_processor():

	def format_date(value, format='medium'):

		return format_datetime(value, "EE yyyy.MM.dd")

	def date_now():
		return format_datetime(datetime.datetime.today(), "yyyy/MM/dd, hh:mm:ss")

	def ago(then):
		if then == None:
			return "Never"
		now = datetime.datetime.now()
		delta = now - then

		d = delta.days
		h, s = divmod(delta.seconds, 3600)
		m, s = divmod(s, 60)
		labels = ['d', 'h', 'm', 's']
		dhms = ['%s %s' % (i, lbl) for i, lbl in zip([d, h, m, s], labels)]
		for start in range(len(dhms)):
			if not dhms[start].startswith('0'):
				break
		for end in range(len(dhms)-1, -1, -1):
			if not dhms[end].startswith('0'):
				break
		return ', '.join(dhms[start:end+1])




	return dict(
			format_date        = format_date,
			date_now           = date_now,
			ago                = ago,
			)

