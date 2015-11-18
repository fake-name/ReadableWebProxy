
#!/usr/bin/python
# from profilehooks import profile
import urllib.parse
import re
import json
import logging
import WebMirror.OutputFilters.util.feedNameLut as feedNameLut
from WebMirror.OutputFilters import AmqpInterface
import settings
from WebMirror.util.titleParse import TitleParser


from WebMirror.OutputFilters.util.MessageConstructors import buildReleaseMessage
from WebMirror.OutputFilters.util.TitleParsers import extractChapterVol
from WebMirror.OutputFilters.util.TitleParsers import extractVolChapterFragmentPostfix
from WebMirror.OutputFilters.util.TitleParsers import extractChapterVolFragment

# pylint: disable=W0201
import WebMirror.OutputFilters.FilterBase
import flags

skip_filter = [
	"www.baka-tsuki.org",
	"re-monster.wikia.com",
]



class DataParser(WebMirror.OutputFilters.FilterBase.FilterBase):

	amqpint = None
	amqp_connect = True

	def __init__(self, transfer=True, debug_print=False, **kwargs):
		super().__init__(**kwargs)

		self.dbg_print = debug_print
		self.transfer = transfer
		self.names = set()

	####################################################################################################################################################
	# Sousetsuka
	####################################################################################################################################################
	def extractSousetsuka(self, item):
		# check that 'Desumachi' is in the tags? It seems to work well enough now....
		desumachi_norm  = re.search(r'^(Death March kara Hajimaru Isekai Kyo?usoukyoku) (\d+)\W(\d+)$', item['title'])
		desumachi_extra = re.search(r'^(Death March kara Hajimaru Isekai Kyusoukyoku)(?: Chapter)? (\d+)\W(Intermission.*?)$', item['title'])

		if desumachi_norm:
			print(desumachi_norm.groups())

		ret = False
		if desumachi_norm:
			series = desumachi_norm.group(1)
			vol    = desumachi_norm.group(2)
			chp    = desumachi_norm.group(3)
			ret = buildReleaseMessage(raw_item=item, series=series, vol=vol, chap=chp)


		elif desumachi_extra:
			series  = desumachi_extra.group(1)
			vol     = desumachi_extra.group(2)
			postfix = desumachi_extra.group(3)
			ret = buildReleaseMessage(item, series, vol, postfix=postfix)

		return ret

	####################################################################################################################################################
	# お兄ちゃん、やめてぇ！ / Onii-chan Yamete
	####################################################################################################################################################
	def extractOniichanyamete(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if       'Jashin Average'   in item['title'] \
				or 'Cthulhu Average'  in item['title'] \
				or 'Evil God Average' in item['tags']  \
				or 'jashin'           in item['tags']:

			if "Side Story" in item['title']:
				return False
			return buildReleaseMessage(item, 'Evil God Average', vol, chp, frag=frag)

		if 'Tilea’s Worries' in item['title']:

			return buildReleaseMessage(item, 'Tilea\'s Worries', vol, chp, postfix=postfix)


		if 'I’m Back in the Other World' in item['title']:
			return buildReleaseMessage(item, 'I\'m Back in the Other World', vol, chp)

		if 'Kazuha Axeplant’s Third Adventure:' in item['title']:
			return buildReleaseMessage(item, 'Kazuha Axeplant\'s Third Adventure', vol, chp)

		elif 'otoburi' in item['tags'] or 'Otoburi' in item['tags']:
			# Arrrgh, the volume/chapter structure for this series is a disaster!
			# I resent having to do this....
			volume_lut = {
				# Child Chapter
				"3 years old"                  : 1,
				"5 years old"                  : 1,
				"6 years old"                  : 1,
				"7 years old"                  : 1,
				"12 years old"                 : 1,
				"12 years old"                 : 1,
				"14 years old"                 : 1,
				"15 years old"                 : 1,
				"16 years old"                 : 1,

				# Academy Chapter (First Year First Semester)
				"School Entrance Ceremony"     : 2,
				"First Year First Semester"    : 2,
				"1st Year 1st Semester"        : 2,

				# Academy Chapter (Summer Vacation)
				"Summer Vacation"              : 3,
				"Summer Vacation 2nd Half"     : 3,
				"Summer Vacation Last"         : 3,

				# Academy Chapter (First Year Second Semester)
				"First Year Second Semester"   : 4,

				# Job Chapter
				"Recuperating?"                : 5,
				"Wedding Preparations?"        : 5,
				"Newlywed Life"                : 5,

				# Major Cleanup Chapter
				"Cleanup"                      : 6,
				"My Lord’s Engagement"         : 6,
				"The Winter is Almost Here"    : 6,
				"Experiments and Preparations" : 6,
				"Engagement Party"             : 6,

				# Dilemma Chapter
				"In the Middle of a Fight?"    : 7,
				"In the Middle of Reflecting"  : 7,
			}

			for chp_key in volume_lut.keys():
				if chp_key.lower() in item['title'].lower():
					return buildReleaseMessage(item, 'Otome Game no Burikko Akuyaku Onna wa Mahou Otaku ni Natta', volume_lut[chp_key], chp)

		# else:
		# 	# self.log.warning("Cannot decode item:")
		# 	# self.log.warning("%s", item['title'])
		# 	# self.log.warning("Cannot decode item: '%s'", item['title'])
		# 	# print(item['tags'])
		return False



	####################################################################################################################################################
	# Natsu TL
	####################################################################################################################################################
	def extractNatsuTl(self, item):
		meister  = re.search(r'^(Magi Craft Meister) Volume (\d+) Chapter (\d+)$', item['title'])
		if meister:
			series = meister.group(1)
			vol    = meister.group(2)
			chp    = meister.group(3)
			return buildReleaseMessage(item, series, vol, chp)
		return False



	####################################################################################################################################################
	# TheLazy9
	####################################################################################################################################################
	def extractTheLazy9(self, item):
		kansutoppu  = re.search(r'^(Kansutoppu!) Chapter (\d+)$', item['title'])
		garudeina  = re.search(r'^(Garudeina Oukoku Koukoku Ki) Chapter (\d+): Part (\d+)$', item['title'])
		# meister  = re.search(r'^(Magi Craft Meister) Volume (\d+) Chapter (\d+)$', item['title'])

		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if kansutoppu:
			series = kansutoppu.group(1)
			vol    = None
			chp    = kansutoppu.group(2)
			return buildReleaseMessage(item, series, vol, chp)
		if garudeina:
			series = garudeina.group(1)
			vol    = None
			chp    = garudeina.group(2)
			frag   = garudeina.group(3)

			return buildReleaseMessage(item, series, vol, chp, frag=frag)

		if "Astarte's Knight" in item['tags']:
			return buildReleaseMessage(item, 'Astarte\'s Knight', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# Yoraikun
	####################################################################################################################################################
	def extractYoraikun(self, item):
		if 'The Rise of the Shield Hero' in item['tags']:
			chp, vol = extractChapterVol(item['title'])
			if vol == 0:
				vol = None
			return buildReleaseMessage(item, 'The Rise of the Shield Hero', vol, chp)
		elif 'Konjiki no Wordmaster' in item['tags']:
			chp, vol = extractChapterVol(item['title'])
			if vol == 0:
				vol = None
			return buildReleaseMessage(item, 'Konjiki no Wordmaster', vol, chp)
		return False

	####################################################################################################################################################
	# FlowerBridgeToo
	####################################################################################################################################################
	def extractFlowerBridgeToo(self, item):
		# Seriously, you were too lazy to type out the *tags*?
		# You only have to do it ONCE!
		if 'MGA Translation' in item['tags']:
			chp, vol = extractChapterVol(item['title'])
			# Also called "Martial God Asura"
			return buildReleaseMessage(item, 'Xiuluo Wushen', vol, chp)
		elif 'Xian Ni' in item['tags'] or 'Xian Ni Translation' in item['tags']:
			chp, vol = extractChapterVol(item['title'])
			return buildReleaseMessage(item, 'Xian Ni', vol, chp)
		elif 'JMG Translation' in item['tags']:  # Series was dropped, have lots of old releases
			chp, vol = extractChapterVol(item['title'])
			return buildReleaseMessage(item, 'Shaonian Yixian', vol, chp)
		return False

	####################################################################################################################################################
	# Gravity Translation
	####################################################################################################################################################
	def extractGravityTranslation(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'Zhan Long' in item['tags']:
			return buildReleaseMessage(item, 'Zhan Long', vol, chp)
		elif 'Battle Through the Heavens' in item['tags']:
			return buildReleaseMessage(item, 'Battle Through the Heavens', vol, chp)
		elif "Ascension of The Alchemist God" in item['title'] \
			or "TAG Chapter" in item['title']                  \
			or 'The Alchemist God: Chapter' in item['title']:
			return buildReleaseMessage(item, 'Ascension of the Alchemist God', vol, chp)
		elif 'Chaotic Sword God' in item['tags']:
			return buildReleaseMessage(item, 'Chaotic Sword God', vol, chp)

		return False

	####################################################################################################################################################
	# Pika Translations
	####################################################################################################################################################
	def extractPikaTranslations(self, item):
		chp, vol = extractChapterVol(item['title'])
		if 'Close Combat Mage' in item['tags']:
			return buildReleaseMessage(item, 'Close Combat Mage', vol, chp)

		return False

	####################################################################################################################################################
	# Blue Silver Translations
	####################################################################################################################################################
	def extractBlueSilverTranslations(self, item):

		if 'Douluo Dalu' in item['tags']:
			proc_str = "%s %s" % (item['tags'], item['title'])
			proc_str = proc_str.replace("'", " ")
			chp, vol = extractChapterVol(proc_str)

			with open("out.txt", "a") as fp:
				fp.write("'%s', '%s', '%s'\n" % (proc_str, chp, vol))
			print(item['title'], item['tags'], proc_str, chp, vol)
			if not (chp and vol):
				return False

			return buildReleaseMessage(item, 'Douluo Dalu', vol, chp)

		return False



	####################################################################################################################################################
	# Alyschu & Co
	####################################################################################################################################################
	def extractAlyschuCo(self, item):
		# Whyyyy would you do these bullshit preview things!
		if "PREVIEW" in item['title'] or "preview" in item['title']:
			return False
		chp, vol = extractChapterVol(item['title'])
		if 'Against the Gods' in item['tags'] or 'Ni Tian Xie Shen (Against the Gods)' in item['title']:
			return buildReleaseMessage(item, 'Against the Gods', vol, chp)
		elif 'The Simple Life of Killing Demons' in item['tags']:
			return buildReleaseMessage(item, 'The Simple Life of Killing Demons', vol, chp)
		elif 'Magic, Mechanics, Shuraba' in item['title']:
			return buildReleaseMessage(item, 'Magic, Mechanics, Shuraba', vol, chp)
		elif 'The Flower Offering' in item['tags']:
			return buildReleaseMessage(item, 'The Flower Offering', vol, chp)
		return False

	####################################################################################################################################################
	# Shin Translations
	####################################################################################################################################################
	def extractShinTranslations(self, item):
		chp, vol, frag = extractChapterVolFragment(item['title'])
		if 'THE NEW GATE' in item['tags'] and not 'Status Update' in item['tags']:
			if chp and vol and frag:
				return buildReleaseMessage(item, 'The New Gate', vol, chp, frag=frag)
		return False

	####################################################################################################################################################
	# Scrya Translations
	####################################################################################################################################################
	def extractScryaTranslations(self, item):
		chp, vol, frag = extractChapterVolFragment(item['title'])
		if "So What if It's an RPG World!?" in item['tags']:
			return buildReleaseMessage(item, "So What if It's an RPG World!?", vol, chp, frag=frag)

		return False

	####################################################################################################################################################
	# Japtem
	####################################################################################################################################################
	def extractJaptem(self, item):
		chp, vol, frag = extractChapterVolFragment(item['title'])
		if '[Chinese] Shadow Rogue' in item['tags']:
			return buildReleaseMessage(item, "Shadow Rogue", vol, chp, frag=frag)
		if '[Chinese] Unique Legend' in item['tags']:
			return buildReleaseMessage(item, "Unique Legend", vol, chp, frag=frag)
		if '[Japanese] Magi\'s Grandson' in item['tags']:
			return buildReleaseMessage(item, "Magi's Grandson", vol, chp, frag=frag)
		if '[Japanese / Hosted] Arifureta' in item['tags']:
			return buildReleaseMessage(item, "Arifureta", vol, chp, frag=frag)
		return False

	####################################################################################################################################################
	# Wuxiaworld
	####################################################################################################################################################


	def extractWuxiaworld(self, item):
		chp, vol, frag = extractChapterVolFragment(item['title'])

		if 'CD Chapter Release' in item['tags']:
			return buildReleaseMessage(item, "Coiling Dragon", vol, chp, frag=frag)
		if 'dragon king with seven stars' in item['tags'] or 'Dragon King with Seven Stars' in item['title']:
			return buildReleaseMessage(item, "Dragon King with Seven Stars", vol, chp, frag=frag)
		if 'ISSTH Chapter Release' in item['tags']:
			return buildReleaseMessage(item, "I Shall Seal the Heavens", vol, chp, frag=frag)
		if 'BTTH Chapter Release' in item['tags'] or 'BTTH Chapter' in item['title']:
			return buildReleaseMessage(item, "Battle Through the Heavens", vol, chp, frag=frag)
		if 'SL Chapter Release' in item['tags'] or 'SA Chapter Release' in item['tags']:
			return buildReleaseMessage(item, "Skyfire Avenue", vol, chp, frag=frag)
		if 'MGA Chapter Release' in item['tags']:
			return buildReleaseMessage(item, "Martial God Asura", vol, chp, frag=frag)
		if 'ATG Chapter Release' in item['tags']:
			return buildReleaseMessage(item, "Ni Tian Xie Shen", vol, chp, frag=frag)
		if 'ST Chapter Release' in item['tags']:
			return buildReleaseMessage(item, "Xingchenbian", vol, chp, frag=frag)

		return False


	####################################################################################################################################################
	# Ziru's Musings | Translations~
	####################################################################################################################################################
	def extractZiruTranslations(self, item):
		if 'Dragon Bloodline' in item['tags'] or 'Dragon’s Bloodline — Chapter ' in item['title']:
			chp, vol, frag = extractChapterVolFragment(item['title'])
			return buildReleaseMessage(item, 'Dragon Bloodline', vol, chp, frag=frag)

		# Wow, the tags must be hand typed. soooo many typos
		if 'Suterareta Yuusha no Eiyuutan' in item['tags'] or \
			'Suterareta Yuusha no Eyuutan' in item['tags'] or \
			'Suterurareta Yuusha no Eiyuutan' in item['tags']:

			extract = re.search(r'Suterareta Yuusha no Ei?yuutan \((\d+)\-(.+?)\)', item['title'])
			if extract:
				vol = int(extract.group(1))
				try:
					chp = int(extract.group(2))
					postfix = ''
				except ValueError:
					chp = None
					postfix = extract.group(2)
				return buildReleaseMessage(item, 'Suterareta Yuusha no Eiyuutan', vol, chp, postfix=postfix)
		return False


	####################################################################################################################################################
	# Void Translations
	####################################################################################################################################################
	def extractVoidTranslations(self, item):
		chp, vol, frag = extractChapterVolFragment(item['title'])
		match = re.search(r'^Xian Ni Chapter \d+ ?[\-–]? ?(.*)$', item['title'])
		if match:
			return buildReleaseMessage(item, 'Xian Ni', vol, chp, postfix=match.group(1))



		return False


	####################################################################################################################################################
	# Calico x Tabby
	####################################################################################################################################################
	def extractCalicoxTabby(self, item):
		chp, vol, frag = extractChapterVolFragment(item['title'])
		if 'Meow Meow Meow' in item['tags']:
			return buildReleaseMessage(item, 'Meow Meow Meow', vol, chp, frag=frag)

		return False


	####################################################################################################################################################
	# Skythewood translations
	####################################################################################################################################################


	def extractSkythewood(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'Altina the Sword Princess' in item['tags']:
			return buildReleaseMessage(item, 'Haken no Kouki Altina', vol, chp, frag=frag)
		if 'Overlord' in item['tags']:
			# Lots of idiot-checking here, because there are a
			# bunch of annoying edge-cases I want to work around.
			# This will PROBABLY BREAK IN THE FUTURE!
			if "Drama CD" in item['title']:
				return False
			if "Track" in item['title']:
				return False
			if not "Volume" in item['title']:
				return False

			return buildReleaseMessage(item, 'Overlord', vol, chp, frag=frag, postfix=postfix)
		if 'Gifting the wonderful world' in item['tags']:
			return buildReleaseMessage(item, 'Gifting the Wonderful World with Blessings!', vol, chp, frag=frag)
		if "Knight's & Magic" in item['tags']:
			return buildReleaseMessage(item, 'Knight\'s & Magic', vol, chp, frag=frag)

		return False

	####################################################################################################################################################
	# Lygar Translations
	####################################################################################################################################################
	def extractLygarTranslations(self, item):
		chp, vol, frag = extractChapterVolFragment(item['title'])

		if 'elf tensei' in item['tags'] and not 'news' in item['tags']:
			return buildReleaseMessage(item, 'Elf Tensei Kara no Cheat Kenkoku-ki', vol, chp, frag=frag)

		return False

	####################################################################################################################################################
	# That Guy Over There
	####################################################################################################################################################
	def extractThatGuyOverThere(self, item):
		chp, vol, frag = extractChapterVolFragment(item['title'])

		if 'wushenkongjian' in item['tags']:
			return buildReleaseMessage(item, 'Wu Shen Kong Jian', vol, chp, frag=frag)

		match = re.search(r'^Le Festin de Vampire – Chapter (\d+)\-(\d+)', item['title'])
		if match:
			chp  = match.group(1)
			frag = match.group(2)
			return buildReleaseMessage(item, 'Le Festin de Vampire', vol, chp, frag=frag)
		return False

	####################################################################################################################################################
	# Otterspace Translation
	####################################################################################################################################################
	def extractOtterspaceTranslation(self, item):
		chp, vol, frag = extractChapterVolFragment(item['title'])
		if 'Elqueeness’' in item['title']:
			return buildReleaseMessage(item, 'Spirit King Elqueeness', vol, chp, frag=frag)
		if '[Dark Mage]' in item['title']:
			return buildReleaseMessage(item, 'Dark Mage', vol, chp, frag=frag)

		return False

	####################################################################################################################################################
	# MadoSpicy TL
	####################################################################################################################################################
	def extractMadoSpicy(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'Kyuuketsu Hime' in item['title']:
			# Hardcode ALL THE THINGS
			postfix = ''
			if "interlude" in postfix.lower():
				postfix = "Interlude {num}".format(num=chp)
				chp = None
			if "prologue" in postfix.lower():
				postfix = "Prologue {num}".format(num=chp)
				chp = None
			return buildReleaseMessage(item, 'Kyuuketsu Hime wa Barairo no Yume o Miru', vol, chp, frag=frag, postfix=postfix)
		return False

	####################################################################################################################################################
	# Tripp Translations
	####################################################################################################################################################
	def extractTrippTl(self, item):
		chp, vol, frag = extractChapterVolFragment(item['title'])

		if 'Majin Tenseiki' in item['title']:
			return buildReleaseMessage(item, 'Majin Tenseiki', vol, chp, frag=frag)

		return False

	####################################################################################################################################################
	# DarkFish Translations
	####################################################################################################################################################
	def extractDarkFish(self, item):
		chp, vol, frag = extractChapterVolFragment(item['title'])
		if 'She Professed Herself The Pupil Of The Wise Man'.lower() in item['title'].lower():
			return buildReleaseMessage(item, 'Kenja no Deshi wo Nanoru Kenja', vol, chp, frag=frag)
		# if 'Majin Tenseiki' in item['title']:
		return False

	####################################################################################################################################################
	# Manga0205 Translations
	####################################################################################################################################################
	def extractManga0205Translations(self, item):
		chp, vol, frag = extractChapterVolFragment(item['title'])
		if 'Sendai Yuusha wa Inkyou Shitai'.lower() in item['title'].lower():
			postfix = ''
			if 'Side Story'.lower() in item['title'].lower():
				postfix = "Side Story {num}".format(num=chp)
				chp = None
			return buildReleaseMessage(item, 'Sendai Yuusha wa Inkyou Shitai', vol, chp, frag=frag, postfix=postfix)

		return False


	####################################################################################################################################################
	# extractAzureSky
	####################################################################################################################################################
	def extractAzureSky(self, item):
		chp, vol, frag = extractChapterVolFragment(item['title'])
		if 'Shinde Hajimaru'.lower() in item['title'].lower():
			postfix = ''
			if "prologue" in item['title'].lower():
				postfix = 'Prologue'
			return buildReleaseMessage(item, 'Shinde Hajimaru Isekai Tensei', vol, chp, frag=frag, postfix=postfix)
		return False

	####################################################################################################################################################
	# extractRaisingTheDead
	####################################################################################################################################################
	def extractRaisingTheDead(self, item):
		chp, vol, frag = extractChapterVolFragment(item['title'])


		if 'Isekai meikyuu de dorei harem wo' in item['tags'] \
			or 'Slave harem in the labyrinth of the other world' in item['tags']:
			return buildReleaseMessage(item, 'Isekai Meikyuu De Dorei Harem wo', vol, chp, frag=frag)

		if 'Shinka no Mi' in item['tags']:
			return buildReleaseMessage(item, 'Shinka no Mi', vol, chp, frag=frag)

		if 'Elf Tensei' in item['tags']:
			return buildReleaseMessage(item, 'Elf Tensei Kara no Cheat Kenkoku-ki', vol, chp, frag=frag)

		if 'Smartphone' in item['tags']:
			return buildReleaseMessage(item, 'Isekai wa Smartphone to Tomoni', vol, chp, frag=frag)

		if 'Tran Sexual Online' in item['tags']:
			return buildReleaseMessage(item, 'Tran Sexual Online', vol, chp, frag=frag)

		if 'Takami no Kago' in item['tags']:
			return buildReleaseMessage(item, 'Takami No Kago', vol, chp, frag=frag)

		return False


	####################################################################################################################################################
	# Tensai Translations
	####################################################################################################################################################
	def extractTensaiTranslations(self, item):
		chp, vol, frag = extractChapterVolFragment(item['title'])
		if 'Spirit Migration' in item['tags']:
			return buildReleaseMessage(item, 'Spirit Migration', vol, chp, frag=frag)

		if 'Tsuyokute New Saga' in item['tags']:
			return buildReleaseMessage(item, 'Tsuyokute New Saga', vol, chp, frag=frag)

		return False

	####################################################################################################################################################
	# Groups involved in KnW:
	# 	Blazing Translations
	# 	CapsUsingShift Tl
	# 	Insignia Pierce
	# 	Kiriko Translations
	# 	Konjiki no Wordmaster
	# 	Loliquent
	# 	Blazing Translations
	# 	Pummels Translations
	# 	XCrossJ
	# 	Probably another dozen randos per week.
	# Really. Fuck you people. Tag your shit, and start a group blog.
	####################################################################################################################################################
	def extractKnW(self, item):
		chp, vol, frag = extractChapterVolFragment(item['title'])

		tags = item['tags']
		title = item['title']
		src = item['srcname']

		postfix = ''
		ret = None

		if 'Character Analysis' in item['title']:
			return ret

		if ('Chapters' in tags and 'Konjiki no Wordmaster' in tags) \
			or 'Konjiki no Wordmaster Web Novel Chapters' in tags   \
			or 'Konjiki' in tags                                    \
			or (src == 'Loliquent' and 'Konjiki no Wordmaster' in title):
			postfix = title.split("–", 1)[-1].strip()
			ret = buildReleaseMessage(item, 'Konjiki no Wordmaster', vol, chp, frag=frag, postfix=postfix)

		elif 'Konjiki no Wordmaster Chapters' in tags                                        \
			or 'Konjiki no Moji Tsukai' in tags                                              \
			or (src == 'Kiriko Translations' and ('KnW' in tags or 'KnW Chapter' in title))  \
			or (src == 'CapsUsingShift Tl' and 'Konjiki no Wordmaster' in title)             \
			or (src == 'Pummels Translations' and 'Konjiki no Word Master Chapter' in title) \
			or (src == 'XCrossJ' and 'Konjiki no Moji Tsukai' in title)                      \
			or (src == 'Insignia Pierce' and 'Konjiki no Word Master Chapter' in title):
			postfix = title.split(":", 1)[-1].strip()
			ret = buildReleaseMessage(item, 'Konjiki no Wordmaster', vol, chp, frag=frag, postfix=postfix)
			# elif 'Konjiki no Moji Tsukai' in tags:

		else:
			pass

		# Only return a value if we've actually found a chapter/vol
		if ret and (ret['vol'] or ret['chp']):
			return ret

		return False


	####################################################################################################################################################
	# Thunder Translations:
	####################################################################################################################################################
	def extractThunder(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'Stellar Transformations' in item['tags'] and (vol or chp):
			return buildReleaseMessage(item, 'Stellar Transformations', vol, chp, frag=frag, postfix=postfix)
		return False


	####################################################################################################################################################
	# Kiri Leaves:
	####################################################################################################################################################
	def extractKiri(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'Tensei Oujo' in item['tags'] and (vol or chp):
			return buildReleaseMessage(item, 'Tensei Oujo wa Kyou mo Hata o Tatakioru', vol, chp, frag=frag, postfix=postfix)

		return False


	####################################################################################################################################################
	# 中翻英圖書館 Translations
	####################################################################################################################################################
	def extractTuShuGuan(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'He Jing Kunlun' in item['tags'] and (vol or chp or postfix):
			return buildReleaseMessage(item, 'The Crane Startles Kunlun', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# Lingson's Translations
	####################################################################################################################################################
	def extractLingson(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'The Legendary Thief' in item['tags'] and (vol or chp or postfix):
			return buildReleaseMessage(item, 'Virtual World - The Legendary Thief', vol, chp, frag=frag, postfix=postfix)

		return False


	####################################################################################################################################################
	# Sword And Game
	####################################################################################################################################################
	def extractSwordAndGame(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'The Rising of the Shield Hero' in item['tags'] and 'chapter' in item['tags']:
			return buildReleaseMessage(item, 'The Rise of the Shield Hero', vol, chp, frag=frag, postfix=postfix)
		if 'Ark' in item['tags'] and (vol or chp or postfix):
			return buildReleaseMessage(item, 'Ark', vol, chp, frag=frag, postfix=postfix)

		return False


	####################################################################################################################################################
	# Clicky Click Translation
	####################################################################################################################################################
	def extractClicky(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'Legendary Moonlight Sculptor' in item['tags'] and any(['Volume' in tag for tag in item['tags']]):
			return buildReleaseMessage(item, 'Legendary Moonlight Sculptor', vol, chp, frag=frag, postfix=postfix)

		return False


	####################################################################################################################################################
	# Defiring
	####################################################################################################################################################
	def extractDefiring(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'World teacher' in item['title']:
			return buildReleaseMessage(item, 'World teacher', vol, chp, frag=frag, postfix=postfix)
		if 'Shinka no Mi' in item['title']:
			return buildReleaseMessage(item, 'Shinka no Mi', vol, chp, frag=frag, postfix=postfix)

		return False


	####################################################################################################################################################
	# Fanatical Translations
	####################################################################################################################################################
	def extractFanatical(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'One Life One Incarnation Beautiful Bones' in item['tags']:
			return buildReleaseMessage(item, 'One Life, One Incarnation - Beautiful Bones', vol, chp, frag=frag, postfix=postfix)
		if 'Best to Have Met You' in item['tags']:
			return buildReleaseMessage(item, 'Zuimei Yujian Ni', vol, chp, frag=frag, postfix=postfix)
		if 'Blazing Sunlight' in item['tags']:
			return buildReleaseMessage(item, 'Blazing Sunlight', vol, chp, frag=frag, postfix=postfix)
		if 'Wipe Clean After Eating' in item['tags']:
			return buildReleaseMessage(item, 'Chigan Mojing', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# Giraffe Corps
	####################################################################################################################################################
	def extractGiraffe(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'Ti Shen' in item['tags']:
			return buildReleaseMessage(item, 'Tishen', vol, chp, frag=frag, postfix=postfix)
		if 'True Star' in item['tags']:
			return buildReleaseMessage(item, 'Juxing', vol, chp, frag=frag, postfix=postfix)
		if 'Gong Hua' in item['tags']:
			return buildReleaseMessage(item, 'Gong Hua', vol, chp, frag=frag, postfix=postfix)
		if 'Chen Yue Zhi Yao' in item['tags']:
			return buildReleaseMessage(item, 'Chen Yue Zhi Yao', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# guhehe.TRANSLATIONS
	####################################################################################################################################################
	def extractGuhehe(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'ShominSample' in item['tags']:
			return buildReleaseMessage(item, 'Ore ga Ojou-sama Gakkou ni "Shomin Sample" Toshite Rachirareta Ken', vol, chp, frag=frag, postfix=postfix)
		if 'OniAi' in item['tags']:
			return buildReleaseMessage(item, 'Onii-chan Dakedo Ai Sae Areba Kankeinai yo ne', vol, chp, frag=frag, postfix=postfix)
		if 'Haganai' in item['tags']:
			return buildReleaseMessage(item, 'Boku wa Tomodachi ga Sukunai', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# Hajiko translation
	####################################################################################################################################################
	def extractHajiko(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'Ryuugoroshi no Sugosuhibi' in item['title']:
			return buildReleaseMessage(item, 'Ryugoroshi no Sugosuhibi', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# Imoutolicious
	####################################################################################################################################################
	def extractImoutolicious(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'sekaimo' in item['tags']:
			return buildReleaseMessage(item, 'Sekai Ichi no Imouto-sama', vol, chp, frag=frag, postfix=postfix)
		if 'dawnbringer' in item['tags']:
			return buildReleaseMessage(item, 'Dawnbringer: The Story of the Machine God', vol, chp, frag=frag, postfix=postfix)
		if 'clotaku club' in item['tags']:
			return buildReleaseMessage(item, 'Sumdeokbu!', vol, chp, frag=frag, postfix=postfix)
		if 'four lovers' in item['tags']:
			return buildReleaseMessage(item, 'Shurabara!', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# Isekai Mahou Translations!
	####################################################################################################################################################
	def extractIsekaiMahou(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'Isekai Mahou Chapter' in item['title'] and 'Release' in item['title']:
			return buildReleaseMessage(item, 'Isekai Mahou wa Okureteru!', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# Kerambit's Incisions
	####################################################################################################################################################
	def extractKerambit(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Yobidasa' in item['tags'] and (vol or chp):
			if not postfix and ":" in item['title']:
				postfix = item['title'].split(":")[-1]

			return buildReleaseMessage(item, 'Yobidasareta Satsuriku-sha', vol, chp, frag=frag, postfix=postfix)
		return False


	####################################################################################################################################################
	# Mahoutsuki Translation
	####################################################################################################################################################
	def extractMahoutsuki(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		# Only ever worked on Le Festin de Vampire
		if 'Uncategorized' in item['tags'] and chp and ("Chapter" in item['title'] or "prologue" in item['title']):
			return buildReleaseMessage(item, 'Le Festin de Vampire', vol, chp, frag=frag, postfix=postfix)
		return False

	####################################################################################################################################################
	# Maou the Yuusha
	####################################################################################################################################################
	def extractMaouTheYuusha(self, item):
		# I basically implemented this almost exclusively to mess with
		# Vaan Cruze, since [s]he has been adding releases manually
		# up to this point.
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if ":" in item['title']:
			postfix = item['title'].split(":", 1)[-1]
		if 'Maou the Yuusha' in item['tags'] and 'chapter' in item['tags']:
			return buildReleaseMessage(item, 'Maou the Yuusha', vol, chp, frag=frag, postfix=postfix)
		return False

	####################################################################################################################################################
	# Nightbreeze Translations
	####################################################################################################################################################
	def extractNightbreeze(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		releases = [
				'Transcending The Nine Heavens',
				'Stellar Transformation',
				'Stellar Transformations',  # I think someone accidentally a typo
			]
		for release in releases:
			if release in item['tags']:
				return buildReleaseMessage(item, release, vol, chp, frag=frag, postfix=postfix)
		return False

	####################################################################################################################################################
	# Ohanashimi
	####################################################################################################################################################
	def extractOhanashimi(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if ":" in item['title']:
			postfix = item['title'].split(":", 1)[-1]
		if "Chapter" in item['title']:
			return buildReleaseMessage(item, 'The Rise of the Shield Hero', vol, chp, frag=frag, postfix=postfix)
		return False

	####################################################################################################################################################
	# Omega Harem Translations
	####################################################################################################################################################
	def extractOmegaHarem(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		title = item['title']
		if 'Destruction Flag Noble Girl Villainess' in title or 'Destruction Flag Otome' in title:
			return buildReleaseMessage(item, 'Destruction Flag Otome', vol, chp, frag=frag, postfix=postfix)
		elif 'Dragon Life' in title:
			return buildReleaseMessage(item, 'Dragon Life', vol, chp, frag=frag, postfix=postfix)
		elif 'World Teacher' in title:
			return buildReleaseMessage(item, 'World Teacher - Isekaishiki Kyouiku Agent', vol, chp, frag=frag, postfix=postfix)
		elif 'jashin sidestory' in title.lower() or 'Jashin Average Side Story' in title:
			return buildReleaseMessage(item, 'Evil God Average – Side Story', vol, chp, frag=frag, postfix=postfix)
		elif 'Heibon' in title:
			return buildReleaseMessage(item, 'E? Heibon Desu yo??', vol, chp, frag=frag, postfix=postfix)
		elif 'Villainess Brother Reincarnation' in title:
			return buildReleaseMessage(item, 'Villainess Brother Reincarnation', vol, chp, frag=frag, postfix=postfix)
		elif 'The Black Knight' in title:
			return buildReleaseMessage(item, 'The Black Knight Who Was Stronger than Even the Hero', vol, chp, frag=frag, postfix=postfix)
		elif 'GunOta' in item['tags'] and 're-Translations rehost' in item['tags']:
			item['srcname'] = "Re:Translations"
			return buildReleaseMessage(item, 'Gun-Ota ga Mahou Sekai ni Tensei Shitara, Gendai Heiki de Guntai Harem wo Tsukucchaimashita!?', vol, chp, frag=frag, postfix=postfix)
		return False


	####################################################################################################################################################
	# Gila Translation Monster
	####################################################################################################################################################
	def extractGilaTranslation(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'Dawn Traveler' in item['tags'] and 'Translation' in item['tags']:
			return buildReleaseMessage(item, 'Dawn Traveler', vol, chp, frag=frag, postfix=postfix)
		if 'Tensei Shitara Slime Datta Ken' in item['tags'] and 'Translation' in item['tags']:
			# This seems to have episodes, not chapters, which confuses the fragment extraction
			if not "chapter" in item['title'].lower() and chp:
				frag = None
			return buildReleaseMessage(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)
		return False

	####################################################################################################################################################
	# A Flappy Teddy Bird
	####################################################################################################################################################
	def extractAFlappyTeddyBird(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'The Black Knight who was stronger than even the Hero' in item['title']:
			return buildReleaseMessage(item, 'The Black Knight Who Was Stronger than Even the Hero', vol, chp, frag=frag, postfix=postfix)
		return False


	####################################################################################################################################################
	# putttytranslations
	####################################################################################################################################################
	def extractPuttty(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		# Whoooo, tag case typos!
		if any(['god of thunder' == val.lower() for val in item['tags']]) and (vol or chp):
			if ":" in item['title']:
				postfix = item['title'].split(":", 1)[-1]
			return buildReleaseMessage(item, 'God of Thunder', vol, chp, frag=frag, postfix=postfix)
		return False

	####################################################################################################################################################
	# Rising Dragons Translation
	####################################################################################################################################################
	def extractRisingDragons(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'God and Devil World' in item['tags'] and 'Release' in item['tags']:
			return buildReleaseMessage(item, 'Shenmo Xitong', vol, chp, frag=frag, postfix=postfix)
		return False


	####################################################################################################################################################
	# Sylver Translations
	####################################################################################################################################################
	def extractSylver(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if "Shura's Wrath" in item['tags']:
			if ":" in item['title']:
				postfix = item['title'].split(":", 1)[-1]
			return buildReleaseMessage(item, 'Shura’s Wrath', vol, chp, frag=frag, postfix=postfix)
		return False

	####################################################################################################################################################
	# Tomorolls
	####################################################################################################################################################
	def extractTomorolls(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'Cicada as Dragon' in item['tags']:
			return buildReleaseMessage(item, 'Cicada as Dragon', vol, chp, frag=frag, postfix=postfix)
		return False

	####################################################################################################################################################
	# Totokk\'s Translations
	####################################################################################################################################################
	def extractTotokk(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		# Lawl, title typo
		if '[SYWZ] Chapter' in item['title'] or '[SWYZ] Chapter' in item['title'] or 'Shen Yin Wang Zuo, Chapter' in item['title']:
			return buildReleaseMessage(item, 'Shen Yin Wang Zuo', vol, chp, frag=frag, postfix=postfix)
		return False

	####################################################################################################################################################
	# Translation Nations
	####################################################################################################################################################
	def extractTranslationNations(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'Stellar Transformation' in item['tags']:
			return buildReleaseMessage(item, 'Stellar Transformations', vol, chp, frag=frag, postfix=postfix)
		if 'The Legendary Thief' in item['tags']:
			return buildReleaseMessage(item, 'Virtual World - The Legendary Thief', vol, chp, frag=frag, postfix=postfix)
		if 'SwallowedStar' in item['tags']:
			return buildReleaseMessage(item, 'Swallowed Star', vol, chp, frag=frag, postfix=postfix)
		return False

	####################################################################################################################################################
	# Ln Addiction
	####################################################################################################################################################
	def extractLnAddiction(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if ('Hissou Dungeon Unei Houhou' in item['tags'] or 'Hisshou Dungeon Unei Houhou' in item['tags']) and (chp or frag):
			return buildReleaseMessage(item, 'Hisshou Dungeon Unei Houhou', vol, chp, frag=frag, postfix=postfix)
		return False

	####################################################################################################################################################
	# Binggo & Corp Translations
	####################################################################################################################################################
	def extractBinggoCorp(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'Jiang Ye' in item['title'] and "Chapter" in item['title']:
			return buildReleaseMessage(item, 'Jiang Ye', vol, chp, frag=frag, postfix=postfix)
		if 'Ze Tian Ji' in item['title'] and "Chapter" in item['title']:
			return buildReleaseMessage(item, 'Ze Tian Ji', vol, chp, frag=frag, postfix=postfix)
		return False

	####################################################################################################################################################
	# tony-yon-ka.blogspot.com (the blog title is stupidly long)
	####################################################################################################################################################
	def extractTonyYonKa(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'Manowa' in item['title'] and chp:
			return buildReleaseMessage(item, 'Manowa Mamono Taosu Nouryoku Ubau Watashi Tsuyokunaru', vol, chp, frag=frag, postfix=postfix)
		if 'Vampire Princess' in item['title'] and chp:
			return buildReleaseMessage(item, 'Kyuuketsu Hime wa Barairo no Yume o Miru', vol, chp, frag=frag, postfix=postfix)
		return False

	####################################################################################################################################################
	# Rebirth Online
	####################################################################################################################################################
	def extractRebirthOnline(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if "TDADP" in item['title'] or 'To deprive a deprived person episode'.lower() in item['title'].lower():
			return buildReleaseMessage(item, 'To Deprive a Deprived Person', vol, chp, frag=frag, postfix=postfix)
		if "Lazy Dragon".lower() in item['title'].lower() and chp:
			return buildReleaseMessage(item, 'Taidana Doragon wa Hatarakimono', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# Ark Machine Translations
	####################################################################################################################################################
	def extractArkMachineTranslations(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'ark volume' in item['title'].lower():
			return buildReleaseMessage(item, 'Ark', vol, chp, frag=frag, postfix=postfix)

		return False


	####################################################################################################################################################
	# Avert Translations
	####################################################################################################################################################
	def extractAvert(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if not (vol or chp or frag):
			return False
		if 'rokujouma' in item['title'].lower():
			return buildReleaseMessage(item, 'Rokujouma no Shinryakusha!', vol, chp, frag=frag, postfix=postfix)
		elif 'fuyo shoukan mahou' in item['title'].lower() \
			or 'fuyo shoukan mahou' in item['tags']        \
			or 'fuyou shoukan mahou' in item['title'].lower():
			return buildReleaseMessage(item, 'Boku wa Isekai de Fuyo Mahou to Shoukan Mahou wo Tenbin ni Kakeru', vol, chp, frag=frag, postfix=postfix)
		elif 'regarding reincarnated to slime chapter' in item['title'].lower() \
				or 'Tensei Shitara Slime Datta Ken' in item['tags']:
			return buildReleaseMessage(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# Binhjamin
	####################################################################################################################################################
	def extractBinhjamin(self, item):

		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if not (vol or chp or frag or postfix):
			return False

		if ("SRKJ" in item['title'] or 'SRKJ-Sayonara Ryuu' in item['tags']) and (chp or vol):
			return buildReleaseMessage(item, 'Sayonara Ryuusei Konnichiwa Jinsei', vol, chp, frag=frag, postfix=postfix)
		if "Unborn" in item['title']:
			return buildReleaseMessage(item, 'Unborn', vol, chp, frag=frag, postfix=postfix)
		if "Bu ni Mi" in item['title'] \
			or '100 Years Of Martial Arts' in item['title']:
			return buildReleaseMessage(item, '100 Years Of Martial Arts', vol, chp, frag=frag, postfix=postfix)
		return False



	####################################################################################################################################################
	# Burei Dan Works
	####################################################################################################################################################
	def extractBureiDan(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'Isekai Canceller' in item['tags'] and (chp or vol or frag or postfix):
			return buildReleaseMessage(item, 'Isekai Canceller', vol, chp, frag=frag, postfix=postfix)
		if 'Kenja ni Natta' in item['tags'] and (chp or vol or frag or postfix):
			return buildReleaseMessage(item, 'Kenja ni Natta', vol, chp, frag=frag, postfix=postfix)
		return False


	####################################################################################################################################################
	# Lazy NEET Translations
	####################################################################################################################################################
	def extractNEET(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'NEET dakedo Hello Work ni Ittara Isekai ni Tsuretekareta' in item['tags']:
			return buildReleaseMessage(item, 'NEET dakedo Hello Work ni Ittara Isekai ni Tsuretekareta', vol, chp, frag=frag, postfix=postfix)
		return False


	####################################################################################################################################################
	# Hokage Translations
	####################################################################################################################################################
	def extractHokageTrans(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if any(['Aim the Deepest Part of the Different World Labyrinth'.lower() in tag.lower() for tag in item['tags']]):
			if re.match(r"\d+\.", item['title']):
				postfix = item['title'].split(".", 1)[-1]
			return buildReleaseMessage(item, 'Aim the Deepest Part of the Different World Labyrinth', vol, chp, frag=frag, postfix=postfix)

		if any(['Divine Protection of Many Gods'.lower() in tag.lower() for tag in item['tags']+[item['title']]]):
			return buildReleaseMessage(item, 'Divine Protection of Many Gods', vol, chp, frag=frag, postfix=postfix)

		if any(['Because Janitor-san is Not a Hero'.lower() in tag.lower() for tag in item['tags']+[item['title']]]):
			return buildReleaseMessage(item, 'Because Janitor-san is Not a Hero', vol, chp, frag=frag, postfix=postfix)

		return False


	####################################################################################################################################################
	# Neo Translations
	####################################################################################################################################################
	def extractNeoTranslations(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'The Man Picked up by the Gods'.lower() in item['title'].lower() and (chp or vol):
			return buildReleaseMessage(item, 'The Man Picked up by the Gods', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# Ruze Translations
	####################################################################################################################################################
	def extractRuzeTranslations(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Guang Zhi Zi' in item['title'] and (chp or vol):
			return buildReleaseMessage(item, 'Guang Zhi Zi', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# Wuxia Translations
	####################################################################################################################################################
	def extractWuxiaTranslations(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		releases = [
			'A Martial Odyssey',
			'Law of the Devil',
			'Tensei Shitara Slime Datta Ken',
			'The Nine Cauldrons',
		]
		for name in releases:
			if name in item['title'] and (chp or vol):
				return buildReleaseMessage(item, name, vol, chp, frag=frag, postfix=postfix)
		return False


	####################################################################################################################################################
	# 1HP
	####################################################################################################################################################
	def extract1HP(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Route to almightyness from 1HP' in item['title'] and (chp or vol):
			return buildReleaseMessage(item, 'HP1 kara Hajimeru Isekai Musou', vol, chp, frag=frag, postfix=postfix)

		return False


	####################################################################################################################################################
	# Tsuigeki Translations
	####################################################################################################################################################
	def extractTsuigeki(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Seiju no Kuni no Kinju Tsukai' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Seiju no Kuni no Kinju Tsukai', vol, chp, frag=frag, postfix=postfix)

		return False



	####################################################################################################################################################
	# Eros Workshop
	####################################################################################################################################################
	def extractErosWorkshop(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Young God Divine Armaments' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Young God Divine Armaments', vol, chp, frag=frag, postfix=postfix)

		return False


	####################################################################################################################################################
	# Forgetful Dreamer
	####################################################################################################################################################
	def extractForgetfulDreamer(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'ヤンデレ系乙女ゲーの世界に転生してしまったようです' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'It seems like I got reincarnated into the world of a Yandere Otome game', vol, chp, frag=frag, postfix=postfix)

		return False


	####################################################################################################################################################
	# Fudge Translations
	####################################################################################################################################################
	def extractFudgeTranslations(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'SoE' in item['title'] and (chp or vol):
			return buildReleaseMessage(item, 'The Sword of Emperor', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# Henouji Translation
	####################################################################################################################################################
	def extractHenoujiTranslation(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Get Naked' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Kazuha Axeplant’s Third Adventure', vol, chp, frag=frag, postfix=postfix)

		if ('Tensai Slime' in item['tags'] or 'Tensei Slime' in item['tags']) and  (chp or vol):
			return buildReleaseMessage(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# Infinite Novel Translations
	####################################################################################################################################################
	def extractInfiniteNovelTranslations(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Yomigaeri no Maou' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Yomigaeri no Maou', vol, chp, frag=frag, postfix=postfix)
		if 'Kuro no Shoukan Samurai' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Kuro no Shoukan Samurai', vol, chp, frag=frag, postfix=postfix)
		if 'Nidoume no Jinsei wo Isekai de' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Nidoume no Jinsei wo Isekai de', vol, chp, frag=frag, postfix=postfix)
		if 'Hachi-nan' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Hachinan tte, Sore wa Nai Deshou!', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# Isekai Soul-Cyborg Translations
	####################################################################################################################################################
	def extractIsekaiTranslation(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Isekai Maou to Shoukan Shoujo Dorei Majutsu' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Isekai Maou to Shoukan Shoujo no Dorei Majutsu', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# Iterations within a Thought-Eclipse
	####################################################################################################################################################
	def extractIterations(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'SaeKano' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Saenai Heroine no Sodatekata', vol, chp, frag=frag, postfix=postfix)

		return False



	####################################################################################################################################################
	# Kaezar Translations
	####################################################################################################################################################
	def extractKaezar(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Mushoku Tensei' in item['tags'] and (chp or vol):
			if 'Redundancy Chapters' in item['tags']:
				return buildReleaseMessage(item, 'Mushoku Tensei Redundancy', vol, chp, frag=frag, postfix=postfix)
			else:
				return buildReleaseMessage(item, 'Mushoku Tensei', vol, chp, frag=frag, postfix=postfix)
		return False


	####################################################################################################################################################
	# Larvyde Translation
	####################################################################################################################################################
	def extractLarvyde(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Ore no Osananajimi wa Joshikousei de Yuusha' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Ore no Osananajimi wa Joshikousei de Yuusha', vol, chp, frag=frag, postfix=postfix)
		if 'Oukoku e Tsuzuku Michi' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Oukoku e Tsuzuku Michi', vol, chp, frag=frag, postfix=postfix)
		if 'Takarakuji de 40-oku Atattandakedo' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Takarakuji de 40 Oku Atattandakedo Isekai ni Ijuu Suru', vol, chp, frag=frag, postfix=postfix)

		return False



	####################################################################################################################################################
	# Unchained Translation
	####################################################################################################################################################
	def extractUnchainedTranslation(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'The Alchemist God' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Ascension of the Alchemist God', vol, chp, frag=frag, postfix=postfix)

		return False


	####################################################################################################################################################
	# World of Watermelons
	####################################################################################################################################################
	def extractWatermelons(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		matches = re.search(r'\bB(\d+)C(\d+)\b', item['title'])
		if 'The Desolate Era' in item['tags'] and matches:
			vol, chp = matches.groups()
			postfix = ""
			if "–" in item['title']:
				postfix = item['title'].split("–", 1)[-1]

			return buildReleaseMessage(item, 'Mang Huang Ji', vol, chp, frag=frag, postfix=postfix)

		return False


	####################################################################################################################################################
	# WCC Translation
	####################################################################################################################################################
	def extractWCCTranslation(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if "chapter" in item['title'].lower():
			if ":" in item['title']:
				postfix = item['title'].split(":", 1)[-1]
			return buildReleaseMessage(item, 'World Customize Creator', vol, chp, frag=frag, postfix=postfix)

		return False


	####################################################################################################################################################
	# Shikkaku Translations
	####################################################################################################################################################
	def extractShikkakuTranslations(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if "kuro no maou" in item['title'].lower():
			return buildReleaseMessage(item, 'Kuro no Maou', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# izra709 | B Group no Shounen Translations
	####################################################################################################################################################
	def extractIzra709(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'monohito chapter' in item['title'].lower():
			return buildReleaseMessage(item, 'Monogatari no Naka no Hito', vol, chp, frag=frag, postfix=postfix)
		if 'b group chapter' in item['title'].lower():
			return buildReleaseMessage(item, 'B Group no Shounen', vol, chp, frag=frag, postfix=postfix)

		return False


	####################################################################################################################################################
	# EnTruce Translations
	####################################################################################################################################################
	def extractEnTruceTranslations(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'kuro no maou' in item['title'].lower() and 'chapter' in item['title'].lower():
			return buildReleaseMessage(item, 'Kuro no Maou', vol, chp, frag=frag, postfix=postfix)

		return False



	####################################################################################################################################################
	# Rhinabolla
	####################################################################################################################################################
	def extractRhinabolla(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'Hachi-nan Chapter' in item['title'] and not 'draft' in item['title'].lower():
			return buildReleaseMessage(item, 'Hachinan tte, Sore wa nai Deshou!', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# Supreme Origin Translations
	####################################################################################################################################################
	def extractSotranslations(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if not (chp or vol):
			return False

		if 'hachi-nan chapter' in item['title'].lower() and not 'draft' in item['title'].lower():
			return buildReleaseMessage(item, 'Hachinan tte, Sore wa nai Deshou!', vol, chp, frag=frag, postfix=postfix)

		if 'the devil of an angel chapter' in item['title'].lower() and not 'draft' in item['title'].lower():
			return buildReleaseMessage(item, 'The Devil of an Angel Chapter', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# Turb0 Translation
	####################################################################################################################################################
	def extractTurb0(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'kumo desu ga, nani ka?' in item['title'].lower() \
			or 'kumo desu ka, nani ga?' in item['title'].lower():
			return buildReleaseMessage(item, 'Kumo Desu ga, Nani ka?', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# 'Translated by a Clown'
	####################################################################################################################################################
	def extractClownTrans(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Tensei Shitara Slime datta ken' in item['tags'] and chp:
			return buildReleaseMessage(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# 'Nohohon Translation'
	####################################################################################################################################################
	def extractNohohon(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Monster Musume Harem wo Tsukurou!' in item['tags']:
			return buildReleaseMessage(item, 'Monster Musume Harem o Tsukurou!', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# NEET Translations
	####################################################################################################################################################
	def extractNeetTranslations(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Marginal Operation' in item['tags']:
			return buildReleaseMessage(item, 'Marginal Operation', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# Kyakka
	####################################################################################################################################################
	def extractKyakka(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'preview' in item['title'].lower():
			return False

		if 'Yahari Ore no Seishun Love Come wa Machigatteiru' in item['tags']  \
			and 'Translation' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Yahari Ore no Seishun Rabukome wa Machigatte Iru.', vol, chp, frag=frag, postfix=postfix)


		if 'Yahari Ore no Seishun Love Come wa Machigatteiru' in item['tags'] and 'Light Novel' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Yahari Ore no Seishun Rabukome wa Machigatte Iru.', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# 'AsherahBlue's Notebook'
	####################################################################################################################################################
	def extractAsherahBlue(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Juvenile Medical God' in item['tags']:
			return buildReleaseMessage(item, 'Shaonian Yixian', vol, chp, frag=frag, postfix=postfix)

		return False



	####################################################################################################################################################
	# 'Alcsel Translations'
	####################################################################################################################################################
	def extractAlcsel(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'AR Chapter' in item['title']:
			return buildReleaseMessage(item, 'Assassin Reborn', vol, chp, frag=frag, postfix=postfix)

		return False


	####################################################################################################################################################
	# 'GuroTranslation'
	####################################################################################################################################################
	def extractGuroTranslation(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Tensei shitara slime datta ken' in item['tags']:
			return buildReleaseMessage(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)

		return False


	####################################################################################################################################################
	# 'Shiroyukineko Translations'
	####################################################################################################################################################
	def extractShiroyukineko(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if not (vol or chp):
			return False

		if 'DOP' in item['tags'] or 'Descent of the Phoenix: 13 Year Old Princess Consort' in item['tags']:
			return buildReleaseMessage(item, 'Descent of the Phoenix: 13 Year Old Princess Consort', vol, chp, frag=frag, postfix=postfix)
		if 'LLS' in item['tags'] or 'Long Live Summons!' in item['tags']:
			return buildReleaseMessage(item, 'Long Live Summons!', vol, chp, frag=frag, postfix=postfix)
		if 'VW:UUTS' in item['tags'] or 'Virtual World: Unparalled Under The Sky' in item['tags']:
			return buildReleaseMessage(item, 'Virtual World: Unparalleled under the Sky', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	# 'NoviceTranslator'
	####################################################################################################################################################
	def extractNoviceTranslator(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Martial God Space Chapter' in item['title'] or 'Martial God Space' in item['tags']:
			return buildReleaseMessage(item, 'Martial God Space', vol, chp, frag=frag, postfix=postfix)
		return False

	####################################################################################################################################################
	# MahouKoukoku
	####################################################################################################################################################
	def extractMahouKoukoku(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if 'Shiro no Koukoku Monogatari ' in item['title']:
			return buildReleaseMessage(item, 'Shiro no Koukoku Monogatari', vol, chp, frag=frag, postfix=postfix)
		return False

	####################################################################################################################################################
	# Ensj Translations
	####################################################################################################################################################
	def extractEnsjTranslations(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'King Shura' in item['tags']:
			return buildReleaseMessage(item, 'King Shura', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	#
	####################################################################################################################################################
	def extractStub(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		print(item['title'])
		print(item['tags'])
		print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

		return False


	####################################################################################################################################################
	# 'A0132'
	####################################################################################################################################################
	def extractA0132(self, item):
		agg_title = "{tags} {title}".format(tags=" ".join(item['tags']), title=item['title'])

		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(agg_title)

		# print(item['title'])
		# print(item['tags'])
		# print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

		return False


	####################################################################################################################################################
	# B
	####################################################################################################################################################
	def extractCeLn(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Seirei Gensouki' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Seirei Gensouki - Konna Sekai de Deaeta Kimi ni', vol, chp, frag=frag, postfix=postfix)

		if 'Mushi Uta' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Mushi-Uta', vol, chp, frag=frag, postfix=postfix)

		if 'Shinonome Yuuko series' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Shinonome Yuuko wa Tanpen Shousetsu o Aishite Iru', vol, chp, frag=frag, postfix=postfix)

		if 'Mismarca Koukoku Monogatari' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Mismarca Koukoku Monogatari', vol, chp, frag=frag, postfix=postfix)


		return False


	####################################################################################################################################################
	# 'yukkuri-literature-service'
	####################################################################################################################################################
	def extractYukkuri(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if '10 nen goshi no HikiNEET o Yamete Gaishutsushitara Jitaku goto Isekai ni Ten’ishiteta' in item['tags']:
			return buildReleaseMessage(item, '10 nen goshi no HikiNEET o Yamete Gaishutsushitara Jitaku goto Isekai ni Ten’ishiteta', vol, chp, frag=frag, postfix=postfix)
		elif 'Takarakuji de 40 Oku Atattanda kedo Isekai ni Ijuusuru' in item['tags']:
			return buildReleaseMessage(item, 'Takarakuji de 40 Oku Atattanda kedo Isekai ni Ijuusuru', vol, chp, frag=frag, postfix=postfix)
		elif 'Tenseisha wa Cheat o Nozomanai' in item['tags']:
			return buildReleaseMessage(item, 'Tenseisha wa Cheat o Nozomanai', vol, chp, frag=frag, postfix=postfix)
		elif 'Genjitsushugisha no Oukoku Kaizouki' in item['tags']:
			return buildReleaseMessage(item, 'Genjitsushugisha no Oukoku Kaizouki', vol, chp, frag=frag, postfix=postfix)


		return False


	####################################################################################################################################################
	# '桜翻訳! | Light novel translations'
	####################################################################################################################################################
	def extractSakurahonyaku(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'hyouketsu kyoukai no eden' in item['tags']:
			return buildReleaseMessage(item, 'Hyouketsu Kyoukai no Eden', vol, chp, frag=frag, postfix=postfix)

		return False



	####################################################################################################################################################
	# JawzTranslations
	####################################################################################################################################################
	def extractJawzTranslations(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Zectas' in item['tags'] and vol and chp:
			return buildReleaseMessage(item, 'Hyouketsu Kyoukai no Eden', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
		if 'LMS' in item['tags'] and vol and chp:
			return buildReleaseMessage(item, 'Legendary Moonlight Sculptor', vol, chp, frag=frag, postfix=postfix)

		return False


	####################################################################################################################################################
	#
	####################################################################################################################################################
	def extractDreadfulDecoding(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Gun Gale Online' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Sword Art Online Alternative - Gun Gale Online', vol, chp, frag=frag, postfix=postfix)

		return False



	####################################################################################################################################################
	#
	####################################################################################################################################################
	def extractBersekerTranslations(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Because the world has changed into a death game is funny' in item['tags'] and (chp or vol or "Prologue" in postfix):
			return buildReleaseMessage(item, 'Sekai ga death game ni natta no de tanoshii desu', vol, chp, frag=frag, postfix=postfix)

		return False

	####################################################################################################################################################
	#
	####################################################################################################################################################
	def extractLunate(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if "chapter" in item['title'].lower() and (vol or chp):
			return buildReleaseMessage(item, 'World Customize Creator', vol, chp, frag=frag, postfix=postfix)

		return False


	####################################################################################################################################################
	#
	####################################################################################################################################################
	def extractBakaDogeza(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if "chapter" in item['title'].lower() and (vol or chp):
			return buildReleaseMessage(item, 'Knights & Magic', vol, chp, frag=frag, postfix=postfix)

		return False


	####################################################################################################################################################
	#
	####################################################################################################################################################
	def extractCNovelProj(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Please Be More Serious' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Please Be More Serious', vol, chp, frag=frag, postfix=postfix)

		if 'Still Not Wanting to Forget' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Still Not Wanting to Forget', vol, chp, frag=frag, postfix=postfix)


		print(item['title'])
		print(item['tags'])
		print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

		return False

	####################################################################################################################################################
	#
	####################################################################################################################################################
	def extractLolercoaster(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'Seirei Gensouki' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Seirei Gensouki - Konna Sekai de Deaeta Kimi ni', vol, chp, frag=frag, postfix=postfix)


		print(item['title'])
		print(item['tags'])
		print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

		return False

	####################################################################################################################################################
	# General feedproxy stuff
	####################################################################################################################################################
	def extractFeedProxy(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if 'The Man Picked up by the Gods' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Kamitachi ni Hirowareta Otoko', vol, chp, frag=frag, postfix=postfix)

		return False




	####################################################################################################################################################
	# Untuned Translation Blog
	####################################################################################################################################################
	def extractUntunedTranslation(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		# if 'meg and seron' in item['tags'] and (chp or vol):
		# 	return buildReleaseMessage(item, 'Meg and Seron', vol, chp, frag=frag, postfix=postfix)

		# Ffffuuuuu now roman numerals!

		# print(item['title'])
		# print(item['tags'])
		# print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

		return False


	####################################################################################################################################################
	# 'CtrlAlcalá'
	####################################################################################################################################################
	def extractCtrlA(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])


		# Literal "three", "five" etc... for chapter numbering?
		# print(item['title'])
		# print(item['tags'])
		# print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

		return False


	####################################################################################################################################################
	####################################################################################################################################################
	##
	##  OEL Bits!
	##
	####################################################################################################################################################
	####################################################################################################################################################


	####################################################################################################################################################
	# DragomirCM
	####################################################################################################################################################
	def extractDragomirCM(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		if not postfix and ":" in item['title']:
			postfix = item['title'].split(":")[-1]
		if 'Magic Academy' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'I was reincarnated as a Magic Academy!', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
		if "100 Luck" in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, '100 Luck and the Dragon Tamer Skill!', vol, chp, frag=frag, postfix=postfix, tl_type='oel')


		return False
	####################################################################################################################################################
	# Mike777ac
	####################################################################################################################################################
	def extractMike777ac(self, item):
		vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

		if not postfix and ":" in item['title']:
			postfix = item['title'].split(":")[-1]

		# Christ, this guy doesn't seem to get how tags work:
		# - 'Action'
		# - 'Adventure'
		# - 'Comedy'
		# - 'Fantasy'
		# - 'Hardcore OP-ness'
		# - 'Hardcore OPness'
		# - 'Magic'
		# - 'Mature'
		# - 'HCOP'
		# - 'MC'
		# - 'Transportation'
		# - 'Dungeon'
		#
		# This shit isn't used for indexing or crap. Why do you have so many useless synonyms and tags that are literally
		# applied to EVERY item?

		if 'Hardcore OPness' in item['tags'] and (chp or vol):
			return buildReleaseMessage(item, 'Hardcore OP-ness', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

		print()
		print(item['title'])
		print(item['tags'])
		print(vol, chp, frag, postfix)

		return False



	####################################################################################################################################################
	####################################################################################################################################################
	##
	##  Dispatcher
	##
	####################################################################################################################################################
	####################################################################################################################################################


	def dispatchRelease(self, item, debug = False):

		ret = False

		if item['srcname'] == 'お兄ちゃん、やめてぇ！':  # I got utf-8 in my code-sauce, bizzickle
			ret = self.extractOniichanyamete(item)
		elif item['srcname'] == 'Sousetsuka':
			ret = self.extractSousetsuka(item)
		elif item['srcname'] == 'Natsu TL':
			ret = self.extractNatsuTl(item)
		elif item['srcname'] == 'TheLazy9':
			ret = self.extractTheLazy9(item)
		elif item['srcname'] == 'Yoraikun Translation':
			ret = self.extractYoraikun(item)
		elif item['srcname'] == 'Flower Bridge Too':
			ret = self.extractFlowerBridgeToo(item)
		elif item['srcname'] == 'Pika Translations':
			ret = self.extractPikaTranslations(item)
		elif item['srcname'] == 'Blue Silver Translations':
			ret = self.extractBlueSilverTranslations(item)
		elif item['srcname'] == 'Alyschu & Co':
			ret = self.extractAlyschuCo(item)
		elif item['srcname'] == 'Henouji Translation':
			ret = self.extractHenoujiTranslation(item)
		elif item['srcname'] == 'Shin Translations':
			ret = self.extractShinTranslations(item)
		elif item['srcname'] == 'LygarTranslations':
			ret = self.extractLygarTranslations(item)
		elif item['srcname'] == 'Scrya Translations':
			ret = self.extractScryaTranslations(item)
		elif item['srcname'] == 'Japtem':
			ret = self.extractJaptem(item)
		elif item['srcname'] == 'Wuxiaworld':
			ret = self.extractWuxiaworld(item)
		elif item['srcname'] == 'Ziru\'s Musings | Translations~':
			ret = self.extractZiruTranslations(item)
		elif item['srcname'] == 'Void Translations':
			ret = self.extractVoidTranslations(item)
		elif item['srcname'] == 'Calico x Tabby':
			ret = self.extractCalicoxTabby(item)
		elif item['srcname'] == 'Skythewood translations':
			ret = self.extractSkythewood(item)
		elif item['srcname'] == 'ThatGuyOverThere':
			ret = self.extractThatGuyOverThere(item)
		elif item['srcname'] == 'otterspacetranslation':
			ret = self.extractOtterspaceTranslation(item)
		elif item['srcname'] == 'MadoSpicy TL':
			ret = self.extractMadoSpicy(item)
		elif item['srcname'] == 'Tripp Translations':
			ret = self.extractTrippTl(item)
		elif item['srcname'] == 'A fish once said this to me':
			ret = self.extractDarkFish(item)
		elif item['srcname'] == 'Manga0205 Translations':
			ret = self.extractManga0205Translations(item)
		elif item['srcname'] == 'Azure Sky Translation':
			ret = self.extractAzureSky(item)
		elif item['srcname'] == 'Raising the Dead':
			ret = self.extractRaisingTheDead(item)
		elif item['srcname'] == 'Tensai Translations':
			ret = self.extractTensaiTranslations(item)
		# The number of people working on Konjiki no Wordmaster
		# is TOO FUCKING HIGH
		elif item['srcname'] == 'Blazing Translations' \
			or item['srcname'] == 'CapsUsingShift Tl' \
			or item['srcname'] == 'Insignia Pierce' \
			or item['srcname'] == 'Kiriko Translations' \
			or item['srcname'] == 'Konjiki no Wordmaster' \
			or item['srcname'] == 'Loliquent' \
			or item['srcname'] == 'Blazing Translations' \
			or item['srcname'] == 'Pummels Translations' \
			or item['srcname'] == 'XCrossJ':
			ret = self.extractKnW(item)
		elif item['srcname'] == 'Thunder Translation':
			ret = self.extractThunder(item)
		elif item['srcname'] == 'Kiri Leaves':
			ret = self.extractKiri(item)
		elif item['srcname'] == 'Gravity Translation' \
			or item['srcname'] == 'Gravity Tales':
			ret = self.extractGravityTranslation(item)
		elif item['srcname'] == '中翻英圖書館 Translations':
			ret = self.extractTuShuGuan(item)
		elif item['srcname'] == 'Lingson\'s Translations':
			ret = self.extractLingson(item)
		elif item['srcname'] == 'Sword and Game':
			ret = self.extractSwordAndGame(item)
		elif item['srcname'] == 'Clicky Click Translation':
			ret = self.extractClicky(item)
		elif item['srcname'] == 'Defiring':
			ret = self.extractDefiring(item)
		elif item['srcname'] == 'Fanatical':
			ret = self.extractFanatical(item)
		elif item['srcname'] == 'Giraffe Corps':
			ret = self.extractGiraffe(item)
		elif item['srcname'] == 'guhehe.TRANSLATIONS':
			ret = self.extractGuhehe(item)
		elif item['srcname'] == 'Hajiko translation':
			ret = self.extractHajiko(item)
		elif item['srcname'] == 'Imoutolicious Light Novel Translations':
			ret = self.extractImoutolicious(item)
		elif item['srcname'] == 'Isekai Mahou Translations!':
			ret = self.extractIsekaiMahou(item)
		elif item['srcname'] == 'izra709 | B Group no Shounen Translations':
			ret = self.extractIzra709(item)
		elif item['srcname'] == 'Kerambit\'s Incisions':
			ret = self.extractKerambit(item)
		elif item['srcname'] == 'Mahoutsuki Translation':
			ret = self.extractMahoutsuki(item)
		elif item['srcname'] == 'VaanCruze':
			ret = self.extractMaouTheYuusha(item)
		elif item['srcname'] == 'Nightbreeze Translations':
			ret = self.extractNightbreeze(item)
		elif item['srcname'] == 'Ohanashimi':
			ret = self.extractOhanashimi(item)
		elif item['srcname'] == 'Omega Harem':
			ret = self.extractOmegaHarem(item)
		elif item['srcname'] == 'pandafuqtranslations':
			ret = self.extractPandaFuq(item)
		elif item['srcname'] == 'Prince Revolution!':
			ret = self.extractPrinceRevolution(item)
		elif item['srcname'] == 'putttytranslations':
			ret = self.extractPuttty(item)
		elif item['srcname'] == 'Rising Dragons Translation':
			ret = self.extractRisingDragons(item)
		elif item['srcname'] == 'Sylver Translations':
			ret = self.extractSylver(item)
		elif item['srcname'] == 'Tomorolls':
			ret = self.extractTomorolls(item)
		elif item['srcname'] == 'Totokk\'s Translations':
			ret = self.extractTotokk(item)
		elif item['srcname'] == 'Translation Nations':
			ret = self.extractTranslationNations(item)
		elif item['srcname'] == 'Untuned Translation Blog':
			ret = self.extractUntunedTranslation(item)
		elif item['srcname'] == 'Gila Translation Monster':
			ret = self.extractGilaTranslation(item)
		elif item['srcname'] == 'AFlappyTeddyBird':
			ret = self.extractAFlappyTeddyBird(item)
		elif item['srcname'] == 'Binggo&Corp':
			ret = self.extractBinggoCorp(item)
		elif item['srcname'] == 'Tony Yon Ka':
			ret = self.extractTonyYonKa(item)

		elif item['srcname'] == 'Rebirth Online':
			ret = self.extractRebirthOnline(item)
		elif item['srcname'] == 'Ln Addiction':
			ret = self.extractLnAddiction(item)
		elif item['srcname'] == 'Ark Machine Translations':
			ret = self.extractArkMachineTranslations(item)
		elif item['srcname'] == 'Avert Translations':
			ret = self.extractAvert(item)

		elif item['srcname'] == 'Binhjamin':
			ret = self.extractBinhjamin(item)
		elif item['srcname'] == 'Burei Dan Works':
			ret = self.extractBureiDan(item)
		elif item['srcname'] == 'C.E. Light Novel Translations':
			ret = self.extractCeLn(item)
		elif item['srcname'] == "Lazy NEET Translations":
			ret = self.extractNEET(item)
		elif item['srcname'] == "Hokage Translations":
			ret = self.extractHokageTrans(item)
		elif item['srcname'] == 'Neo Translations':
			ret = self.extractNeoTranslations(item)
		elif item['srcname'] == "Ruze Translations":
			ret = self.extractRuzeTranslations(item)
		elif item['srcname'] == 'Wuxia Translations':
			ret = self.extractWuxiaTranslations(item)
		elif item['srcname'] == '1HP':
			ret = self.extract1HP(item)
		elif item['srcname'] == 'Tsuigeki Translations':
			ret = self.extractTsuigeki(item)

		elif item['srcname'] == "Eros Workshop":
			ret = self.extractErosWorkshop(item)
		elif item['srcname'] == "FeedProxy":
			ret = self.extractFeedProxy(item)
		elif item['srcname'] == "Forgetful Dreamer":
			ret = self.extractForgetfulDreamer(item)
		elif item['srcname'] == "Fudge Translations":
			ret = self.extractFudgeTranslations(item)
		elif item['srcname'] == "Infinite Novel Translations":
			ret = self.extractInfiniteNovelTranslations(item)
		elif item['srcname'] == "Isekai Soul-Cyborg Translations":
			ret = self.extractIsekaiTranslation(item)
		elif item['srcname'] == "Iterations within a Thought-Eclipse":
			ret = self.extractIterations(item)
		elif item['srcname'] == "Kaezar Translations":
			ret = self.extractKaezar(item)
		elif item['srcname'] == "Kyakka":
			ret = self.extractKyakka(item)
		elif item['srcname'] == "Larvyde":
			ret = self.extractLarvyde(item)
		elif item['srcname'] == "Shiroyukineko Translations":
			ret = self.extractShiroyukineko(item)
		elif item['srcname'] == "Unchained Translation":
			ret = self.extractUnchainedTranslation(item)
		elif item['srcname'] == 'World of Watermelons':
			ret = self.extractWatermelons(item)
		elif item['srcname'] == 'WCC Translation':
			ret = self.extractWCCTranslation(item)
		elif item['srcname'] == 'Shikkaku Translations':
			ret = self.extractShikkakuTranslations(item)
		elif item['srcname'] == 'EnTruce Translations':
			ret = self.extractEnTruceTranslations(item)
		elif item['srcname'] == 'Rhinabolla':
			ret = self.extractRhinabolla(item)
		elif item['srcname'] == 'Supreme Origin Translations':
			ret = self.extractSotranslations(item)
		elif item['srcname'] == 'Turb0 Translation':
			ret = self.extractTurb0(item)
		elif item['srcname'] == 'Translated by a Clown':
			ret = self.extractClownTrans(item)
		elif item['srcname'] == 'Nohohon Translation':
			ret = self.extractNohohon(item)
		elif item['srcname'] == 'NEET Translations':
			ret = self.extractNeetTranslations(item)
		elif item['srcname'] == 'CtrlAlcalá':
			ret = self.extractCtrlA(item)
		elif item['srcname'] == 'AsherahBlue\'s Notebook':
			ret = self.extractAsherahBlue(item)
		elif item['srcname'] == 'Alcsel Translations':
			ret = self.extractAlcsel(item)
		elif item['srcname'] == 'Guro Translation':
			ret = self.extractGuroTranslation(item)
		elif item['srcname'] == 'NoviceTranslator':
			ret = self.extractNoviceTranslator(item)
		elif item['srcname'] == 'Mahou Koukoku':
			ret = self.extractMahouKoukoku(item)
		elif item['srcname'] == 'Ensj Translations':
			ret = self.extractEnsjTranslations(item)

		elif item['srcname'] == 'Yukkuri Free Time Literature Service':
			ret = self.extractYukkuri(item)
		elif item['srcname'] == '桜翻訳! | Light novel translations':
			ret = self.extractSakurahonyaku(item)
		elif item['srcname'] == 'JawzTranslations':
			ret = self.extractJawzTranslations(item)
		elif item['srcname'] == 'Dreadful Decoding':
			ret = self.extractDreadfulDecoding(item)
		elif item['srcname'] == 'Berseker Translations':
			ret = self.extractBersekerTranslations(item)
		elif item['srcname'] == 'Lunate':
			ret = self.extractLunate(item)
		elif item['srcname'] == 'Baka Dogeza Translation':
			ret = self.extractBakaDogeza(item)
		elif item['srcname'] == 'The C-Novel Project':
			ret = self.extractCNovelProj(item)

		# To Add:

		elif item['srcname'] == 'A0132':
			ret = self.extractA0132(item)
		elif item['srcname'] == "Kami Translation":
			ret = self.extractWAT(item)
		elif item['srcname'] == "KobatoChanDaiSukiScan":
			ret = self.extractWAT(item)
		elif item['srcname'] == "Kyakka":
			ret = self.extractWAT(item)
		elif item['srcname'] == "Mahou Koukoku":
			ret = self.extractWAT(item)
		elif item['srcname'] == "Roasted Tea":
			ret = self.extractWAT(item)
		elif item['srcname'] == 'Undecent Translations':
			ret = self.extractWAT(item)
		elif item['srcname'] == 'Undecent Translations':
			ret = self.extractWAT(item)
		elif item['srcname'] == 'WCC Translation':
			ret = self.extractWAT(item)
		elif item['srcname'] == 'ℝeanとann@':
			ret = self.extractWAT(item)
		elif item['srcname'] == 'Bad Translation':
			ret = self.extractWAT(item)
		elif item['srcname'] == 'LordofScrubs':
			ret = self.extractWAT(item)
		elif item['srcname'] == 'Roxism HQ':
			ret = self.extractWAT(item)
		elif item['srcname'] == "HaruPARTY":
			ret = self.extractWAT(item)

		# 'Henouji Translation', 'Tensei Slime Chapter 6  Skill Learning (Last Part)', '['Light Novel', 'Tensei Slime']', 'None', '6.0', 'None', ''
		# 'izra709 | B Group no Shounen Translations', 'Chapter 2 – Her Situation', '['Uncategorized']', 'None', '2.0', 'None', ''
		# 'JawzTranslations', 'Legendary Moonlight Sculptor English Volume 22 Chapter 03', '['LMS']', '22.0', '3.0', 'None', ''
		# 'Light Novel translations', 'Surviving a Monster World chapter 1, Alpha', '['Uncategorized']', 'None', '1.0', 'None', ''
		# 'pandafuqtranslations', 'Chapter 4 (2)', '['Douluodalu 2 - The unrivaled Tang-Clan', 'Douluodalu 2', 'translation', 'wuxia']', 'None', '4.0', 'None', ''
		# 'TheLazy9', 'Astarte’s Knight – The 3rd Story: Pig and Moustache', '["Astarte's Knight"]', 'None', '3.0', 'None', ''
		# 'Translation Raven', 'Godly Hunter – Chapter 14 – I Got Tricked! – Intransient', '['Godly Hunter', 'Intransient', 'Translation']', 'None', '14.0', 'None', ''
		# 'Untuned Translation Blog', '5656! -Knights' Strange Night- Episode 3', '['5656', 'etsusa bridge', 'light novel', 'translation']', 'None', '3.0', 'None', ''

		# Boku wa Isekai de Fuyo Mahou to Shoukan Mahou wo Tenbin ni Kakeru (Novel)


		# Handle "three" rather then "3"?
		# 'CtrlAlcalá', 'Magical Tournament Volume Three Chapter Eight: Sieger (Winner) – It’s okay if they don’t catch you', '['Fiction']', 'None', 'None', 'None', ''
		# 'CtrlAlcalá', 'Magical Tournament Volume Three Chapter Five: Beziehung (Connection) – My strenght is not your strenght', '['Fiction']', 'None', 'None', 'None', ''
		# 'CtrlAlcalá', 'Magical Tournament Volume Three Chapter Nine: Glas (Glass) – Nothing is for certain', '['Fiction']', 'None', 'None', 'None', ''
		# 'CtrlAlcalá', 'Magical Tournament Volume Three Chapter Seven: Gëfuhle (Feelings) – The one who wouldn’t back down.', '['Fiction']', 'None', 'None', 'None', ''
		# 'CtrlAlcalá', 'Magical Tournament Volume Three Chapter Six: Entwicklung (Evolution) – Just one more step', '['Fiction']', 'None', 'None', 'None', ''
		# 'CtrlAlcalá', 'Magical Tournament Volume Three Fifth Intermission: Monde (World) – Boredom of the [Demon Empress].', '['Fiction']', 'None', 'None', 'None', 'Intermission: Monde (World) – Boredom of the [Demon Empress].'
		# 'CtrlAlcalá', 'Magical Tournament Volume Three Sixth Intermission: Ciel (Sky) – [Babel’s Ruin] Ascension.', '['Fiction']', 'None', 'None', 'None', 'Intermission: Ciel (Sky) – [Babel’s Ruin] Ascension.'
		# 'CtrlAlcalá', 'Magical Tournament Volume Three Special Transmission: Character Index [Cinco]', '['Fiction']', 'None', 'None', 'None', ''
		# 'CtrlAlcalá', 'Magical Tournament Volume Three Special Transmission: Character Index [Seis]', '['Fiction']', 'None', 'None', 'None', ''

		# Will be challenging, uses pages instead of chapters
		elif item['srcname'] == "Shin Sekai Yori – From the New World":
			ret = self.extractWAT(item)

		# More annoying crap. Volumes are in the tags, chapters are "chapter {chp}-{part}"
		elif item['srcname'] == "A0132":
			ret = self.extractWAT(item)



		elif item['srcname'] == 'DragomirCM':
			ret = self.extractDragomirCM(item)

		elif item['srcname'] == 'Mike777ac':
			ret = self.extractMike777ac(item)



		# if ret:
		# 	print(item['title'])
		# 	print(ret["vol"], ret["chp"])
		# 	print()



		# One of the series is being re-numbered
		# also, uses lots of sequences, e.g. 5-10, etc...

		# Dead?
		# elif item['srcname'] == "Hello Translations":
		# 	ret = self.extractWAT(item)
		# elif item['srcname'] == "itranslateln":
		# 	ret = self.extractITranslateln(item)
		#

		# OEL Junk
		# 'JawzTranslations'

		# no tags OR title information
		# 'Bad Translation'

		# No parseable content here
		# 'Krytyk\'s Translations'

		# Releases are shit, and it's largely unparseable anyways
		# 'ELYSION Translation'


		# ret = False

		if flags.RSS_DEBUG and not ret:
			vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
			if vol or chp or frag:
				with open('rss_filter_misses.txt', "a") as fp:
					# fp.write("\n==============================\n")

					write_items = [
						("SourceName: ", item['srcname']),
						("Title:      ", item['title']),
						("Vol:        ", vol),
						("Chp:        ", chp),
						("Frag:       ", frag),
						("Postfix:    ", postfix),
						("Feed URL:   ", item['linkUrl']),
						("Tags:       ", item['tags']),
						("GUID:       ", item['guid']),
					]

					for name, val in write_items:
						fp.write("%s '%s', " % (name, val))
					fp.write("\n")
					# fp.write("Feed URL: '%s', guid: '%s'" % (item['linkUrl'], item['guid']))
					# fp.write("'%s', '%s', '%s', '%s', '%s', '%s', '%s'\n" % (item['srcname'], item['title'], item['tags'], vol, chp, frag, postfix))

		if self.dbg_print or flags.RSS_DEBUG:
			vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
			if not ret:
				print("Missed: '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (item['srcname'], item['title'], item['tags'], vol, chp, frag, postfix))
			# else:
			# 	print("OK! '%s', V:'%s', C:'%s', '%s', '%s', '%s'" % (ret['srcname'], ret['vol'], ret['chp'], ret['postfix'], ret['series'], ret['itemurl']))
			ret = False

		# Only return a value if we've actually found a chapter/vol
		if ret and not (ret['vol'] or ret['chp'] or ret['postfix']):
			ret = False

		# Do not trigger if there is "preview" in the title.
		if 'preview' in item['title'].lower():
			ret = False
		if ret:
			assert 'tl_type' in ret


		# ret = False

		return ret

		# DELETE FROM releases WHERE series=2346;
		# DELETE FROM releaseschanges WHERE series=2346;
		# DELETE FROM alternatenames WHERE series=2346;
		# DELETE FROM alternatenameschanges WHERE series=2346;
		# DELETE FROM serieschanges WHERE id=2346;
		# DELETE FROM series WHERE id=2346;

		# DELETE FROM releases WHERE tlgroup=58;
		# DELETE FROM releaseschanges WHERE tlgroup=58;
		# DELETE FROM alternatetranslatornames WHERE "group"=58;
		# DELETE FROM alternatetranslatornameschanges WHERE "group"=58;
		# DELETE FROM translators WHERE id=58;
		# DELETE FROM translatorschanges WHERE id=58;


	def getProcessedReleaseInfo(self, feedDat, debug):

		if any([item in feedDat['linkUrl'] for item in skip_filter]):
			print("Skipping!")
			return


		release = self.dispatchRelease(feedDat, debug)
		if release:
			ret = {
				'type' : 'parsed-release',
				'data' : release
			}
			return json.dumps(ret)
		return False


	def getRawFeedMessage(self, feedDat):

		feedDat = feedDat.copy()

		# remove the contents item, since it can be
		# quite large, and is not used.
		feedDat.pop('contents')
		ret = {
			'type' : 'raw-feed',
			'data' : feedDat
		}
		return json.dumps(ret)

	def processFeedData(self, feedDat, tx_raw=True, tx_parse=True):


		if any([item in feedDat['linkUrl'] for item in skip_filter]):
			return

		nicename = feedNameLut.getNiceName(feedDat['linkUrl'])
		if not nicename:
			nicename = urllib.parse.urlparse(feedDat['linkUrl']).netloc


		# if not nicename in self.names:
		# 	self.names.add(nicename)
		# 	# print(nicename)

		feedDat['srcname'] = nicename


		raw = self.getRawFeedMessage(feedDat)
		if raw and tx_raw:
			self.amqp_put_item(raw)

		debug = False
		if not tx_parse:
			debug = True

		new = self.getProcessedReleaseInfo(feedDat, debug)
		if new and tx_parse:
			self.amqp_put_item(new)



	####################################################################################################################################################
	# Todo:
	####################################################################################################################################################

	def extractWAT(self, item):
		# print("'{}' '{}'".format(item['srcname'], item['title']))
		return False

	def extractAssholeTranslations(self, item):
		return False

	####################################################################################################################################################
	#
	#  ##     ## ##    ## ########     ###    ########   ######  ########    ###    ########  ##       ########
	#  ##     ## ###   ## ##     ##   ## ##   ##     ## ##    ## ##         ## ##   ##     ## ##       ##
	#  ##     ## ####  ## ##     ##  ##   ##  ##     ## ##       ##        ##   ##  ##     ## ##       ##
	#  ##     ## ## ## ## ########  ##     ## ########   ######  ######   ##     ## ########  ##       ######
	#  ##     ## ##  #### ##        ######### ##   ##         ## ##       ######### ##     ## ##       ##
	#  ##     ## ##   ### ##        ##     ## ##    ##  ##    ## ##       ##     ## ##     ## ##       ##
	#   #######  ##    ## ##        ##     ## ##     ##  ######  ######## ##     ## ########  ######## ########
	#
	####################################################################################################################################################



	####################################################################################################################################################
	# pandafuqtranslations
	####################################################################################################################################################
	def extractPandaFuq(self, item):
		# More "third part of translation" or "last part of chapter nnn" crap
		pass


	####################################################################################################################################################
	# Prince Revolution!
	####################################################################################################################################################
	def extractPrinceRevolution(self, item):
		# Has annoying volume format ("V8C5"), will have to revisit.
		# vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
		# print(item['title'])
		# print(item['tags'])
		# print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))
		return False
