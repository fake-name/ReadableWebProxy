
import calendar
import datetime
import json
import os
import os.path
import shutil
import traceback
from concurrent.futures import ThreadPoolExecutor

import urllib.error
import urllib.parse

from sqlalchemy import and_
from sqlalchemy import or_
import sqlalchemy.exc
from sqlalchemy_continuum.utils import version_table

if __name__ == "__main__":
	import logSetup
	logSetup.initLogging()

import common.database as db


import flags
import pprint
import config

import WebMirror.OutputFilters.rss.FeedDataParser
import WebMirror.OutputFilters.util.feedNameLut
import astor

def add_name(sess, netloc, nametxt):
	check = sess.query(db.RssParserFunctions) \
		.filter(db.RssParserFunctions.feed_name == nametxt) \
		.scalar()

	if not check:
		print("Wat?", nametxt)
		return


	have = sess.query(db.RssFeedFuncLut) \
		.filter(db.RssFeedFuncLut.feed_netloc == netloc) \
		.scalar()
	if have:
		assert(check.id == have.feed_id)
	else:
		new = db.RssFeedFuncLut(
				feed_netloc = netloc,
				feed_id     = check.id,
			)
		sess.add(new)
		sess.commit()

def update_func(sess, feed_name, fcont):
	res = sess.query(db.RssParserFunctions) \
		.filter(db.RssParserFunctions.feed_name == feed_name) \
		.scalar()

	if res:
		print("have:", feed_name)
		if not res.func == fcont:
			print("Contents mismatch!", feed_name)
			res.func = fcont
			sess.commit()

		print("Func: ", res.get_func())
	else:
		new = db.RssParserFunctions(
				version   = 1,
				feed_name = feed_name,
				enabled   = False,
				func      = fcont,
			)
		print("Adding ", feed_name)
		sess.add(new)
		sess.commit()

def exposed_import_feed_parse_funcs():
	'''
	Import the feed parsing functions into the database.
	'''

	sess = db.get_db_session()

	parse_map = WebMirror.OutputFilters.rss.FeedDataParser.RSS_PARSE_FUNCTION_MAP
	for key, func in parse_map.items():
		func_str = astor.to_source(astor.code_to_ast(func), indent_with="	")
		update_func(sess, key, func_str)

	name_map = WebMirror.OutputFilters.util.feedNameLut.mapper

	for key, val in name_map.items():
		print(key, val)
		add_name(sess, key, val)
