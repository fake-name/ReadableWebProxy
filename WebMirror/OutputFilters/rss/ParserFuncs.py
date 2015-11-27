
from WebMirror.OutputFilters.util.MessageConstructors import buildReleaseMessage
from WebMirror.OutputFilters.util.TitleParsers import extractChapterVol
from WebMirror.OutputFilters.util.TitleParsers import extractChapterVolFragment
from WebMirror.OutputFilters.util.TitleParsers import extractVolChapterFragmentPostfix

import re


####################################################################################################################################################
# Sousetsuka
####################################################################################################################################################
def extractSousetsuka(item):
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
def extractOniichanyamete(item):
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
def extractNatsuTl(item):
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
def extractTheLazy9(item):
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
def extractYoraikun(item):
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
def extractFlowerBridgeToo(item):
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
def extractGravityTranslation(item):
	vol, chp, dummy_frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'Zhan Long' in item['tags']:
		return buildReleaseMessage(item, 'Zhan Long', vol, chp, postfix=postfix)
	elif 'Battle Through the Heavens' in item['tags']:
		return buildReleaseMessage(item, 'Battle Through the Heavens', vol, chp, postfix=postfix)
	elif "Ascension of The Alchemist God" in item['title'] \
		or "TAG Chapter" in item['title']                  \
		or 'The Alchemist God: Chapter' in item['title']:
		return buildReleaseMessage(item, 'Ascension of the Alchemist God', vol, chp, postfix=postfix)
	elif 'Chaotic Sword God' in item['tags']:
		return buildReleaseMessage(item, 'Chaotic Sword God', vol, chp, postfix=postfix)

	return False

####################################################################################################################################################
# Pika Translations
####################################################################################################################################################
def extractPikaTranslations(item):
	chp, vol = extractChapterVol(item['title'])
	if 'Close Combat Mage' in item['tags']:
		return buildReleaseMessage(item, 'Close Combat Mage', vol, chp)

	return False

####################################################################################################################################################
# Blue Silver Translations
####################################################################################################################################################
def extractBlueSilverTranslations(item):

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
def extractAlyschuCo(item):
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
def extractShinTranslations(item):
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if 'THE NEW GATE' in item['tags'] and not 'Status Update' in item['tags']:
		if chp and vol and frag:
			return buildReleaseMessage(item, 'The New Gate', vol, chp, frag=frag)
	return False

####################################################################################################################################################
# Scrya Translations
####################################################################################################################################################
def extractScryaTranslations(item):
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if "So What if It's an RPG World!?" in item['tags']:
		return buildReleaseMessage(item, "So What if It's an RPG World!?", vol, chp, frag=frag)

	return False

####################################################################################################################################################
# Japtem
####################################################################################################################################################
def extractJaptem(item):
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


def extractWuxiaworld(item):
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
def extractZiruTranslations(item):
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
def extractVoidTranslations(item):
	chp, vol, dummy_frag = extractChapterVolFragment(item['title'])
	match = re.search(r'^Xian Ni Chapter \d+ ?[\-–]? ?(.*)$', item['title'])
	if match:
		return buildReleaseMessage(item, 'Xian Ni', vol, chp, postfix=match.group(1))



	return False


####################################################################################################################################################
# Calico x Tabby
####################################################################################################################################################
def extractCalicoxTabby(item):
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if 'Meow Meow Meow' in item['tags']:
		return buildReleaseMessage(item, 'Meow Meow Meow', vol, chp, frag=frag)

	return False


####################################################################################################################################################
# Skythewood translations
####################################################################################################################################################


