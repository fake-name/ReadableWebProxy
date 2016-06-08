

import time
import pprint
import json
import datetime
import calendar

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


	def __init__(self):

		input_settings = {
			'RABBIT_LOGIN'      : settings.NU_RABBIT_LOGIN,
			'RABBIT_PASWD'      : settings.NU_RABBIT_PASWD,
			'RABBIT_SRVER'      : settings.NU_RABBIT_SRVER,
			'RABBIT_VHOST'      : settings.NU_RABBIT_VHOST,
			'synchronous'       : False,
			'prefetch'          : 25,
			'master'            : True,
			'taskq_task'        : 'nuresponse.master.q',
			'taskq_response'    : 'nureleases.master.q',
			'poll_rate'         : 1.0 / 25,
		}

		self.data_in = WebMirror.OutputFilters.AmqpInterface.RabbitQueueHandler(input_settings)

		# output_settings = {
		# 	'RABBIT_LOGIN'      : settings.RABBIT_LOGIN,
		# 	'RABBIT_PASWD'      : settings.RABBIT_PASWD,
		# 	'RABBIT_SRVER'      : settings.RABBIT_SRVER,
		# 	'RABBIT_VHOST'      : settings.RABBIT_VHOST,
		# 	'taskq_task'     : 'task.master.q',
		# 	'taskq_response' : 'response.master.q',
		# }


		super().__init__(db_sess = db.get_db_session(postfix='nu_forwarder'))


	def __del__(self):
		db.delete_db_session(postfix='nu_forwarder')


	def do_release(self, input_data):
		if not 'nu_release' in input_data:
			with open("nu bad release %s.txt" % time.time(), "w") as fp:
				fp.write("Release packet that doesn't seem valid?\n\n")
				fp.write(pprint.pformat(input_data))

			raise ValueError("Wat?")

		if not isinstance(input_data, dict):

			with open("nu bad release %s.txt" % time.time(), "w") as fp:
				fp.write("Release packet that doesn't seem valid?\n\n")
				fp.write(pprint.pformat(input_data))

			raise ValueError("Wat?")

		item = input_data['nu_release']

		vol, chap, frag, postfix = extractVolChapterFragmentPostfix(item['releaseinfo'])


		ret = {
			'srcname'      : fix_string(item['groupinfo']),
			'series'       : fix_string(item['seriesname']),
			'vol'          : vol,
			'chp'          : chap,
			'frag'         : frag,
			'published'    : calendar.timegm(datetime.datetime.strptime(item['addtime'], '%Y-%m-%dT%H:%M:%S.%f').timetuple()),
			'itemurl'      : item['actual_target'],
			'postfix'      : fix_string(postfix),
			'author'       : None,
			'tl_type'      : 'translated',
			'match_author' : False,

			'nu_release'   : True

		}

		release = createReleasePacket(ret, beta=False)
		print("Packed release:", release)
		self.amqp_put_item(release)

	def go(self):
		empties = 0
		while 1:
			new = self.data_in.get_item()
			if new:
				new = json.loads(new)
				self.do_release(new)


				empties = 0
			else:
				empties += 1
				time.sleep(1)
			print("Looping!", empties)
			if empties > 10:
				print("returning?")
				self.data_in.close()
				self.data_in = None
				self._amqpint.close()
				self._amqpint = None
				return


if __name__ == '__main__':
	import logSetup
	logSetup.initLogging()

	intf = NuForwarder()
	print(intf)
	print(intf.go())


