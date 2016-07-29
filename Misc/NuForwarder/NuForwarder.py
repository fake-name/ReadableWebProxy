

import time
import urllib.parse
import pprint
import json
import datetime
import traceback
import os.path
import json
import calendar

import sqlalchemy.exc

from WebMirror.OutputFilters.util.MessageConstructors import fix_string
from WebMirror.OutputFilters.util.MessageConstructors import createReleasePacket
from WebMirror.OutputFilters.util.TitleParsers import extractVolChapterFragmentPostfix

import WebMirror.OutputFilters.FilterBase
import WebMirror.OutputFilters.util.MessageConstructors  as msgpackers
import WebMirror.OutputFilters.AmqpInterface
from WebMirror.OutputFilters.util.TitleParsers import extractTitle
import WebMirror.database as db

MIN_RATING = 2.5

########################################################################################################################
#
#	##     ##    ###    #### ##    ##     ######  ##          ###     ######   ######
#	###   ###   ## ##    ##  ###   ##    ##    ## ##         ## ##   ##    ## ##    ##
#	#### ####  ##   ##   ##  ####  ##    ##       ##        ##   ##  ##       ##
#	## ### ## ##     ##  ##  ## ## ##    ##       ##       ##     ##  ######   ######
#	##     ## #########  ##  ##  ####    ##       ##       #########       ##       ##
#	##     ## ##     ##  ##  ##   ###    ##    ## ##       ##     ## ##    ## ##    ##
#	##     ## ##     ## #### ##    ##     ######  ######## ##     ##  ######   ######
#
########################################################################################################################





import settings