def extractSkythewood(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'Altina the Sword Princess' in item['tags']:
		return buildReleaseMessage(item, 'Haken no Kouki Altina', vol, chp, frag=frag)
	if 'Overlord' in item['tags']:
		# Lots of idiot-checking here, because there are a
		# bunch of annoying edge-cases I want to work around.
		# This will PROBABLY BREAK IN THE FUTURE!
		if "Drama CD" in item['title'] or \
			"Track" in item['title'] or   \
			not "Volume" in item['title']:
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
def extractLygarTranslations(item):
	chp, vol, frag = extractChapterVolFragment(item['title'])

	if 'elf tensei' in item['tags'] and not 'news' in item['tags']:
		return buildReleaseMessage(item, 'Elf Tensei Kara no Cheat Kenkoku-ki', vol, chp, frag=frag)

	return False

####################################################################################################################################################
# That Guy Over There
####################################################################################################################################################
def extractThatGuyOverThere(item):
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
def extractOtterspaceTranslation(item):
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if 'Elqueeness’' in item['title']:
		return buildReleaseMessage(item, 'Spirit King Elqueeness', vol, chp, frag=frag)
	if '[Dark Mage]' in item['title']:
		return buildReleaseMessage(item, 'Dark Mage', vol, chp, frag=frag)

	return False

####################################################################################################################################################
# MadoSpicy TL
####################################################################################################################################################
def extractMadoSpicy(item):
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
def extractTrippTl(item):
	chp, vol, frag = extractChapterVolFragment(item['title'])

	if 'Majin Tenseiki' in item['title']:
		return buildReleaseMessage(item, 'Majin Tenseiki', vol, chp, frag=frag)

	return False

####################################################################################################################################################
# DarkFish Translations
####################################################################################################################################################
def extractDarkFish(item):
	chp, vol, frag = extractChapterVolFragment(item['title'])

	if 'She Professed Herself The Pupil Of The Wise Man'.lower() in item['title'].lower() or 'She Professed Herself The Pupil Of The Wise Man' in item['tags']:
		return buildReleaseMessage(item, 'Kenja no Deshi wo Nanoru Kenja', vol, chp, frag=frag)
	# if 'Majin Tenseiki' in item['title']:
	return False

####################################################################################################################################################
# Manga0205 Translations
####################################################################################################################################################
def extractManga0205Translations(item):
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
def extractAzureSky(item):
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
def extractRaisingTheDead(item):
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
def extractTensaiTranslations(item):
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
def extractKnW(item):
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
def extractThunder(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'Stellar Transformations' in item['tags'] and (vol or chp):
		return buildReleaseMessage(item, 'Stellar Transformations', vol, chp, frag=frag, postfix=postfix)
	return False


####################################################################################################################################################
# Kiri Leaves:
####################################################################################################################################################
def extractKiri(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'Tensei Oujo' in item['tags'] and (vol or chp):
		return buildReleaseMessage(item, 'Tensei Oujo wa Kyou mo Hata o Tatakioru', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
# 中翻英圖書館 Translations
####################################################################################################################################################
def extractTuShuGuan(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'He Jing Kunlun' in item['tags'] and (vol or chp or postfix):
		return buildReleaseMessage(item, 'The Crane Startles Kunlun', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Lingson's Translations
####################################################################################################################################################
def extractLingson(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'The Legendary Thief' in item['tags'] and (vol or chp or postfix):
		return buildReleaseMessage(item, 'Virtual World - The Legendary Thief', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
# Sword And Game
####################################################################################################################################################
def extractSwordAndGame(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'The Rising of the Shield Hero' in item['tags'] and 'chapter' in item['tags']:
		return buildReleaseMessage(item, 'The Rise of the Shield Hero', vol, chp, frag=frag, postfix=postfix)
	if 'Ark' in item['tags'] and (vol or chp or postfix):
		return buildReleaseMessage(item, 'Ark', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
# Clicky Click Translation
####################################################################################################################################################
def extractClicky(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'Legendary Moonlight Sculptor' in item['tags'] and any(['Volume' in tag for tag in item['tags']]):
		return buildReleaseMessage(item, 'Legendary Moonlight Sculptor', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
# Defiring
####################################################################################################################################################
def extractDefiring(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'World teacher' in item['title']:
		return buildReleaseMessage(item, 'World teacher', vol, chp, frag=frag, postfix=postfix)
	if 'Shinka no Mi' in item['title']:
		return buildReleaseMessage(item, 'Shinka no Mi', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
# Fanatical Translations
####################################################################################################################################################
def extractFanatical(item):
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
def extractGiraffe(item):
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
def extractGuhehe(item):
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
def extractHajiko(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'Ryuugoroshi no Sugosuhibi' in item['title']:
		return buildReleaseMessage(item, 'Ryugoroshi no Sugosuhibi', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Imoutolicious
####################################################################################################################################################
def extractImoutolicious(item):
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
def extractIsekaiMahou(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'Isekai Mahou Chapter' in item['title'] and 'Release' in item['title']:
		return buildReleaseMessage(item, 'Isekai Mahou wa Okureteru!', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Kerambit's Incisions
####################################################################################################################################################
def extractKerambit(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Yobidasa' in item['tags'] and (vol or chp):
		if not postfix and ":" in item['title']:
			postfix = item['title'].split(":")[-1]

		return buildReleaseMessage(item, 'Yobidasareta Satsuriku-sha', vol, chp, frag=frag, postfix=postfix)
	return False


####################################################################################################################################################
# Mahoutsuki Translation
####################################################################################################################################################
def extractMahoutsuki(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	# Only ever worked on Le Festin de Vampire
	if 'Uncategorized' in item['tags'] and chp and ("Chapter" in item['title'] or "prologue" in item['title']):
		return buildReleaseMessage(item, 'Le Festin de Vampire', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# Maou the Yuusha
####################################################################################################################################################
def extractMaouTheYuusha(item):
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
def extractNightbreeze(item):
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
def extractOhanashimi(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if ":" in item['title']:
		postfix = item['title'].split(":", 1)[-1]
	if "Chapter" in item['title']:
		return buildReleaseMessage(item, 'The Rise of the Shield Hero', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# Omega Harem Translations
####################################################################################################################################################
def extractOmegaHarem(item):
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
def extractGilaTranslation(item):
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
def extractAFlappyTeddyBird(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'The Black Knight who was stronger than even the Hero' in item['title']:
		return buildReleaseMessage(item, 'The Black Knight Who Was Stronger than Even the Hero', vol, chp, frag=frag, postfix=postfix)
	return False


####################################################################################################################################################
# putttytranslations
####################################################################################################################################################
def extractPuttty(item):
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
def extractRisingDragons(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'God and Devil World' in item['tags'] and 'Release' in item['tags']:
		return buildReleaseMessage(item, 'Shenmo Xitong', vol, chp, frag=frag, postfix=postfix)
	return False


####################################################################################################################################################
# Sylver Translations
####################################################################################################################################################
def extractSylver(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if "Shura's Wrath" in item['tags']:
		if ":" in item['title']:
			postfix = item['title'].split(":", 1)[-1]
		return buildReleaseMessage(item, 'Shura’s Wrath', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# Tomorolls
####################################################################################################################################################
def extractTomorolls(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'Cicada as Dragon' in item['tags']:
		return buildReleaseMessage(item, 'Cicada as Dragon', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# Totokk\'s Translations
####################################################################################################################################################
def extractTotokk(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	# Lawl, title typo
	if '[SYWZ] Chapter' in item['title'] or '[SWYZ] Chapter' in item['title'] or 'Shen Yin Wang Zuo, Chapter' in item['title']:
		return buildReleaseMessage(item, 'Shen Yin Wang Zuo', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# Translation Nations
####################################################################################################################################################
def extractTranslationNations(item):
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
def extractLnAddiction(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if ('Hissou Dungeon Unei Houhou' in item['tags'] or 'Hisshou Dungeon Unei Houhou' in item['tags']) and (chp or frag):
		return buildReleaseMessage(item, 'Hisshou Dungeon Unei Houhou', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# Binggo & Corp Translations
####################################################################################################################################################
def extractBinggoCorp(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'Jiang Ye' in item['title'] and "Chapter" in item['title']:
		return buildReleaseMessage(item, 'Jiang Ye', vol, chp, frag=frag, postfix=postfix)
	if 'Ze Tian Ji' in item['title'] and "Chapter" in item['title']:
		return buildReleaseMessage(item, 'Ze Tian Ji', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# tony-yon-ka.blogspot.com (the blog title is stupidly long)
####################################################################################################################################################
def extractTonyYonKa(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'Manowa' in item['title'] and chp:
		return buildReleaseMessage(item, 'Manowa Mamono Taosu Nouryoku Ubau Watashi Tsuyokunaru', vol, chp, frag=frag, postfix=postfix)
	if 'Vampire Princess' in item['title'] and chp:
		return buildReleaseMessage(item, 'Kyuuketsu Hime wa Barairo no Yume o Miru', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# Rebirth Online
####################################################################################################################################################
def extractRebirthOnline(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if "TDADP" in item['title'] or 'To deprive a deprived person episode'.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'To Deprive a Deprived Person', vol, chp, frag=frag, postfix=postfix)
	if "Lazy Dragon".lower() in item['title'].lower() and chp:
		return buildReleaseMessage(item, 'Taidana Doragon wa Hatarakimono', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Ark Machine Translations
####################################################################################################################################################
def extractArkMachineTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'ark volume' in item['title'].lower():
		return buildReleaseMessage(item, 'Ark', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
# Avert Translations
####################################################################################################################################################
def extractAvert(item):
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
def extractBinhjamin(item):

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
def extractBureiDan(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'Isekai Canceller' in item['tags'] and (chp or vol or frag or postfix):
		return buildReleaseMessage(item, 'Isekai Canceller', vol, chp, frag=frag, postfix=postfix)
	if 'Kenja ni Natta' in item['tags'] and (chp or vol or frag or postfix):
		return buildReleaseMessage(item, 'Kenja ni Natta', vol, chp, frag=frag, postfix=postfix)
	return False


####################################################################################################################################################
# Lazy NEET Translations
####################################################################################################################################################
def extractNEET(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'NEET dakedo Hello Work ni Ittara Isekai ni Tsuretekareta' in item['tags']:
		return buildReleaseMessage(item, 'NEET dakedo Hello Work ni Ittara Isekai ni Tsuretekareta', vol, chp, frag=frag, postfix=postfix)
	return False


####################################################################################################################################################
# Hokage Translations
####################################################################################################################################################
def extractHokageTrans(item):
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
def extractNeoTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'The Man Picked up by the Gods'.lower() in item['title'].lower() and (chp or vol):
		return buildReleaseMessage(item, 'The Man Picked up by the Gods', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Ruze Translations
####################################################################################################################################################
def extractRuzeTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Guang Zhi Zi' in item['title'] and (chp or vol):
		return buildReleaseMessage(item, 'Guang Zhi Zi', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Wuxia Translations
####################################################################################################################################################
def extractWuxiaTranslations(item):
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
def extract1HP(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Route to almightyness from 1HP' in item['title'] and (chp or vol):
		return buildReleaseMessage(item, 'HP1 kara Hajimeru Isekai Musou', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
# Tsuigeki Translations
####################################################################################################################################################
def extractTsuigeki(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Seiju no Kuni no Kinju Tsukai' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Seiju no Kuni no Kinju Tsukai', vol, chp, frag=frag, postfix=postfix)

	return False



####################################################################################################################################################
# Eros Workshop
####################################################################################################################################################
def extractErosWorkshop(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Young God Divine Armaments' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Young God Divine Armaments', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
# Forgetful Dreamer
####################################################################################################################################################
def extractForgetfulDreamer(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'ヤンデレ系乙女ゲーの世界に転生してしまったようです' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'It seems like I got reincarnated into the world of a Yandere Otome game', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
# Fudge Translations
####################################################################################################################################################
def extractFudgeTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'SoE' in item['title'] and (chp or vol):
		return buildReleaseMessage(item, 'The Sword of Emperor', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Henouji Translation
####################################################################################################################################################
def extractHenoujiTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Get Naked' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Kazuha Axeplant’s Third Adventure', vol, chp, frag=frag, postfix=postfix)

	if ('Tensai Slime' in item['tags'] or 'Tensei Slime' in item['tags']) and  (chp or vol):
		return buildReleaseMessage(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Infinite Novel Translations
####################################################################################################################################################
def extractInfiniteNovelTranslations(item):
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
def extractIsekaiTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Isekai Maou to Shoukan Shoujo Dorei Majutsu' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Isekai Maou to Shoukan Shoujo no Dorei Majutsu', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Iterations within a Thought-Eclipse
####################################################################################################################################################
def extractIterations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'SaeKano' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Saenai Heroine no Sodatekata', vol, chp, frag=frag, postfix=postfix)

	return False



####################################################################################################################################################
# Kaezar Translations
####################################################################################################################################################
def extractKaezar(item):
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
def extractLarvyde(item):
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
def extractUnchainedTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'The Alchemist God' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Ascension of the Alchemist God', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
# World of Watermelons
####################################################################################################################################################
def extractWatermelons(item):
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
def extractWCCTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if "chapter" in item['title'].lower():
		if ":" in item['title']:
			postfix = item['title'].split(":", 1)[-1]
		return buildReleaseMessage(item, 'World Customize Creator', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
# Shikkaku Translations
####################################################################################################################################################
def extractShikkakuTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if "kuro no maou" in item['title'].lower():
		return buildReleaseMessage(item, 'Kuro no Maou', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# izra709 | B Group no Shounen Translations
####################################################################################################################################################
def extractIzra709(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'monohito chapter' in item['title'].lower():
		return buildReleaseMessage(item, 'Monogatari no Naka no Hito', vol, chp, frag=frag, postfix=postfix)
	if 'b group chapter' in item['title'].lower():
		return buildReleaseMessage(item, 'B Group no Shounen', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
# EnTruce Translations
####################################################################################################################################################
def extractEnTruceTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'kuro no maou' in item['title'].lower() and 'chapter' in item['title'].lower():
		return buildReleaseMessage(item, 'Kuro no Maou', vol, chp, frag=frag, postfix=postfix)

	return False



####################################################################################################################################################
# Rhinabolla
####################################################################################################################################################
def extractRhinabolla(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'Hachi-nan Chapter' in item['title'] and not 'draft' in item['title'].lower():
		return buildReleaseMessage(item, 'Hachinan tte, Sore wa nai Deshou!', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Supreme Origin Translations
####################################################################################################################################################
def extractSotranslations(item):
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
def extractTurb0(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'kumo desu ga, nani ka?' in item['title'].lower() \
		or 'kumo desu ka, nani ga?' in item['title'].lower():
		return buildReleaseMessage(item, 'Kumo Desu ga, Nani ka?', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# 'Translated by a Clown'
####################################################################################################################################################
def extractClownTrans(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Tensei Shitara Slime datta ken' in item['tags'] and chp:
		return buildReleaseMessage(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# 'Nohohon Translation'
####################################################################################################################################################
def extractNohohon(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Monster Musume Harem wo Tsukurou!' in item['tags']:
		return buildReleaseMessage(item, 'Monster Musume Harem o Tsukurou!', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# NEET Translations
####################################################################################################################################################
def extractNeetTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Marginal Operation' in item['tags']:
		return buildReleaseMessage(item, 'Marginal Operation', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Kyakka
####################################################################################################################################################
def extractKyakka(item):
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
def extractAsherahBlue(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Juvenile Medical God' in item['tags']:
		return buildReleaseMessage(item, 'Shaonian Yixian', vol, chp, frag=frag, postfix=postfix)

	return False



####################################################################################################################################################
# 'Alcsel Translations'
####################################################################################################################################################
def extractAlcsel(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'AR Chapter' in item['title']:
		return buildReleaseMessage(item, 'Assassin Reborn', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
# 'GuroTranslation'
####################################################################################################################################################
def extractGuroTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Tensei shitara slime datta ken' in item['tags']:
		return buildReleaseMessage(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
# 'Shiroyukineko Translations'
####################################################################################################################################################
def extractShiroyukineko(item):
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
def extractNoviceTranslator(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Martial God Space Chapter' in item['title'] or 'Martial God Space' in item['tags']:
		return buildReleaseMessage(item, 'Martial God Space', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# MahouKoukoku
####################################################################################################################################################
def extractMahouKoukoku(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'Shiro no Koukoku Monogatari ' in item['title']:
		return buildReleaseMessage(item, 'Shiro no Koukoku Monogatari', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# Ensj Translations
####################################################################################################################################################
def extractEnsjTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'King Shura' in item['tags']:
		return buildReleaseMessage(item, 'King Shura', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractStub(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	print(item['title'])
	print(item['tags'])
	print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

	return False


####################################################################################################################################################
# B
####################################################################################################################################################
def extractCeLn(item):
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
def extractYukkuri(item):
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
def extractSakurahonyaku(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'hyouketsu kyoukai no eden' in item['tags']:
		return buildReleaseMessage(item, 'Hyouketsu Kyoukai no Eden', vol, chp, frag=frag, postfix=postfix)

	return False



####################################################################################################################################################
# JawzTranslations
####################################################################################################################################################
def extractJawzTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Zectas' in item['tags'] and vol and chp:
		return buildReleaseMessage(item, 'Hyouketsu Kyoukai no Eden', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'LMS' in item['tags'] and vol and chp:
		return buildReleaseMessage(item, 'Legendary Moonlight Sculptor', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
#
####################################################################################################################################################
def extractDreadfulDecoding(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Gun Gale Online' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Sword Art Online Alternative - Gun Gale Online', vol, chp, frag=frag, postfix=postfix)

	return False



####################################################################################################################################################
#
####################################################################################################################################################
def extractBersekerTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Because the world has changed into a death game is funny' in item['tags'] and (chp or vol or "Prologue" in postfix):
		return buildReleaseMessage(item, 'Sekai ga death game ni natta no de tanoshii desu', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractLunate(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if "chapter" in item['title'].lower() and (vol or chp):
		return buildReleaseMessage(item, 'World Customize Creator', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
#
####################################################################################################################################################
def extractBakaDogeza(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if "chapter" in item['title'].lower() and (vol or chp):
		return buildReleaseMessage(item, 'Knights & Magic', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
#
####################################################################################################################################################
def extractCNovelProj(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Please Be More Serious' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Please Be More Serious', vol, chp, frag=frag, postfix=postfix)

	if 'Still Not Wanting to Forget' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Still Not Wanting to Forget', vol, chp, frag=frag, postfix=postfix)


	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractRancer(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'The Strongest Magical Beast' in item['tags'] and 'Chapter Release' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'The Strongest Magical Beast', vol, chp, frag=frag, postfix=postfix)

	if 'Apocalypse ЯR' in item['tags'] and 'Chapter Release' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Apocalypse ЯR', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
#
####################################################################################################################################################
def extract87Percent(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Return of the former hero' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Return of the Former Hero', vol, chp, frag=frag, postfix=postfix)

	if 'Summoning at random' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Summoning at Random', vol, chp, frag=frag, postfix=postfix)

	if 'Legend' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'レジェンド', vol, chp, frag=frag, postfix=postfix)

	if 'Death game' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'The world is fun as it has become a death game', vol, chp, frag=frag, postfix=postfix)


	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractBeehugger(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Battle Emperor' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Battle Emperor', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractBuBuJingXinTrans(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'bu bu jing xin' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Bu Bu Jing Xin', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractMoonBunnyCafe(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Monogatari no Naka no Hito' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Monogatari no Naka no Hito', vol, chp, frag=frag, postfix=postfix)
	if 'Against The Gods' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Against The Gods', vol, chp, frag=frag, postfix=postfix)
	if 'The Demonic King Chases His Wife: The Rebellious Good-for-nothing Miss' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'The Demonic King Chases His Wife: The Rebellious Good-for-nothing Miss', vol, chp, frag=frag, postfix=postfix)
	if 'The Saint’s Recovery Magic is a Degraded Version of Mine' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'The Saint’s Recovery Magic is a Degraded Version of Mine', vol, chp, frag=frag, postfix=postfix)
	if 'It seems like I got reincarnated into the world of a Yandere Otome game.' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'It seems like I got reincarnated into the world of a Yandere Otome game.', vol, chp, frag=frag, postfix=postfix)
	if 'Parallel World Pharmacy'.lower() in item['title'].lower() and (chp or vol):
		return buildReleaseMessage(item, 'Parallel World Pharmacy', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
#
####################################################################################################################################################
def extractEroLightNovelTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Adolescent Adam' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Shishunki na Adam', vol, chp, frag=frag, postfix=postfix)

	if 'Harem Castle' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Harem Castle', vol, chp, frag=frag, postfix=postfix)
	if 'Harem Pirates' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Harem Pirates', vol, chp, frag=frag, postfix=postfix)

	if "Student Council President's Secret Laid Bare" in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, "Student Council President's Secret Laid Bare", vol, chp, frag=frag, postfix=postfix)


	return False


####################################################################################################################################################
#
####################################################################################################################################################
def extractLolercoaster(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Seirei Gensouki' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Seirei Gensouki - Konna Sekai de Deaeta Kimi ni', vol, chp, frag=frag, postfix=postfix)


	print(item['title'])
	print(item['tags'])
	print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWIP(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	# if 'Seirei Gensouki' in item['tags'] and (chp or vol):
	# 	return buildReleaseMessage(item, 'Seirei Gensouki - Konna Sekai de Deaeta Kimi ni', vol, chp, frag=frag, postfix=postfix)


	print(item['title'])
	print(item['tags'])
	print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

	return False


####################################################################################################################################################
# General feedproxy stuff
####################################################################################################################################################
def extractFeedProxy(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'The Man Picked up by the Gods' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Kamitachi ni Hirowareta Otoko', vol, chp, frag=frag, postfix=postfix)

	return False




def extractBase(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	# if 'meg and seron' in item['tags'] and (chp or vol):
	# 	return buildReleaseMessage(item, 'Meg and Seron', vol, chp, frag=frag, postfix=postfix)

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
def extractDragomirCM(item):
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
def extractMike777ac(item):
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