class NuForwarder(WebMirror.OutputFilters.FilterBase.FilterBase):
	'''
		NU Updates are batched and only forwarded to the output periodically,
		to make timing attacks somewhat more difficult.
		It's still possible to look at execution edge-times, albeit somewhat
		smeared out by the multiple intercontinental message queues, but if that
		becomes an issue, it'll be simple enough to introduce fuzzy delays.

		Also, hurrah, I got my distributed RPC system going again, so that's nice.

		Example JSON response from distributed worker:
			{
			    "nu_release": {
			        "actual_target": "http://shiroyukitranslations.com/the-strongest-dan-god-chapter-63-dominating-business-channels/",
			        "seriesname": "The Strongest Dan God",
			        "outbound_wrapper": "http://www.novelupdates.com/extnu/134595/",
			        "groupinfo": "Shiroyukineko Translations",
			        "releaseinfo": "c63",
			        "addtime": "2016-05-30T04:16:41.351430",
			        "referrer": "https://www.novelupdates.com"
			    }
			}
	'''


	# Shut up the abstract base class.
	wanted_mimetypes = None
	want_priority    = None
	extractContent = None

	loggerPath = "Main.Forwarder.Nu"


	def __init__(self, connect=True):

		input_settings = {
			'RABBIT_LOGIN'      : settings.NU_RABBIT_LOGIN,
			'RABBIT_PASWD'      : settings.NU_RABBIT_PASWD,
			'RABBIT_SRVER'      : settings.NU_RABBIT_SRVER,
			'RABBIT_VHOST'      : settings.NU_RABBIT_VHOST,
			'synchronous'       : False,
			'prefetch'          : 1,
			'master'            : True,
			'taskq_task'        : 'nuresponse.master.q',
			'taskq_response'    : 'nureleases.master.q',
			'poll_rate'         : 1.0 / 25,
		}
		if connect:
			self.data_in = WebMirror.OutputFilters.AmqpInterface.RabbitQueueHandler(input_settings)

		# output_settings = {
		# 	'RABBIT_LOGIN'      : settings.RABBIT_LOGIN,
		# 	'RABBIT_PASWD'      : settings.RABBIT_PASWD,
		# 	'RABBIT_SRVER'      : settings.RABBIT_SRVER,
		# 	'RABBIT_VHOST'      : settings.RABBIT_VHOST,
		# 	'taskq_task'     : 'task.master.q',
		# 	'taskq_response' : 'response.master.q',
		# }

		self.name_lut, self.group_lut = load_lut()

		super().__init__(db_sess = db.get_db_session(postfix='nu_forwarder'), connect=connect)


	def __del__(self):
		db.delete_db_session(postfix='nu_forwarder')


	def insert_new_release(self, input_data):
		new = db.NuOutboundWrapperMap(
				client_id        = input_data['nu_release']['client_id'],
				client_key       = input_data['nu_release']['client_key'],
				seriesname       = input_data['nu_release']['seriesname'],
				releaseinfo      = input_data['nu_release']['releaseinfo'],
				groupinfo        = input_data['nu_release']['groupinfo'],
				referrer         = input_data['nu_release']['referrer'],
				outbound_wrapper = input_data['nu_release']['outbound_wrapper'],
				actual_target    = input_data['nu_release']['actual_target'],
			)

		while 1:
			try:
				self.db_sess.add(new)
				self.db_sess.commit()
				return

			except sqlalchemy.exc.InvalidRequestError:
				print("InvalidRequest error!")
				self.db_sess.rollback()
				traceback.print_exc()
			except sqlalchemy.exc.OperationalError:
				print("InvalidRequest error!")
				self.db_sess.rollback()
			except sqlalchemy.exc.IntegrityError:

				with open("nu_db_collisions.txt", "wa") as fp:
					fp.write(str(input_data))
					fp.write("\n")

				print("[upsertRssItems] -> Integrity error!")
				traceback.print_exc()
				self.db_sess.rollback()
				break


	def add_release(self, input_data):

		expected = [
			'seriesname',
			'releaseinfo',
			'groupinfo',
			'referrer',
			'outbound_wrapper',
			'actual_target',
			'client_id',
			'client_key',
		]

		# Patch incoming data using the series name LUT.
		if input_data['nu_release']['seriesname'] in self.name_lut:
			input_data['nu_release']['seriesname'] = self.name_lut[input_data['nu_release']['seriesname']]

		# I think the redirect unwrapper occationally times out, or something?
		if input_data['nu_release']['actual_target'].startswith('https://www.novelupdates.com'):
			return

		if not 'nu_release' in input_data:
			with open("nu bad release %s.txt" % time.time(), "w") as fp:
				fp.write("Release packet that doesn't seem valid?\n")
				fp.write(str(input_data))
				fp.write("\n")


			raise ValueError("Wat?")

		elif not isinstance(input_data, dict):

			with open("nu bad release %s.txt" % time.time(), "w") as fp:
				fp.write("Release packet that doesn't seem valid?\n")
				fp.write(str(input_data))
				fp.write("\n")

			raise ValueError("Wat?")

		elif not all([item in input_data['nu_release'] for item in expected]):
			with open("nu missing part release %s.txt" % time.time(), "w") as fp:
				fp.write("Release packet that doesn't seem valid?\n")
				fp.write(str(input_data))
				fp.write("\n")

			print(input_data['nu_release'])
			raise ValueError("Wat?")

		self.retrigger_page(input_data['nu_release']['actual_target'])

		have = self.db_sess.query(db.NuOutboundWrapperMap)                                                  \
				.filter(db.NuOutboundWrapperMap.client_id     == input_data['nu_release']['client_id'])     \
				.filter(db.NuOutboundWrapperMap.client_key    == input_data['nu_release']['client_key'])    \
				.filter(db.NuOutboundWrapperMap.seriesname    == input_data['nu_release']['seriesname'])    \
				.filter(db.NuOutboundWrapperMap.releaseinfo   == input_data['nu_release']['releaseinfo'])   \
				.filter(db.NuOutboundWrapperMap.groupinfo     == input_data['nu_release']['groupinfo'])     \
				.filter(db.NuOutboundWrapperMap.actual_target == input_data['nu_release']['actual_target']) \
				.scalar()
		if not have:
			self.insert_new_release(input_data)

	def process_inbound_messages(self):
		empties = 0
		while 1:
			new = self.data_in.get_item()
			if new:
				if isinstance(new, bytes):
					new = new.decode("utf-8")
				new = json.loads(new)
				self.add_release(new)

				empties = 0
			else:
				empties += 1
				time.sleep(1)
			print("Looping!", empties)
			if empties > 10:
				print("returning?")
				return

	def go(self):
		try:
			self.process_inbound_messages()
			self.fix_names()
			self.consolidate_validated()
			self.emit_verified_releases()
		finally:
			self.close()

	def fix_names(self):
		for old, new in self.name_lut.items():
			have = self.db_sess.query(db.NuOutboundWrapperMap)         \
				.filter(db.NuOutboundWrapperMap.seriesname     == old) \
				.all()
			for row in have:
				try:
					assert row.seriesname == old
					row.seriesname = new
					self.log.info("Fixing name row: %s -> %s", old, row.seriesname)

					self.db_sess.commit()
				except sqlalchemy.exc.IntegrityError:
					self.log.error("Failure")
					traceback.print_exc()
					self.db_sess.rollback()
					self.db_sess.delete(row)
					self.db_sess.commit()

		for old, new in self.group_lut.items():
			have = self.db_sess.query(db.NuOutboundWrapperMap)         \
				.filter(db.NuOutboundWrapperMap.groupinfo     == old) \
				.all()
			for row in have:
				try:
					assert row.groupinfo == old
					row.groupinfo = new
					self.log.info("Fixing group row: %s -> %s", old, row.groupinfo)

					self.db_sess.commit()
				except sqlalchemy.exc.IntegrityError:
					self.log.error("Failure")
					traceback.print_exc()
					self.db_sess.rollback()
					self.db_sess.delete(row)
					self.db_sess.commit()



	def do_release(self, item):

		vol, chap, frag, postfix = extractVolChapterFragmentPostfix(item['releaseinfo'])


		ret = {
			'srcname'      : fix_string(item['groupinfo']),
			'series'       : fix_string(item['seriesname']),
			'vol'          : vol,
			'chp'          : chap,
			'frag'         : frag,
			'published'    : calendar.timegm(item['addtime'].timetuple()),
			'itemurl'      : item['actual_target'],
			'postfix'      : fix_string(postfix),
			'author'       : None,
			'tl_type'      : 'translated',
			'match_author' : False,

			'nu_release'   : True

		}

		release = createReleasePacket(ret, beta=False)
		# print("Packed release:", release)
		self.amqp_put_item(release)


	def emit_verified_releases(self):
			have = self.db_sess.query(db.NuOutboundWrapperMap)     \
				.filter(db.NuOutboundWrapperMap.validated == True) \
				.all()
			agg_releases = {}
			for row in have:
				try:
					key = (row.seriesname, row.releaseinfo, row.groupinfo)
					if not key in agg_releases:

						agg_releases[key] = {
							'releaseinfo'   : row.releaseinfo,
							'groupinfo'     : row.groupinfo,
							'seriesname'    : row.seriesname,
							'addtime'       : row.released_on,
							'actual_target' : row.actual_target,
						}
					else:
						assert str(row.releaseinfo)   == agg_releases[key]['releaseinfo'],   "Wat? (%s) %s -> %s" % (
							row.releaseinfo   == agg_releases[key]['releaseinfo'], row.releaseinfo,     agg_releases[key]['releaseinfo'])
						assert str(row.groupinfo)     == agg_releases[key]['groupinfo'],     "Wat? (%s) %s -> %s" % (
							row.groupinfo     == agg_releases[key]['groupinfo'], row.groupinfo,         agg_releases[key]['groupinfo'])
						assert str(row.seriesname)    == agg_releases[key]['seriesname'],    "Wat? (%s) %s -> %s" % (
							row.seriesname    == agg_releases[key]['seriesname'], row.seriesname,       agg_releases[key]['seriesname'])

						if 'blogspot' in row.actual_target:
							# Blogspot is ANNOYING, and has a bajillion possible TLDs that all resolve the same place.
							# Therefore, ignore the TLD from the netloc
							url1 = urllib.parse.urlsplit(row.actual_target)
							url2 = urllib.parse.urlsplit(agg_releases[key]['actual_target'])
							nl1 = url1.netloc.split(".")
							nl2 = url2.netloc.split(".")
							l = max(min(len(nl1), len(nl2))-1, 1)
							print("l", l)

							url1 = (url1.scheme, nl1[0:l], url1.path, url1.query, url1.fragment)
							url2 = (url2.scheme, nl2[0:l], url2.path, url2.query, url2.fragment)
							assert url1 == url2, "wat? %s -> %s" % (url1, url2)
						elif 'docs.google.com' in row.actual_target:
							# We don't care about the query or fragment for google doc entries.
							url1 = urllib.parse.urlsplit(row.actual_target)
							url2 = urllib.parse.urlsplit(agg_releases[key]['actual_target'])
							url1 = (url1.scheme, url1.netloc, url1.path)
							url2 = (url2.scheme, url2.netloc, url2.path)
							assert url1 == url2, "wat? %s -> %s" % (url1, url2)

						else:
							assert str(row.actual_target) == agg_releases[key]['actual_target'], "Wat? (%s) %s -> %s" % (row.actual_target == agg_releases[key]['actual_target'], row.actual_target, agg_releases[key]['actual_target'])
				except AssertionError:
					agg_releases[key] = None
				except TypeError:
					agg_releases[key] = None


			for release in agg_releases.values():
				if release:
					self.do_release(release)
			# print("Valid releases:")
			# print(agg_releases)


	def consolidate_validated(self):

		rows = self.db_sess.query(db.NuOutboundWrapperMap).all()
		rowlut = {}
		for row in rows:
			key = row.seriesname, row.releaseinfo, row.groupinfo, row.actual_target
			if not key in rowlut:
				rowlut[key] = []
			rowlut[key].append(row)

		for valueset in [tmp for tmp in rowlut.values() if len(tmp) > 1]:
			if not all(x.validated == valueset[0].validated for x in valueset):
				if any(x.validated == True for x in valueset):
					for val in valueset:
						val.validated = True
		self.db_sess.commit()

	def close(self):
		print("Closing")
		self.data_in.close()
		self.data_in = None
		self._amqpint.close()
		self._amqpint = None


	def __del__(self):
		try:
			self.close()
		except Exception:
			pass


	def _go(self, *args, **kwargs):
		self.go()

def load_lut():
	outf = os.path.join(os.path.split(__file__)[0], 'name_fix_lut.json')
	jctnt = open(outf).read()
	lut = json.loads(jctnt)
	return lut



if __name__ == '__main__':
	import logSetup
	logSetup.initLogging()

	# intf = NuForwarder()
	# intf.go()
	#print(load_lut())
	intf = NuForwarder(connect=False)
	intf.fix_names()
	# intf.consolidate_validated()
	# try:
	# 	intf.fix_names()
	# finally:
	# 	intf.close()
	# intf.go()


