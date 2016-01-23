
from WebMirror.OutputFilters.util.MessageConstructors import buildReleaseMessage
from WebMirror.OutputFilters.util.TitleParsers import extractChapterVol
from WebMirror.OutputFilters.util.TitleParsers import extractChapterVolFragment
from WebMirror.OutputFilters.util.TitleParsers import extractVolChapterFragmentPostfix

import re

####################################################################################################################################################
# Sousetsuka
####################################################################################################################################################
def extractSousetsuka(item):

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Desumachi' in item['tags']:

		extract = re.search(r'Kyousoukyoku (\d+)\-(\d+)', item['title'])
		if extract and not vol:
			vol = int(extract.group(1))
			chp = int(extract.group(2))
			# print("'{}' '{}', '{}', '{}', '{}'".format(item['title'], vol, chp, frag, postfix))

		# print(item['tags'],)
		return buildReleaseMessage(item, "Death March kara Hajimaru Isekai Kyousoukyoku", vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# お兄ちゃん、やめてぇ！ / Onii-chan Yamete
####################################################################################################################################################
def extractOniichanyamete(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if       'Jashin Average'   in item['title'] \
			or 'Cthulhu Average'  in item['title'] \
			or 'Evil God Average' in item['tags']  \
			or 'jashin'           in item['tags']:

		if "Side Story" in item['title']:
			return False
		return buildReleaseMessage(item, 'Evil God Average', vol, chp, frag=frag)

	if 'Tilea’s Worries' in item['title']:
		return buildReleaseMessage(item, 'Tilea\'s Worries', vol, chp, postfix=postfix)

	if 'Kenkyo Kenjitu' in item['tags']:
		return buildReleaseMessage(item, 'Kenkyo Kenjitu', vol, chp, postfix=postfix)

	if 'The Bathroom Goddess' in item['tags']:
		return buildReleaseMessage(item, 'The Bathroom Goddess', vol, chp, postfix=postfix)
	if 'a wild boss appeared' in item['tags']:
		return buildReleaseMessage(item, 'A Wild Boss Appeared', vol, chp, postfix=postfix)

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
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Jikuu' in item['tags']:
		return buildReleaseMessage(item, "Jikuu Mahou de Isekai to Chikyuu wo ittarikitari", vol, chp, frag=frag, postfix=postfix)

	if 'Magi Craft Meister' in item['tags']:
		return buildReleaseMessage(item, 'Magi Craft Meister', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# TheLazy9
####################################################################################################################################################
def extractTheLazy9(item):

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'かんすとっぷ！(KANSUTOPPU)' in item['tags'] or "Kansutoppu!" in item['title']:
		return buildReleaseMessage(item, "Kansutoppu!", vol, chp, frag=frag, postfix=postfix)
	if 'Goblin Tenseiki ~erufu youjo ni kaku de maketeru yuusha na ore~' in item['tags']:
		return buildReleaseMessage(item, 'Goblin Tenseiki ~erufu youjo ni kaku de maketeru yuusha na ore~', vol, chp, frag=frag, postfix=postfix)

	if "Black Knight" in item['title']:
		return buildReleaseMessage(item, "The Black Knight Who Was Stronger than even the Hero", vol, chp, frag=frag, postfix=postfix)
	if "Astarte’s Knight" in item['title']:
		return buildReleaseMessage(item, "Astarte's Knight", vol, chp, frag=frag, postfix=postfix)
	if "HTG:" in item['title']:
		return buildReleaseMessage(item, "Tozoku shoujo ni tensei shita ore no shimei wa yuusha to maou ni iyagarasena no!", vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Yoraikun
####################################################################################################################################################
def extractYoraikun(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'The Rise of the Shield Hero' in item['tags']:
		return buildReleaseMessage(item, 'The Rise of the Shield Hero', vol, chp, frag=frag, postfix=postfix)
	elif 'Konjiki no Wordmaster' in item['tags']:
		return buildReleaseMessage(item, 'Konjiki no Wordmaster', vol, chp, frag=frag, postfix=postfix)
	elif 'IKCTAWBWTWH' in item['tags']:
		return buildReleaseMessage(item, 'I Kinda Came to Another World, But Where\'s the Way Home', vol, chp, frag=frag, postfix=postfix)
	elif 'Sevens' in item['tags']:
		return buildReleaseMessage(item, 'Sevens', vol, chp, frag=frag, postfix=postfix)
	elif 'The Lazy King' in item['tags']:
		return buildReleaseMessage(item, 'The Lazy King', vol, chp, frag=frag, postfix=postfix)

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
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	ltags = [tmp.lower() for tmp in item['tags']]

	if 'The King’s Avatar Chapter ' in item['title'] or \
		item['title'].startswith("The King’s Avatar (QZGS)"):
		return buildReleaseMessage(item, 'The King\'s Avatar', vol, chp, frag=frag, postfix=postfix)
	if 'Against Heaven :' in item['title']:
		return buildReleaseMessage(item, 'Against Heaven', vol, chp, frag=frag, postfix=postfix)
	if 'Great Demon King' in item['title']:
		return buildReleaseMessage(item, 'Great Demon King', vol, chp, frag=frag, postfix=postfix)
	if 'zhan long' in ltags or \
		item['title'].startswith("ZL "):
		return buildReleaseMessage(item, 'Zhan Long', vol, chp, frag=frag, postfix=postfix)
	if 'quan zhi gao shou' in ltags or \
		item['title'].startswith("QZGS "):
		return buildReleaseMessage(item, 'Quan Zhi Gao Shou', vol, chp, frag=frag, postfix=postfix)
	if 'battle through the heavens' in ltags or \
		item['title'].startswith("BTTH "):
		return buildReleaseMessage(item, 'Battle Through the Heavens', vol, chp, frag=frag, postfix=postfix)
	if "Ascension of The Alchemist God" in item['title'] \
		or "TAG Chapter" in item['title']                  \
		or 'The Alchemist God: Chapter' in item['title']:
		return buildReleaseMessage(item, 'Ascension of the Alchemist God', vol, chp, frag=frag, postfix=postfix)
	if 'chaotic sword god' in ltags:
		return buildReleaseMessage(item, 'Chaotic Sword God', vol, chp, frag=frag, postfix=postfix)
	if 'true martial world' in ltags:
		return buildReleaseMessage(item, 'True Martial World', vol, chp, frag=frag, postfix=postfix)
	if 'wu dong qian kun' in ltags:
		return buildReleaseMessage(item, 'Wu Dong Qian Kun', vol, chp, frag=frag, postfix=postfix)
	if "demon's diary" in ltags:
		return buildReleaseMessage(item, "Demon's Diary", vol, chp, frag=frag, postfix=postfix)
	if 'blue phoenix' in ltags or \
		item['title'].startswith("Blue Phoenix Chapter"):
		return buildReleaseMessage(item, 'Blue Phoenix', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if "the ancient's son" in ltags:
		return buildReleaseMessage(item, "The Ancient's Son", vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Might of the Stars' in item['title']:
		return buildReleaseMessage(item, 'Might of the Stars', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'mo tian ji' in ltags:
		return buildReleaseMessage(item, 'Mo Tian Ji', vol, chp, frag=frag, postfix=postfix)
	if 'great demon king' in ltags:
		return buildReleaseMessage(item, 'Great Demon King', vol, chp, frag=frag, postfix=postfix)
	if 'heavenly star' in ltags:
		return buildReleaseMessage(item, 'Heavenly Star', vol, chp, frag=frag, postfix=postfix)
	if 'conquest' in ltags:
		return buildReleaseMessage(item, 'Conquest', vol, chp, frag=frag, postfix=postfix)
	if 'shadow rogue' in ltags:
		return buildReleaseMessage(item, 'Shadow Rogue', vol, chp, frag=frag, postfix=postfix)
	if 'Blood Hourglass' in item['title']:
		return buildReleaseMessage(item, 'Blood Hourglass', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Pika Translations
####################################################################################################################################################
def extractPikaTranslations(item):
	chp, vol = extractChapterVol(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Close Combat Mage' in item['tags'] or \
		'CCM Chapter' in item['title'] or \
		'Close Combat Mage Chapter' in item['title']:
		return buildReleaseMessage(item, 'Close Combat Mage', vol, chp)
	if 'IoR Book' in item['title'] or \
		'IoR B' in item['title'] or \
		'Inch of Radiance Book' in item['title'] or \
		'Inch of Radiance Chapter' in item['title']:
		return buildReleaseMessage(item, 'Inch of Radiance', vol, chp)
	if 'World of Immortals Chapter' in item['title']:
		return buildReleaseMessage(item, 'World of Immortals', vol, chp)
	if 'Perfect World Chapter' in item['title'] or \
		'PW Chapter' in item['title']:
		return buildReleaseMessage(item, 'Perfect World', vol, chp)

	return False

####################################################################################################################################################
# Blue Silver Translations
####################################################################################################################################################
def extractBlueSilverTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Douluo Dalu' in item['tags']:
		proc_str = "%s %s" % (item['tags'], item['title'])
		proc_str = proc_str.replace("'", " ")
		chp, vol = extractChapterVol(proc_str)

		if not (chp and vol):
			return False
		return buildReleaseMessage(item, 'Douluo Dalu', vol, chp)

	if 'Immortal Executioner' in item['tags']:
		if not (chp or vol) or "preview" in item['title'].lower():
			return False
		return buildReleaseMessage(item, 'Immortal Executioner', vol, chp, frag=frag, postfix=postfix)

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

	if 'My Disciple Died Yet Again' in item['tags']:
		return buildReleaseMessage(item, 'My Disciple Died Yet Again', vol, chp, frag=frag)

	return False

####################################################################################################################################################
# Japtem
####################################################################################################################################################
def extractJaptem(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if '[Chinese] Shadow Rogue' in item['tags']:
		return buildReleaseMessage(item, "Shadow Rogue", vol, chp, frag=frag)
	if '[Chinese] Unique Legend' in item['tags']:
		return buildReleaseMessage(item, "Unique Legend", vol, chp, frag=frag)
	if '[Japanese] Magi\'s Grandson' in item['tags']:
		return buildReleaseMessage(item, "Magi's Grandson", vol, chp, frag=frag)
	if '[Japanese / Hosted] Arifureta' in item['tags']:
		return buildReleaseMessage(item, "Arifureta", vol, chp, frag=frag)
	if '[Korean] 21st Century Archmage' in item['tags']:
		return buildReleaseMessage(item, "21st Century Archmage", vol, chp, frag=frag)

	return False

####################################################################################################################################################
# Wuxiaworld
####################################################################################################################################################

def extractWuxiaworld(item):
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if not (chp or vol or frag):
		return False
	if 'Announcements' in item['tags']:
		return False

	if 'CD Chapter Release' in item['tags'] or 'Coiling Dragon' in item['tags']:
		return buildReleaseMessage(item, "Coiling Dragon", vol, chp, frag=frag)
	if 'dragon king with seven stars' in item['tags'] or 'Dragon King with Seven Stars' in item['title']:
		return buildReleaseMessage(item, "Dragon King with Seven Stars", vol, chp, frag=frag)
	if 'ISSTH Chapter Release' in item['tags'] or 'I Shall Seal the Heavens' in item['tags']:
		return buildReleaseMessage(item, "I Shall Seal the Heavens", vol, chp, frag=frag)
	if 'BTTH Chapter Release' in item['tags'] or 'BTTH Chapter' in item['title'] or 'Battle Through the Heavens' in item['tags']:
		return buildReleaseMessage(item, "Battle Through the Heavens", vol, chp, frag=frag)
	if 'SL Chapter Release' in item['tags'] or 'SA Chapter Release' in item['tags'] or 'Skyfire Avenue' in item['tags']:
		return buildReleaseMessage(item, "Skyfire Avenue", vol, chp, frag=frag)
	if 'MGA Chapter Release' in item['tags'] or 'Martial God Asura' in item['tags']:
		return buildReleaseMessage(item, "Martial God Asura", vol, chp, frag=frag)
	if 'ATG Chapter Release' in item['tags'] or 'Against the Gods' in item['tags']:
		return buildReleaseMessage(item, "Ni Tian Xie Shen", vol, chp, frag=frag)
	if 'ST Chapter Release' in item['tags']:
		return buildReleaseMessage(item, "Xingchenbian", vol, chp, frag=frag)
	if 'HJC Chapter Release' in item['tags'] or 'Heavenly Jewel Change' in item['tags']:
		return buildReleaseMessage(item, "Heavenly Jewel Change", vol, chp, frag=frag)
	if 'Child of Light' in item['tags'] or 'COL Chapter Release' in item['tags']:
		return buildReleaseMessage(item, 'Child of Light', vol, chp, frag=frag)
	if 'TDG Chapter Release' in item['tags'] or 'Tales of Demons & Gods' in item['tags']:
		return buildReleaseMessage(item, 'Tales of Demons & Gods', vol, chp, frag=frag)
	if 'TGR Chapter Release' in item['tags'] or 'The Great Ruler' in item['tags']:
		return buildReleaseMessage(item, 'The Great Ruler', vol, chp, frag=frag)
	if 'DE Chapter Release' in item['tags'] or 'Desolate Era' in item['tags']:
		return buildReleaseMessage(item, 'Desolate Era', vol, chp, frag=frag)
	if 'Wu Dong Qian Kun' in item['tags']:
		return buildReleaseMessage(item, 'Wu Dong Qian Kun', vol, chp, frag=frag)
	if 'Perfect World' in item['tags']:
		return buildReleaseMessage(item, 'Perfect World', vol, chp, frag=frag)

	return False

####################################################################################################################################################
# Ziru's Musings | Translations~
####################################################################################################################################################
def extractZiruTranslations(item):
	chp, vol, frag = extractChapterVolFragment(item['title'])

	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Dragon Bloodline' in item['tags'] or 'Dragon’s Bloodline — Chapter ' in item['title']:
		return buildReleaseMessage(item, 'Dragon Bloodline', vol, chp, frag=frag)
	if 'Lazy Dungeon Master' in item['tags'] or 'Lazy Dungeon Master ' in item['title']:
		return buildReleaseMessage(item, 'Lazy Dungeon Master', vol, chp, frag=frag)
	if 'Happy Peach' in item['tags'] or 'Happy Peach ' in item['title']:
		return buildReleaseMessage(item, 'Happy Peach', vol, chp, frag=frag)
	if "The Guild's Cheat Receptionist" in item['tags']:
		return buildReleaseMessage(item, "The Guild's Cheat Receptionist", vol, chp, frag=frag)
	if 'Suterareta Yuusha no Eiyuutan' in item['tags']:
		return buildReleaseMessage(item, 'Suterareta Yuusha no Eiyuutan', vol, chp, frag=frag)
	if 'The Restart' in item['tags']:
		return buildReleaseMessage(item, 'The Restart', vol, chp, frag=frag, tl_type='oel')

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Altina the Sword Princess' in item['tags']:
		return buildReleaseMessage(item, 'Haken no Kouki Altina', vol, chp, frag=frag)
	if 'Overlord' in item['tags']:
		# Lots of idiot-checking here, because there are a
		# bunch of annoying edge-cases I want to work around.
		# This will PROBABLY BREAK IN THE FUTURE!
		if "Drama CD" in item['title'] or \
			"Track" in item['title'] or   \
			not "Volume" in item['title']:
			return None

		return buildReleaseMessage(item, 'Overlord', vol, chp, frag=frag, postfix=postfix)
	if 'Gifting the wonderful world' in item['tags']:
		return buildReleaseMessage(item, 'Gifting the Wonderful World with Blessings!', vol, chp, frag=frag)
	if "Knight's & Magic" in item['tags']:
		return buildReleaseMessage(item, 'Knight\'s & Magic', vol, chp, frag=frag)
	if "Gate" in item['tags']:
		return buildReleaseMessage(item, 'Gate - Thus the JSDF Fought There!', vol, chp, frag=frag)
	if 'Genocide Reality' in item['tags']:
		return buildReleaseMessage(item, 'Genocide Reality', vol, chp, frag=frag)
	if 'Youjo Senki' in item['tags']:
		return buildReleaseMessage(item, 'Youjo Senki', vol, chp, frag=frag)

	return False

####################################################################################################################################################
# Lygar Translations
####################################################################################################################################################
def extractLygarTranslations(item):

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if ('elf tensei' in item['tags'] or 'elf tensei' in item['title'].lower()) and not 'news' in item['tags']:
		return buildReleaseMessage(item, 'Elf Tensei Kara no Cheat Kenkoku-ki', vol, chp, frag=frag, postfix=postfix)
	if 'Himekishi ga Classmate' in item['tags'] and not 'poll' in item['tags']:
		return buildReleaseMessage(item, 'Himekishi ga Classmate! ~ Isekai Cheat de Dorei ka Harem~', vol, chp, frag=frag, postfix=postfix)

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Elqueeness’' in item['title']:
		return buildReleaseMessage(item, 'Spirit King Elqueeness', vol, chp, frag=frag)
	if '[Dark Mage]' in item['title']:
		return buildReleaseMessage(item, 'Dark Mage', vol, chp, frag=frag)
	if 'Dragon Maken War' in item['title']:
		return buildReleaseMessage(item, 'Dragon Maken War', vol, chp, frag=frag)

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

	if 'She Professed Herself The Pupil Of The Wise Man'.lower() in item['title'].lower() or \
		'She Professed Herself The Pupil Of The Wise Man'.lower() in [tmp.lower() for tmp in item['tags']]:
		return buildReleaseMessage(item, 'Kenja no Deshi wo Nanoru Kenja', vol, chp, frag=frag)
	# if 'Majin Tenseiki' in item['title']:
	return False
####################################################################################################################################################
# Hot Cocoa Translations
####################################################################################################################################################
def extractHotCocoa(item):
	chp, vol, frag = extractChapterVolFragment(item['title'])

	if 'She Professed Herself The Pupil Of The Wise Man'.lower() in item['title'].lower() or \
		'She Professed Herself The Pupil Of The Wise Man'.lower() in [tmp.lower() for tmp in item['tags']]:
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
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Isekai meikyuu de dorei harem wo' in item['tags'] \
		or 'Slave harem in the labyrinth of the other world' in item['tags']:
		return buildReleaseMessage(item, 'Isekai Meikyuu De Dorei Harem wo', vol, chp, frag=frag)

	if 'Shinka no Mi' in item['tags'] or 'Shinka' in item['title']:
		return buildReleaseMessage(item, 'Shinka no Mi', vol, chp, frag=frag)

	if 'Kumo desu ga' in item['tags']:
		return buildReleaseMessage(item, 'Kumo Desu Ga, Nani Ka?', vol, chp, frag=frag)

	if 'Din No Monshou' in item['tags']:
		return buildReleaseMessage(item, 'Din No Monshou', vol, chp, frag=frag)

	if 'Elf Tensei' in item['tags']:
		return buildReleaseMessage(item, 'Elf Tensei Kara no Cheat Kenkoku-ki', vol, chp, frag=frag)

	if 'Smartphone' in item['tags'] or 'Smartphone Chapter' in item['title']:
		return buildReleaseMessage(item, 'Isekai wa Smartphone to Tomoni', vol, chp, frag=frag)

	if 'Tran Sexual Online' in item['tags'] or \
		'Tran Sexual Online' in item['title'] or \
		'Trans Sexual Online' in item['title']:
		return buildReleaseMessage(item, 'Tran Sexual Online', vol, chp, frag=frag)

	if 'Master Of Monsters' in item['title'] or 'Master of Monsters' in item['tags']:
		return buildReleaseMessage(item, 'Master Of Monsters', vol, chp, frag=frag)

	if 'Takami no Kago' in item['tags'] or 'Takami no Kago' in item['title']:
		return buildReleaseMessage(item, 'Takami No Kago', vol, chp, frag=frag)

	if 'Alice Tales' in item['tags']:
		return buildReleaseMessage(item, 'Alice Tale in Phantasmagoria', vol, chp, frag=frag)

	if 'E? Heibon Desu Yo??' in item['tags']:
		return buildReleaseMessage(item, 'E? Heibon Desu Yo??', vol, chp, frag=frag)

	if 'Right Grasper' in item['tags']:
		return buildReleaseMessage(item, 'Right Grasper ~Stealing Skills in the Other World~', vol, chp, frag=frag)

	if 'Is Heaven Supposed To Be Like This?!' in item['tags']:
		return buildReleaseMessage(item, "Is Heaven Supposed to Be Like This?!", vol, chp, frag=frag, tl_type='oel')

	if 'KmF?!' in item['tags']:
		matches = re.search(r'When I returned home, what I found was fantasy!\? (\d+)\-(\d+)', item['title'], flags=re.IGNORECASE)
		if matches:
			vol = float(matches.group(1))
			chp = float(matches.group(2))
			return buildReleaseMessage(item, 'Kaettekite mo Fantasy!?', vol, chp, frag=frag, postfix=postfix)

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	tags = item['tags']
	title = item['title']
	src = item['srcname']

	postfix = ''

	if src == 'XCrossJ' and 'Cross Gun' in item['tags']:
		return buildReleaseMessage(item, 'Cross Gun', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	if 'Character Analysis' in item['title']:
		return False

	if "Chapter" in title and src == 'Blazing Translations':
		if "By:" in title:
			return False
		if "Comment" in title:
			return False

		if ":" in title:
			postfix = title.split(":", 1)[-1].strip()
		elif "-" in title:
			postfix = title.split("–", 1)[-1].strip()
		else:
			postfix = ""

		return buildReleaseMessage(item, 'Konjiki no Wordmaster', vol, chp, frag=frag, postfix=postfix)

	if ('Chapters' in tags and 'Konjiki no Wordmaster' in tags) \
		or 'Konjiki no Wordmaster Web Novel Chapters' in tags   \
		or 'Konjiki' in tags                                    \
		or (src == 'Loliquent' and 'Konjiki no Wordmaster' in title):
		postfix = title.split("–", 1)[-1].strip()
		return buildReleaseMessage(item, 'Konjiki no Wordmaster', vol, chp, frag=frag, postfix=postfix)

	elif 'Konjiki no Wordmaster Chapters' in tags                                        \
		or 'Konjiki no Moji Tsukai' in tags                                              \
		or (src == 'Kiriko Translations' and ('KnW' in tags or 'KnW Chapter' in title))  \
		or (src == 'CapsUsingShift Tl' and 'Konjiki no Wordmaster' in title)             \
		or (src == 'Pummels Translations' and 'Konjiki no Word Master Chapter' in title) \
		or (src == 'XCrossJ' and 'Konjiki no Moji Tsukai' in title)                      \
		or (src == 'Insignia Pierce' and 'Konjiki no Word Master Chapter' in title):
		postfix = title.split(":", 1)[-1].strip()
		return buildReleaseMessage(item, 'Konjiki no Wordmaster', vol, chp, frag=frag, postfix=postfix)
		# elif 'Konjiki no Moji Tsukai' in tags:

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
	if 'ALBT Chapter Release' in item['tags'] and (vol or chp or postfix):
		return buildReleaseMessage(item, 'Assassin Landlord Beauty Tenants', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Sword And Game
####################################################################################################################################################
def extractSwordAndGame(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'The Rising of the Shield Hero' in item['tags'] and 'chapter' in [tmp.lower() for tmp in item['tags']]:
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
	if 'World teacher'.lower() in item['title'].lower() or 'World teacher' in item['tags']:
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
	if "Don't be So Proud" in item['tags']:
		return buildReleaseMessage(item, "Don't be So Proud", vol, chp, frag=frag, postfix=postfix)
	if 'Mo Bao Fei Bao' in item['tags']:
		return buildReleaseMessage(item, 'Mo Bao Fei Bao', vol, chp, frag=frag, postfix=postfix)
	if 'Your Humble Servant is Guilty!' in item['tags']:
		return buildReleaseMessage(item, 'Your Humble Servant is Guilty!', vol, chp, frag=frag, postfix=postfix)

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
	if 'Ryuugoroshi no Sugosuhibi' in item['title'] or 'Ryuugoroshi no Sugosu Hibi' in item['tags']:
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if ":" in item['title']:
		postfix = item['title'].split(":", 1)[-1]
	if 'Maou the Yuusha' in item['tags'] and 'chapter' in [tmp.lower() for tmp in item['tags']]:
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
	if not (chp or vol):
		return False
	if "preview" in item['title']:
		return False

	title = item['title']
	if 'Destruction Flag Noble Girl Villainess' in title or 'Destruction Flag Otome' in title:
		return buildReleaseMessage(item, 'Destruction Flag Otome', vol, chp, frag=frag, postfix=postfix)
	if 'Demon King Reincarnation' in title:
		return buildReleaseMessage(item, 'I, the Demon King, have become a noble girl villainess? Hah, what a joke.', vol, chp, frag=frag, postfix=postfix)
	if 'Slave Girl –' in title:
		return buildReleaseMessage(item, 'Demotion Trip ~The Magic Girl Swordsman from the Hero’s Party Stumbled into Another World and Became a Slave', vol, chp, frag=frag, postfix=postfix)
	if 'Flight of the Dragon, Dance of the Phoenix' in title:
		return buildReleaseMessage(item, 'Dragon Flies Phoenix Dances', vol, chp, frag=frag, postfix=postfix)
	elif 'Dragon Life' in title:
		return buildReleaseMessage(item, 'Dragon Life', vol, chp, frag=frag, postfix=postfix)
	elif 'World Teacher' in title:
		return buildReleaseMessage(item, 'World Teacher - Isekaishiki Kyouiku Agent', vol, chp, frag=frag, postfix=postfix)
	elif 'jashin sidestory' in title.lower() or 'Jashin Average Side Story' in title:
		return buildReleaseMessage(item, 'Evil God Average – Side Story', vol, chp, frag=frag, postfix=postfix)
	elif 'Heibon' in title:
		return buildReleaseMessage(item, 'E? Heibon Desu yo??', vol, chp, frag=frag, postfix=postfix)
	elif 'eliza chapter' in title.lower():
		if "–" in title and not postfix:
			postfix = title.split("–")[-1]
		return buildReleaseMessage(item, 'I Reincarnated as a Noble Girl Villainess, but why did it turn out this way', vol, chp, frag=frag, postfix=postfix)
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
	ltags = [tmp.lower() for tmp in item['tags']]

	if 'dawn traveler' in ltags and 'translation' in ltags:
		return buildReleaseMessage(item, 'Dawn Traveler', vol, chp, frag=frag, postfix=postfix)
	if 'different world business symbol' in ltags and 'translation' in ltags:
		return buildReleaseMessage(item, 'Different World Business Symbol', vol, chp, frag=frag, postfix=postfix)
	if 'star sea lord' in ltags and 'translation' in ltags:
		return buildReleaseMessage(item, 'Star Sea Lord', vol, chp, frag=frag, postfix=postfix)
	if 'tensei shitara slime datta ken' in ltags and 'translation' in ltags:
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	# Whoooo, tag case typos!
	if any(['god of thunder' == val.lower() for val in item['tags']]) and (vol or chp):
		if ":" in item['title']:
			postfix = item['title'].split(":", 1)[-1]
		return buildReleaseMessage(item, 'God of Thunder', vol, chp, frag=frag, postfix=postfix)
	if 'Beseech the devil'.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'Beseech the Devil', vol, chp, frag=frag, postfix=postfix)
	if 'Goblin' in item['tags']:
		return buildReleaseMessage(item, 'Goblin', vol, chp, frag=frag, postfix=postfix)
	if 'King of the Eternal Night' in item['tags']:
		return buildReleaseMessage(item, 'King of the Eternal Night', vol, chp, frag=frag, postfix=postfix)
	if 'Martial World' in item['tags']:
		return buildReleaseMessage(item, 'Martial World', vol, chp, frag=frag, postfix=postfix)

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

	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "History's Number One Founder" in item['tags']:
		if ":" in item['title']:
			postfix = item['title'].split(":", 1)[-1]
		return buildReleaseMessage(item, "History's Number One Founder", vol, chp, frag=frag, postfix=postfix)
	if "Shura's Wrath" in item['tags'] or "Shura\"s Wrath" in item['tags']:
		if ":" in item['title']:
			postfix = item['title'].split(":", 1)[-1]
		return buildReleaseMessage(item, 'Shura\'s Wrath', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# Tomorolls
####################################################################################################################################################
def extractTomorolls(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'Cicada as Dragon' in item['tags'] or 'Semi Datte Tensei Sureba Ryuu Ni Naru' in item['title']:
		return buildReleaseMessage(item, 'Cicada as Dragon', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# Totokk\'s Translations
####################################################################################################################################################
def extractTotokk(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	# Lawl, title typo
	if '[SYWZ] Chapter' in item['title'] or '[SWYZ] Chapter' in item['title'] \
		or '[SYWZ]' in item['title'] or 'Shen Yin Wang Zuo, Chapter' in item['title']:
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
#
####################################################################################################################################################
def extractRebirthOnlineWorld(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Earth Core' in item['tags']:
		return buildReleaseMessage(item, 'Earth\'s Core', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'goddess grant me a girlfriend' in item['tags']:
		return buildReleaseMessage(item, 'Goddess Grant me a Girlfriend', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Loiterous' in item['tags']:
		return buildReleaseMessage(item, 'Loiterous', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if "tdadp" in item['title'].lower() or 'To deprive a deprived person episode'.lower() in item['title'].lower():
		if vol and chp:
			vol = None
		return buildReleaseMessage(item, 'To Deprive a Deprived Person', vol, chp, frag=frag, postfix=postfix)
	if "Lazy Dragon".lower() in item['title'].lower():
		return buildReleaseMessage(item, 'Taidana Doragon wa Hatarakimono', vol, chp, frag=frag, postfix=postfix)
	if "Neta Chara".lower() in item['title'].lower():
		return buildReleaseMessage(item, 'Neta Chara', vol, chp, frag=frag, postfix=postfix)
	if "Destination of Crybird".lower() in item['title'].lower():
		return buildReleaseMessage(item, 'Destination of Crybird', vol, chp, frag=frag, postfix=postfix)
	if "Immortal God Emperor".lower() in item['title'].lower():
		return buildReleaseMessage(item, 'Immortal God Emperor', vol, chp, frag=frag, postfix=postfix)
	if "Zombie master".lower() in item['title'].lower():
		return buildReleaseMessage(item, 'Zombie Master', vol, chp, frag=frag, postfix=postfix)
	if "Werewolf chapter".lower() in item['title'].lower():
		return buildReleaseMessage(item, 'Werewolf chapter', vol, chp, frag=frag, postfix=postfix)
	if 'Master of Dungeon'.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'TMaster of Dungeon', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'TRTS(The Rude Time Stopper)'.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'The Rude Time Stopper', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
# Ark Machine Translations
####################################################################################################################################################
def extractArkMachineTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'ark volume' in item['title'].lower() or \
		'ark the legend volume' in item['title'].lower():
		return buildReleaseMessage(item, 'Ark', vol, chp, frag=frag, postfix=postfix)

	if 'lms volume' in item['title'].lower():
		return buildReleaseMessage(item, 'Legendary Moonlight Sculptor', vol, chp, frag=frag, postfix=postfix)

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
	if 'Han-Ryuu Shoujo no Dorei Raifu' in item['tags'] and (chp or vol or frag or postfix):
		return buildReleaseMessage(item, 'Han-Ryuu Shoujo no Dorei Raifu', vol, chp, frag=frag, postfix=postfix)
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
		'Sovereign of the Three Realms',
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if not postfix and '–' in item['title']:
		postfix = item['title'].split("–")[-1]
	if 'Ore no Osananajimi wa Joshikousei de Yuusha' in item['tags']:
		return buildReleaseMessage(item, 'Ore no Osananajimi wa Joshikousei de Yuusha', vol, chp, frag=frag, postfix=postfix)
	if 'Oukoku e Tsuzuku Michi' in item['tags']:
		return buildReleaseMessage(item, 'Oukoku e Tsuzuku Michi', vol, chp, frag=frag, postfix=postfix)
	if 'Takarakuji de 40-oku Atattandakedo' in item['tags']:
		return buildReleaseMessage(item, 'Takarakuji de 40 Oku Atattandakedo Isekai ni Ijuu Suru', vol, chp, frag=frag, postfix=postfix)
	if 'Jaaku Chika Teikoku' in item['tags']:
		return buildReleaseMessage(item, 'Jaaku Chika Teikoku', vol, chp, frag=frag, postfix=postfix)
	if 'Saenai Heroine no Sodatekata' in item['tags']:
		return buildReleaseMessage(item, 'Saenai Heroine no Sodatekata', vol, chp, frag=frag, postfix=postfix)
	if 'Genjitsushugisha no Oukokukaizouki' in item['tags']:
		return buildReleaseMessage(item, 'Genjitsushugisha no Oukokukaizouki', vol, chp, frag=frag, postfix=postfix)

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
	if 'KENS' in item['tags']:
		return buildReleaseMessage(item, 'Kamigoroshi no Eiyuu to Nanatsu no Seiyaku', vol, chp, frag=frag, postfix=postfix)

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

	if 'kuro no maou' in item['title'].lower() and 'chapter' in item['title'].lower() and (chp or vol):
		return buildReleaseMessage(item, 'Kuro no Maou', vol, chp, frag=frag, postfix=postfix)
	if 'kuro no maou' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Kuro no Maou', vol, chp, frag=frag, postfix=postfix)
	if 'maken no daydreamer' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Maken no Daydreamer', vol, chp, frag=frag, postfix=postfix)
	if 'knw' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Konjiki no Wordmaster', vol, chp, frag=frag, postfix=postfix)
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

	if not (chp or vol) or "preview" in item['title'].lower():
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

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	extr = re.search(r' ([A-Z])\d+', item['title'], flags=re.IGNORECASE)
	if extr:
		if vol and not chp:
			chp, vol = vol, chp
		ep_key = extr.group(1)
		if ep_key == "S":
			postfix = "Shun chapter"
		elif ep_key == "J" or ep_key == "Y":
			postfix = "Julius chapter"
		elif ep_key == "K":
			postfix = "Katia chapter"
		elif ep_key == "B":
			postfix = "Balto chapter"
	if re.search(r'blood \d+', item['title'], flags=re.IGNORECASE):
		postfix = "Blood Chapter"



	if 'kumo desu ga, nani ka?' in item['title'].lower()     \
		or 'kumo desu ka, nani ga?' in item['title'].lower() \
		or 'kumo desu ga, nani ga?' in item['title'].lower():
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

	ltags = [tmp.lower() for tmp in item['tags']]

	if 'tensei shitara slime datta ken' in ltags:
		return buildReleaseMessage(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)
	if '1000 nin no homunkurusu no shoujo tachi ni kakomarete isekai kenkoku' in ltags:
		return buildReleaseMessage(item, '1000 nin no Homunkurusu no Shoujo tachi ni Kakomarete Isekai Kenkoku', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# 'Shiroyukineko Translations'
####################################################################################################################################################
def extractShiroyukineko(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'DOP' in item['tags'] or 'Descent of the Phoenix: 13 Year Old Princess Consort' in item['tags'] or item['title'].startswith('DOP Chapter'):
		return buildReleaseMessage(item, 'Descent of the Phoenix: 13 Year Old Princess Consort', vol, chp, frag=frag, postfix=postfix)
	if 'LLS' in item['tags'] or 'Long Live Summons!' in item['tags']:
		return buildReleaseMessage(item, 'Long Live Summons!', vol, chp, frag=frag, postfix=postfix)
	if 'VW:UUTS' in item['tags'] or 'Virtual World: Unparalled Under The Sky' in item['tags']:
		return buildReleaseMessage(item, 'Virtual World: Unparalleled under the Sky', vol, chp, frag=frag, postfix=postfix)
	if 'Ze Tian Ji' in item['tags'] or 'ZTJ Chapter' in item['title']:
		return buildReleaseMessage(item, 'Ze Tian Ji', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# 'NoviceTranslator'
####################################################################################################################################################
def extractNoviceTranslator(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Martial God Space Chapter' in item['title'] or 'Martial God Space' in item['tags']:
		return buildReleaseMessage(item, 'Martial God Space', vol, chp, frag=frag, postfix=postfix)
	if 'Dragon Martial Emperor Chapter' in item['title']:
		return buildReleaseMessage(item, 'Martial God Space', vol, chp, frag=frag, postfix=postfix)
	if 'Genius Sword Immortal' in item['tags']:
		return buildReleaseMessage(item, 'Genius Sword Immortal', vol, chp, frag=frag, postfix=postfix)
	if 'God of Destruction' in item['tags']:
		return buildReleaseMessage(item, 'God of Destruction', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
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

	if '10 nen goshi no HikiNEET o Yamete Gaishutsushitara Jitaku goto Isekai ni Ten’ishiteta' in item['tags'] or \
		 'When I was going out from my house to stop become a Hiki-NEET after 10 years I was transported to another world' in item['tags']:
		return buildReleaseMessage(item, '10 nen goshi no HikiNEET o Yamete Gaishutsushitara Jitaku goto Isekai ni Ten’ishiteta', vol, chp, frag=frag, postfix=postfix)
	elif 'Takarakuji de 40 Oku Atattanda kedo Isekai ni Ijuusuru' in item['tags']:
		return buildReleaseMessage(item, 'Takarakuji de 40 Oku Atattanda kedo Isekai ni Ijuusuru', vol, chp, frag=frag, postfix=postfix)
	elif 'Tenseisha wa Cheat o Nozomanai' in item['tags']:
		return buildReleaseMessage(item, 'Tenseisha wa Cheat o Nozomanai', vol, chp, frag=frag, postfix=postfix)
	elif 'Genjitsushugisha no Oukoku Kaizouki' in item['tags']:
		return buildReleaseMessage(item, 'Genjitsushugisha no Oukoku Kaizouki', vol, chp, frag=frag, postfix=postfix)
	elif 'I Won 4 Billion in a Lottery But I Went to Another World' in item['tags']:
		return buildReleaseMessage(item, 'Takarakuji de 40 Oku Atattanda kedo Isekai ni Ijuusuru', vol, chp, frag=frag, postfix=postfix)
	elif  'The Curious Girl and The Traveler' in item['tags']:
		return buildReleaseMessage(item,  'The Curious Girl and The Traveler', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	elif  'Yukkuri Oniisan' in item['tags']:
		return buildReleaseMessage(item,  'Yukkuri Oniisan', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

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
		return buildReleaseMessage(item, 'Zectas', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'LMS' in item['tags'] and vol and chp:
		return buildReleaseMessage(item, 'Legendary Moonlight Sculptor', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractDreadfulDecoding(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Gun Gale Online' in item['tags']:
		return buildReleaseMessage(item, 'Sword Art Online Alternative - Gun Gale Online', vol, chp, frag=frag, postfix=postfix)
	if 'RotTS' in item['tags']:
		return buildReleaseMessage(item, 'Sword Art Online Alternative - Rondo of the Transient Sword', vol, chp, frag=frag, postfix=postfix)

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Return of the former hero' in item['tags']:
		return buildReleaseMessage(item, 'Return of the Former Hero', vol, chp, frag=frag, postfix=postfix)
	if 'Dragon egg' in item['tags']:
		return buildReleaseMessage(item, 'Reincarnated as a dragon’s egg ～Lets aim to be the strongest～', vol, chp, frag=frag, postfix=postfix)

	if 'Summoning at random' in item['tags']:
		return buildReleaseMessage(item, 'Summoning at Random', vol, chp, frag=frag, postfix=postfix)

	if 'Legend' in item['tags']:
		return buildReleaseMessage(item, 'レジェンド', vol, chp, frag=frag, postfix=postfix)

	if 'Death game' in item['tags']:
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

	if not (chp or vol):
		return False
	if "preview" in item['title']:
		return False

	ltags = [tmp.lower() for tmp in item['tags']]

	if 'monogatari no naka no hito' in ltags:
		return buildReleaseMessage(item, 'Monogatari no Naka no Hito', vol, chp, frag=frag, postfix=postfix)
	if 'five way heaven' in ltags:
		return buildReleaseMessage(item, 'Five Way Heaven', vol, chp, frag=frag, postfix=postfix)
	if 'because i’m a weapon shop uncle' in ltags or \
		'because im a weapon shop uncle' in item['title'].lower().replace("’", "").replace("'", "") or \
		'because im a weapons shop uncle' in item['title'].lower().replace("’", "").replace("'", ""):
		return buildReleaseMessage(item, 'Because I\'m a Weapon Shop Uncle', vol, chp, frag=frag, postfix=postfix)
	if 'maken no daydreamer' in ltags:
		return buildReleaseMessage(item, 'Maken no Daydreamer', vol, chp, frag=frag, postfix=postfix)
	if 'magic robot aluminare' in ltags:
		return buildReleaseMessage(item, 'Magic Robot Aluminare', vol, chp, frag=frag, postfix=postfix)
	if  'it seems like i got reincarnated into the world of a yandere otome game.' in ltags:
		return buildReleaseMessage(item,  'It seems like I got reincarnated into the world of a Yandere Otome game.', vol, chp, frag=frag, postfix=postfix)
	if 'kuro no maou' in ltags:
		return buildReleaseMessage(item, 'Kuro no Maou', vol, chp, frag=frag, postfix=postfix)
	if "what's your gender, princess?" in ltags:
		return buildReleaseMessage(item, "What's Your Gender, Princess?", vol, chp, frag=frag, postfix=postfix)
	if 'kumo desu ga, nani ka?' in ltags:
		return buildReleaseMessage(item, 'Kumo Desu ga, Nani ka?', vol, chp, frag=frag, postfix=postfix)
	if 'magic mechanics shuraba' in ltags:
		return buildReleaseMessage(item, 'Magic Mechanics Shuraba', vol, chp, frag=frag, postfix=postfix)
	if "shura's wrath" in ltags:
		return buildReleaseMessage(item, "Shura's Wrath", vol, chp, frag=frag, postfix=postfix)
	if 'against the gods' in ltags:
		return buildReleaseMessage(item, 'Against The Gods', vol, chp, frag=frag, postfix=postfix)
	if 'b group no shounen' in ltags:
		return buildReleaseMessage(item, 'B Group no Shounen', vol, chp, frag=frag, postfix=postfix)
	if 'i reincarnated as a noble girl villainess, but why did it turn out this way' in ltags or \
		'i reincarnated as a noble girl villainess, but why did it turn out this way?' in ltags:
		return buildReleaseMessage(item, 'I Reincarnated as a Noble Girl Villainess, but why did it turn out this way', vol, chp, frag=frag, postfix=postfix)
	if 'slave career planner' in ltags or 'Slave Career Planner Volume' in item['title']:
		return buildReleaseMessage(item, 'Slave Career Planner', vol, chp, frag=frag, postfix=postfix)
	if 'the simple life of killing demons' in ltags:
		return buildReleaseMessage(item, 'The Simple Life of Killing Demons', vol, chp, frag=frag, postfix=postfix)
	if 'tensei shitara slime datta ken' in ltags:
		return buildReleaseMessage(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)
	if 'godly hunter' in ltags:
		return buildReleaseMessage(item, 'Godly Hunter', vol, chp, frag=frag, postfix=postfix)
	if 'kamigoroshi no eiyuu to nanatsu no seiyaku' in ltags:
		return buildReleaseMessage(item, 'Kamigoroshi no Eiyuu to Nanatsu no Seiyaku', vol, chp, frag=frag, postfix=postfix)
	if 'and so the girl obtained a wicked girl’s body' in ltags:
		return buildReleaseMessage(item, 'And so the Girl Obtained a Wicked Girl\'s Body', vol, chp, frag=frag, postfix=postfix)
	if 'shen mu' in ltags:
		return buildReleaseMessage(item, 'Shen Mu', vol, chp, frag=frag, postfix=postfix)
	if 'the demonic king chases his wife: the rebellious good-for-nothing miss' in ltags or \
		'dkc chapter'.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'The Demonic King Chases His Wife: The Rebellious Good-for-nothing Miss', vol, chp, frag=frag, postfix=postfix)
	if 'the saint’s recovery magic is a degraded version of mine' in ltags:
		return buildReleaseMessage(item, 'The Saint’s Recovery Magic is a Degraded Version of Mine', vol, chp, frag=frag, postfix=postfix)
	if 'it seems like i got reincarnated into the world of a yandere otome game.' in ltags:
		return buildReleaseMessage(item, 'It seems like I got reincarnated into the world of a Yandere Otome game.', vol, chp, frag=frag, postfix=postfix)
	if 'Parallel World Pharmacy'.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'Parallel World Pharmacy', vol, chp, frag=frag, postfix=postfix)
	if 'no fatigue' in ltags:
		return buildReleaseMessage(item, 'No Fatigue', vol, chp, frag=frag, postfix=postfix)

	if 'Isekai Maou to Shoukan Shoujo Dorei Majutsu' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Isekai Maou to Shoukan Shoujo no Dorei Majutsu', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractEroLightNovelTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Adolescent Adam' in item['tags'] and (chp or vol):
		if 'Adolescent Adam 2' in item['title']:
			if not vol:
				vol = 1
			return buildReleaseMessage(item, 'Shishunki na Adam', vol+1, chp, frag=frag, postfix=postfix)
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
def extractWuxiaSociety(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'The Heaven Sword and Dragon Sabre' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'The Heaven Sword and Dragon Sabre', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWuxiaHeroes(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Conquest' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Conquest', vol, chp, frag=frag, postfix=postfix)
	if 'Blood Hourglass' in item['title']:
		return buildReleaseMessage(item, 'Blood Hourglass', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractLonahora(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if "Earth's Core" in item['tags'] and (chp and vol):
		return buildReleaseMessage(item, "Earth's Core", vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractRadiantTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Chapter Release' in item['tags']:
		if ('Child of Light' in item['tags'] or 'Guang Zhi Zi' in item['tags']) and (chp or vol):
			return buildReleaseMessage(item, 'Guang Zhi Zi', vol, chp, frag=frag, postfix=postfix)
		if ('Bing Huo Mo Chu' in item['tags'] or 'Magic Chef of Ice and Fire' in item['tags']) and (chp or vol):
			return buildReleaseMessage(item, 'Bing Huo Mo Chu', vol, chp, frag=frag, postfix=postfix)
		if ('Lord Xue Ying' in item['tags']) and (chp or vol):
			return buildReleaseMessage(item, 'Xue Ying Ling Zhu', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractTalesOfMU(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if any('volume' in tag.lower() for tag in item['tags']) and (chp or vol):
		return buildReleaseMessage(item, 'Tales of MU', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractYoujinsite(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if '[God & Devil World]' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Shenmo Xitong', vol, chp, frag=frag, postfix=postfix)

	if '[LBD&A]' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Line between Devil and Angel', vol, chp, frag=frag, postfix=postfix)

	if '[VW: Conquer the World]' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'VW: Conquering the World', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractYoushoku(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'The Other World Dining Hall' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'The Other World Dining Hall', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractZSW(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Shen Mu' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Shen Mu', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractA0132(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if (chp or vol):
		return buildReleaseMessage(item, 'Terror Infinity', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractLostInTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Third Prince Elmer' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item,  'Third Prince Elmer', vol, chp, frag=frag, postfix=postfix)
	if 'Otoko Aruji' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item,  'Otoko Aruji', vol, chp, frag=frag, postfix=postfix)
	if "Sword Saint's Disciple" in item['tags'] and (chp or vol):
		return buildReleaseMessage(item,  "Sword Saint's Disciple", vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractPeasKingdom(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	ltags = [tmp.lower() for tmp in item['tags']]
	if 'second chance' in ltags and (chp or vol):
		return buildReleaseMessage(item, 'Second Chance: a Wonderful New Life', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractCircusTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'German Translation' in item['tags']:
		return False
	if 'Turkish Translation' in item['tags']:
		return False
	if 'Spanish translation' in item['tags']:
		return False

	if chp or vol:
		return buildReleaseMessage(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractDistractedTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	ltags = [tmp.lower() for tmp in item['tags']]
	if 'gonna get captured' in ltags and (chp or vol):
		return buildReleaseMessage(item, "Like Hell I’m Gonna Get Captured!", vol, chp, frag=frag, postfix=postfix)

	if 'Get Captured: Chapter' in item['title'] and (chp or vol):
		return buildReleaseMessage(item, "Like Hell I’m Gonna Get Captured!", vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractForgottenConqueror(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if chp:
		return buildReleaseMessage(item, "Forgotten Conqueror", vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractHoldX(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Shoya Kara Hajimeru Ai Aru Seikatsu' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Shoya Kara Hajimeru Ai Aru Seikatsu', vol, chp, frag=frag, postfix=postfix)
	if 'Bishoujo wo Jouzu ni Nikubenki ni Suru Houhou' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Bishoujo wo Jouzu ni Nikubenki ni Suru Houhou', vol, chp, frag=frag, postfix=postfix)
	if  'Riaru de Reberu Age Shitara Hobo Chītona Jinsei ni Natta' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item,  'Riaru de Reberu Age Shitara Hobo Chītona Jinsei ni Natta', vol, chp, frag=frag, postfix=postfix)
	if 'Erogacha' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Erogacha', vol, chp, frag=frag, postfix=postfix)
	if 'Ore no Sekai no Kouryakubon' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Ore no Sekai no Kouryakubon', vol, chp, frag=frag, postfix=postfix)
	if 'Takarakuji de 40 oku Atatta Ndakedo i Sekai ni Ijū Suru' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Takarakuji de 40 oku Atatta Ndakedo i Sekai ni Ijū Suru', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractSolitaryTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'The Great Ruler' in item['tags']:
		return buildReleaseMessage(item, 'The Great Ruler', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################

def extractThyaeria(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Tales of Demons and Gods' in item['tags']:
		return buildReleaseMessage(item, 'Tales of Demons and Gods', vol, chp, frag=frag, postfix=postfix)
	if 'Warlock of the Magus World' in item['tags']:
		return buildReleaseMessage(item, 'Warlock of the Magus World', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractPlaceOfLegends(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'The Fragile Monster Lord' in item['tags']:
		return buildReleaseMessage(item, 'The Fragile Monster Lord', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'The New Start' in item['tags']:
		return buildReleaseMessage(item, 'The New Start', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'The Rude Time Stopper' in item['tags']:
		return buildReleaseMessage(item, 'The Rude Time Stopper', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractLoiterous(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Loiterous' in item['tags'] and "chapter" in item['title'].lower():
		return buildReleaseMessage(item, 'Loiterous', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractMechaMushroom(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'YaoNie Bing Wang (WSK)' in item['title'] or   \
		'Yao Nie Bing Wang (WSK)' in item['title'] or \
		'YNBW (WSK)' in item['title']:
		return buildReleaseMessage(item, 'Yao Nie Bing Wang', vol, chp, frag=frag, postfix=postfix)
	if 'Jiang Ye Chapter' in item['title']:
		return buildReleaseMessage(item, 'Jiang Ye Chapter', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractShinsori(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Doll Dungeon' in item['title']:
		return buildReleaseMessage(item, 'Doll Dungeon', vol, chp, frag=frag, postfix=postfix)

	if 'Raising Slaves in Another World While on a Journey' in item['title']:
		return buildReleaseMessage(item, 'Raising Slaves in Another World While on a Journey', vol, chp, frag=frag, postfix=postfix)
	if 'Occupation: Adventurer ; Race: Various' in item['title'] or 'Race: Various' in item['tags']:
		return buildReleaseMessage(item, 'Occupation: Adventurer ; Race: Various', vol, chp, frag=frag, postfix=postfix)
	if 'Yuusha ga onna da to dame desu ka?' in item['title']:
		return buildReleaseMessage(item, 'Yuusha ga onna da to dame desu ka?', vol, chp, frag=frag, postfix=postfix)
	if 'The Bears Bear a Bare Kuma' in item['title'] or 'Kuma Kuma Kuma Bear' in item['title']:
		return buildReleaseMessage(item, 'Kuma Kuma Kuma Bear', vol, chp, frag=frag, postfix=postfix)
	if 'Silver Death' in item['title']:
		return buildReleaseMessage(item, 'Silver Death', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractSoaring(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	# If you release "teaser" chapters, you're a douche
	if "teaser" in item['title'].lower():
		return False

	if 'Limitless Sword God Chapter' in item['title'] or 'Limitless Sword God' in item['tags'] or 'LSG' in item['tags']:
		return buildReleaseMessage(item, 'Limitless Sword God', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractSoraTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "teaser" in item['title'].lower():
		return False

	if 'Isekai Mahou....' in item['tags']:
		return buildReleaseMessage(item, 'Isekai Mahou wa Okureteru!', vol, chp, frag=frag, postfix=postfix)

	print(item['title'])
	print(item['tags'])
	print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractAzurro(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if not 'translation project' in item['tags']:
		return False

	if 'A Naive Short-tempered Girl' in item['tags']:
		return buildReleaseMessage(item, 'A Naive Short-tempered Girl', vol, chp, frag=frag, postfix=postfix)
	if 'Substitute Bride' in item['tags']:
		return buildReleaseMessage(item, 'Substitute Bride', vol, chp, frag=frag, postfix=postfix)
	if 'Husband is Great Black Belly (老公是腹黑大人)' in item['tags']:
		return buildReleaseMessage(item, 'Husband is Great Black Belly', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractCloversNook(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'A mistaken marriage match: A generation of military counselor' in item['tags']:
		return buildReleaseMessage(item, 'A mistaken marriage match: A generation of military counselor', vol, chp, frag=frag, postfix=postfix)
	if 'A mistaken marriage match: Record of washed grievances' in item['tags']:
		return buildReleaseMessage(item, 'A mistaken marriage match: Record of washed grievances', vol, chp, frag=frag, postfix=postfix)
	if 'Three Marriages' in item['tags']:
		return buildReleaseMessage(item, 'Three Marriages', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractCookiePasta(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	return buildReleaseMessage(item, 'Douluo Dalu 2 - Jueshi Tangmen', vol, chp, frag=frag, postfix=postfix)

	print(item['title'])
	print(item['tags'])
	print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractXantAndMinions(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) and not "prologue" in item['title'].lower():
		return False
	if 'LV999 Villager' in item['title']:
		return buildReleaseMessage(item, 'LV999 Villager', vol, chp, frag=frag, postfix=postfix)
	if 'Boundary Labyrinth and the Foreign Magician' in item['title']:
		return buildReleaseMessage(item, 'Boundary Labyrinth and the Foreign Magician', vol, chp, frag=frag, postfix=postfix)
	if 'The Bears Bear a Bare Kuma' in item['title'] or 'Kuma Kuma Kuma Bear' in item['title']:
		return buildReleaseMessage(item, 'Kuma Kuma Kuma Bear', vol, chp, frag=frag, postfix=postfix)
	if "Black Knight" in item['title']:
		return buildReleaseMessage(item, "The Black Knight Who Was Stronger than even the Hero", vol, chp, frag=frag, postfix=postfix)

	print(item['title'])
	print(item['tags'])
	print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractTotallyInsaneTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "PMG" in item['tags']:
		return buildReleaseMessage(item, "Peerless Martial God", vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractNovelsNao(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Martial God Space' in item['tags']:
		return buildReleaseMessage(item, 'Martial God Space', vol, chp, frag=frag, postfix=postfix)
	if 'Martial Peak' in item['tags']:
		return buildReleaseMessage(item, 'Martial Peak', vol, chp, frag=frag, postfix=postfix)
	if 'Mythical Tyrant' in item['tags']:
		return buildReleaseMessage(item, 'Mythical Tyrant', vol, chp, frag=frag, postfix=postfix)
	if 'Genius Sword Immortal' in item['tags']:
		return buildReleaseMessage(item, 'Genius Sword Immortal', vol, chp, frag=frag, postfix=postfix)
	if 'King Shura' in item['tags']:
		return buildReleaseMessage(item, 'King Shura', vol, chp, frag=frag, postfix=postfix)
	if 'The Six Immortals' in item['tags']:
		return buildReleaseMessage(item, 'The Six Immortals', vol, chp, frag=frag, postfix=postfix)
	if 'Devouring The Heavens' in item['tags']:
		return buildReleaseMessage(item, 'Devouring The Heavens', vol, chp, frag=frag, postfix=postfix)
	if 'Dragon Martial Emperor' in item['tags']:
		return buildReleaseMessage(item, 'Dragon Martial Emperor', vol, chp, frag=frag, postfix=postfix)
	if 'Three Marriages' in item['tags']:
		return buildReleaseMessage(item, 'Three Marriages', vol, chp, frag=frag, postfix=postfix)
	if 'I Fell and Thus I Must Rise Again!' in item['tags']:
		return buildReleaseMessage(item, 'I Fell and Thus I Must Rise Again!', vol, chp, frag=frag, postfix=postfix)
	if 'The Unseeing Eyes' in item['tags']:
		return buildReleaseMessage(item, 'The Unseeing Eyes', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'The Gemstone Chronicles' in item['tags']:
		return buildReleaseMessage(item, 'The Gemstone Chronicles', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Apocalypse Now' in item['tags']:
		return buildReleaseMessage(item, 'Apocalypse Now', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'God of Destruction' in item['tags']:
		return buildReleaseMessage(item, 'God of Destruction', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'The Song of Swords' in item['tags']:
		return buildReleaseMessage(item, 'The Song of Swords', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if "Dragon's Soul" in item['tags']:
		return buildReleaseMessage(item, "Dragon's Soul", vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	print(item['title'])
	print(item['tags'])
	print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractMachineSlicedBread(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	# No guarantee we have chapter numbers here, unfortunately.

	if 'Charm TL' in item['tags']:
		return buildReleaseMessage(item, 'I made a slave harem using a charm cheat in a different world.', vol, chp, frag=frag, postfix=postfix)
	if 'Cheatman TL' in item['tags']:
		return buildReleaseMessage(item, 'Joudan Mitaina Chiito Nouryouku de Isekai ni Tensei shi, Sukikatte suru Hanashi', vol, chp, frag=frag, postfix=postfix)
	if 'Zombie Emperor TL' in item['tags']:
		return buildReleaseMessage(item, 'The Bloodshot One-Eyed Zombie Emperor', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWatDaMeow(item):

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Commushou' in item['tags']:
		return buildReleaseMessage(item, 'Commushou no Ore ga, Koushou Skill ni Zenfurishite Tenseishita Kekka', vol, chp, frag=frag, postfix=postfix)
	if 'Kitsune-sama' in item['tags']:
		return buildReleaseMessage(item, 'Isekai Kichattakedo Kaerimichi doko?', vol, chp, frag=frag, postfix=postfix)
	if 'JuJoku' in item['title']:
		return buildReleaseMessage(item, 'Junai X Ryoujoku Kompurekusu', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractDreamsOfJianghu(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'TBVW' in item['tags']:
		return buildReleaseMessage(item, 'To Be A Virtuous Wife', vol, chp, frag=frag, postfix=postfix)
	if 'WC' in item['tags']:
		return buildReleaseMessage(item, 'World of Cultivation', vol, chp, frag=frag, postfix=postfix)

	print(item['title'])
	print(item['tags'])
	print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWolfieTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'The amber sword' in item['tags']:
		return buildReleaseMessage(item, 'The Amber Sword', vol, chp, frag=frag, postfix=postfix)
	if 'The latest game is too amazing' in item['tags']:
		return buildReleaseMessage(item, 'The Latest Game is too Amazing', vol, chp, frag=frag, postfix=postfix)
	if 'The strategy to become good at magic' in item['tags']:
		return buildReleaseMessage(item, 'The Strategy to Become Good at Magic', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractNutty(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'A Mistaken Marriage Match' in item['tags'] and 'a generation of military counselor' in item['tags']:
		return buildReleaseMessage(item, 'A mistaken marriage match: A generation of military counselor', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractDaoSeekerBlog(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Otherworldly Evil Monarch' in item['tags'] or 'Chapter' in item['title']:
		return buildReleaseMessage(item, 'Otherworldly Evil Monarch', vol, chp, frag=frag, postfix=postfix)

	print(item['title'])
	print(item['tags'])
	print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractCeruleonice(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'martial emperor reborn' in item['tags']:
		return buildReleaseMessage(item, 'Martial Emperor Reborn', vol, chp, frag=frag, postfix=postfix)
	if 'Totem' in item['tags']:
		return buildReleaseMessage(item, 'Totem', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractTrungtNguyen(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Underdog Versus Boss' in item['tags']:
		return buildReleaseMessage(item, 'Underdog Versus Boss', vol, chp, frag=frag, postfix=postfix)
	if 'Beloved Little Treasure' in item['tags']:
		return buildReleaseMessage(item, 'Beloved Little Treasure', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractTaffyTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'CCM' in item['tags']:
		return buildReleaseMessage(item, 'Close Combat Mage', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractBeginningAfterTheEnd(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if "Chapter" in item['title']:
		return buildReleaseMessage(item, 'The Beginning After The End', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractVerathragana(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if "Chapter" in item['title']:
		return buildReleaseMessage(item, 'The Prince Of Nilfheim', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractOneManArmy(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if "DBWG – Chapter" in item['title'] or 'Dragon-Blooded War God' in item['tags']:
		return buildReleaseMessage(item, 'Dragon-Blooded War God', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractBcat00(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Law of the devil' in item['title']:
		return buildReleaseMessage(item, 'Law of the Devil', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractFiveStar(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Xian Ni' in item['title']:
		return buildReleaseMessage(item, 'Xian Ni', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractOKTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Oyaji Kanojo' in item['tags']:
		return buildReleaseMessage(item, 'Oyaji Kanojo', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractUltimateArcane(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Isekai ni kanaderu densetsu ~toki wo tomeru mono~' in item['tags']:
		return buildReleaseMessage(item, 'Isekai ni kanaderu densetsu ~toki wo tomeru mono~', vol, chp, frag=frag, postfix=postfix)
	if 'JIKUU MAHOU DE ISEKAI TO CHIKYUU WO ITTARIKITARI' in item['tags']:
		return buildReleaseMessage(item, 'Jikuu Mahou de Isekai to Chikyuu wo ittarikitari', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractManaTankMagus(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Mana Tank Magus' in item['tags']:
		return buildReleaseMessage(item, 'Mana Tank Magus', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractRainbowTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Myriad of Shades' in item['tags']:
		return buildReleaseMessage(item, 'Myriad of Shades', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractCtrlAlcala(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Chronicles Of Adrian Weiss Chapter'.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'Starry Heaven Saga: The Chronicles Of Adrian Weiss', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Magical Tournament Volume' in item['title']:
		return buildReleaseMessage(item, 'Magical Tournament: Rise Of The Black Swan', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Type: Hybrid' in item['title']:
		return buildReleaseMessage(item, 'Type: Hybrid', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Elementals:' in item['title'] or 'Elementals Chapter' in item['title']:
		return buildReleaseMessage(item, 'Elementals: Crystal Garden', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractKamiTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	# Most of Kami Translation's projects are manga. They only do one ln
	if 'Game Sensou' in item['tags']:
		return buildReleaseMessage(item, 'Boku to Kanojo no Game Sensou', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractOmgitsaray(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if "chapter" in item['title'].lower():
		return buildReleaseMessage(item, '9 Heavenly Thunder Manual', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractReddyCreations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if "rigel" in item['title'].lower():
		return buildReleaseMessage(item, 'Rigel', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	else:
		return buildReleaseMessage(item, 'Riddick/ Against the Heavens', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractShinSekaiYori(item):

	chStr = ""
	for tag in item['tags']:
		if "chapter" in tag.lower():
			chStr = chStr + " " + tag

	chStr += " " + item['title']

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(chStr)
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if frag:
		frag = frag / 10

	return buildReleaseMessage(item, 'Shin Sekai yori', vol, chp, frag=frag, postfix=postfix)

####################################################################################################################################################
#
####################################################################################################################################################
def extractKobatoChanDaiSukiScan(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	# Return of `None` makes the "Missed item" filter system ignore the return.
	if 'Lookism' in item['tags'] or 'webtoon' in item['tags']:
		return None # No webcomics plz

	if 'God of Crime' in item['tags'] :
		return buildReleaseMessage(item, 'God of Crime', vol, chp, frag=frag, postfix=postfix)
	if 'Kenkyo kenjitsu o motto ni ikite orimasu!' in item['tags']:
		return buildReleaseMessage(item, 'Kenkyo, Kenjitsu o Motto ni Ikite Orimasu!', vol, chp, frag=frag, postfix=postfix)
	if 'God of Thunder' in item['tags']:
		return buildReleaseMessage(item, 'God of Thunder', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractPrinceRevolution(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Romance RPG' in item['tags'] :
		return buildReleaseMessage(item, 'Romance RPG', vol, chp, frag=frag, postfix=postfix)
	if 'The Legend of Sun Knight' in item['tags'] :
		return buildReleaseMessage(item, 'The Legend of Sun Knight', vol, chp, frag=frag, postfix=postfix)
	if 'Dominions End' in item['tags'] :
		return buildReleaseMessage(item, 'Dominions End', vol, chp, frag=frag, postfix=postfix)
	if '½ Prince' in item['tags'] :
		return buildReleaseMessage(item, '½ Prince', vol, chp, frag=frag, postfix=postfix)
	if 'killvsprince' in item['tags'] :
		return buildReleaseMessage(item, 'Kill No More VS 1/2 Prince', vol, chp, frag=frag, postfix=postfix)
	if 'Illusions-Lies-Truth' in item['tags'] :
		return buildReleaseMessage(item, 'Illusions, Lies, Truth', vol, chp, frag=frag, postfix=postfix)
	if 'No Hero' in item['tags'] :
		return buildReleaseMessage(item, 'No Hero', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractAnathema(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	return buildReleaseMessage(item, 'Anathema', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

####################################################################################################################################################
#
####################################################################################################################################################
def extractKingJaahn(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	return buildReleaseMessage(item, 'Divine Progress', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

####################################################################################################################################################
#
####################################################################################################################################################
def extractUntunedTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	# TODO: Needs the facility to parse roman numerals!

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractRumorsBlock(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "Rumor's Block" in item['tags'] and "chapter" in item['title'].lower():
		return buildReleaseMessage(item, "Rumor's Block", vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractTwistedCogs(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if '–' in item['title']:
		postfix = item['title'].split('–', 1)[-1].strip()

	if "smut" in item['title'].lower():
		return buildReleaseMessage(item, 'Twisted Smut', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return buildReleaseMessage(item, 'Twisted Cogs', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

####################################################################################################################################################
#
####################################################################################################################################################
def extractReantoAnna(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Only I am not attacked in a world over runned by zombies' in item['tags'] or \
		("Chapter" in item['title'] and len(item['tags']) == 1 and 'Uncategorized' in item['tags']):
		return buildReleaseMessage(item, 'Only I am not attacked in a world overflowing with zombies', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractDawningHowls(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Dragon Flies Phoenix Dances' in item['tags'] :
		return buildReleaseMessage(item, 'Dragon Flies Phoenix Dances', vol, chp, frag=frag, postfix=postfix)
	if 'Eastern Palace' in item['tags'] :
		return buildReleaseMessage(item, 'Eastern Palace', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractSubudai11(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'My Beautiful Teacher Chapter' in item['title'] :
		return buildReleaseMessage(item, 'My Beautiful Teacher', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractGoddessGrantMeaGirlfriend(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'ggmag chapter' in item['tags']:
		return buildReleaseMessage(item, 'Goddess! Grant Me a Girlfriend!!', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractEndOnline(item):

	title = item['title']

	for tag in item['tags']:
		if "volume" in tag.lower():
			title = tag + " " + title

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(title)

	if not (chp or vol) or "published" in item['title'].lower():
		return False

	if 'End Online' in item['tags']:
		return buildReleaseMessage(item, 'End Online', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Chronicle of the Eternal' in item['tags']:
		return buildReleaseMessage(item, 'Chronicle of the Eternal', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractOneSecondSpring(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'The Princess Who Cannot Marry' in item['tags'] :
		return buildReleaseMessage(item, 'The Princess Who Cannot Marry', vol, chp, frag=frag, postfix=postfix)
	if 'Heavy Sweetness Ash-like Frost' in item['tags'] :
		return buildReleaseMessage(item, 'Heavy Sweetness Ash-like Frost', vol, chp, frag=frag, postfix=postfix)
	if 'Our Second Master' in item['tags'] :
		return buildReleaseMessage(item, 'Our Second Master', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractTranslationRaven(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Godly Hunter' in item['tags'] :
		return buildReleaseMessage(item, 'Godly Hunter', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractKoreanNovelTrans(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag):
		return False

	if 'Novel: Kill the Lights' in item['tags'] :
		return buildReleaseMessage(item, 'Kill the Lights', vol, chp, frag=frag, postfix=postfix)
	if 'Novel: Black Butterfly' in item['tags'] :
		return buildReleaseMessage(item, 'Black Butterfly', vol, chp, frag=frag, postfix=postfix)
	if 'NL Novel: Our House Pet' in item['tags'] :
		return buildReleaseMessage(item, 'Our House Pet', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractRoxism(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Bocchi Tenseiki' in item['tags'] and "chapter" in item['title'].lower():
		return buildReleaseMessage(item,  'Bocchi Tenseiki', vol, chp, frag=frag, postfix=postfix)
	if 'Seirei Gensouki ~Konna Sekai de Deaeta Kimi ni~' in item['tags'] and "chapter" in item['title'].lower():
		return buildReleaseMessage(item,  'Seirei Gensouki ~Konna Sekai de Deaeta Kimi ni~', vol, chp, frag=frag, postfix=postfix)
	if 'DHM' in item['tags'] and "chapter" in item['title'].lower():
		return buildReleaseMessage(item,  'Dungeon+Harem+Master', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractChineseBLTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Novel: City of Endless Rain' in item['tags'] :
		return buildReleaseMessage(item, 'City of Endless Rain', vol, chp, frag=frag, postfix=postfix)
	if 'Novel: Cold Sands' in item['tags'] :
		return buildReleaseMessage(item, 'Cold Sands', vol, chp, frag=frag, postfix=postfix)
	if 'Novel: The Rental Shop Owner' in item['tags'] :
		return buildReleaseMessage(item, 'The Rental Shop Owner', vol, chp, frag=frag, postfix=postfix)
	if 'Novel: Till Death Do Us Part' in item['tags'] :
		return buildReleaseMessage(item, 'Till Death Do Us Part', vol, chp, frag=frag, postfix=postfix)
	if 'Novel: Love Late' in item['tags'] :
		return buildReleaseMessage(item, 'Love Late', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractKahoim(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Soshite Shoujo wa Akujo no Karada o Te ni Ireru' in item['tags'] :
		return buildReleaseMessage(item, 'Soshite Shoujo wa Akujo no Karada o Te ni Ireru', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractSilvasLibrary(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if "Silva's Diary - Zero no Tsukaima" in item['tags'] :
		return buildReleaseMessage(item, "Silva's Diary - Zero no Tsukaima", vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractOriginNovels(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if '–' in item['title']:
		postfix = item['title'].split("–")[-1]
	if 'True Identity' in item['tags'] :
		return buildReleaseMessage(item, 'True Identity', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractOutspanFoster(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if "Chapter" in item['tags'] and 'ascension' in item['tags'] :
		return buildReleaseMessage(item, 'The Ascension Chronicle', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractDiwasteman(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "commentary" in item['title'].lower():
		return False
	if 'Parameter remote controller' in item['tags'] :
		return buildReleaseMessage(item, 'Parameter remote controller', vol, chp, frag=frag, postfix=postfix)
	if 'maou no hajimekata' in item['tags'] :
		return buildReleaseMessage(item, 'Maou no Hajimekata', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractHoldXandClick(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Bishoujo wo Jouzu ni Nikubenki ni Suru Houhou' in item['tags'] :
		return buildReleaseMessage(item, 'Bishoujo wo Jouzu ni Nikubenki ni Suru Houhou', vol, chp, frag=frag, postfix=postfix)

	print(item['title'])
	print(item['tags'])
	print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractKoreYoriHachidori(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Seiun wo kakeru'.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'Seiun wo Kakeru', vol, chp, frag=frag, postfix=postfix)
	if 'Ochitekita Naga'.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'Ochitekita Naga to Majo no Kuni', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractTsukigomori(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag):
		return False

	if 'Our Glamorous Time' in item['tags']:
		return buildReleaseMessage(item, 'Our Glamorous Time', vol, chp, frag=frag, postfix=postfix)
	if 'Same Place Not Same Bed' in item['tags']:
		return buildReleaseMessage(item, 'Same Place Not Same Bed', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractIsekaiTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Tsuki ga Michibiku Isekai Douchuu' in item['tags']:
		return buildReleaseMessage(item, 'Tsuki ga Michibiku Isekai Douchuu', vol, chp, frag=frag, postfix=postfix)
	if 'Double Edge Hero' in item['tags']:
		return buildReleaseMessage(item, 'Double Edge Hero', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractAndrew9495(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if "Skill Taker's World Domination Building a slave harem from scratch" in item['tags']:
		return buildReleaseMessage(item, 'Skill Taker’s World Domination ~ Building a Slave Harem from Scratch', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractAtenTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Skill Taker' in item['tags'] or 'Skill Taker Ch' in item['title']:
		return buildReleaseMessage(item, 'Skill Taker’s World Domination ~ Building a Slave Harem from Scratch', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractMakinaTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if "I aim to be an adventurer with the jobclass of 'Jobless'" in item['tags']:
		return buildReleaseMessage(item, 'I Aim to Be an Adventurer with the Jobclass of "Jobless"', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractHaruPARTY(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Yuusha Party' in item['tags']:
		return buildReleaseMessage(item, 'Yuusha Party no Kawaii Ko ga Ita no de, Kokuhaku Shite', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractNekoyashiki(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'rakudai kishi no eiyuutan' in item['tags']:
		return buildReleaseMessage(item, 'Rakudai Kishi no Eiyuutan', vol, chp, frag=frag, postfix=postfix)
	if 'Ore no Pet was Seijo-sama' in item['tags']:
		return buildReleaseMessage(item, 'Ore no Pet was Seijo-sama', vol, chp, frag=frag, postfix=postfix)

	print(item['title'])
	print(item['tags'])
	print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractKonobuta(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Ryouriban' in item['title']:
		return buildReleaseMessage(item, 'The Cook of the Mercenary Corp', vol, chp, frag=frag, postfix=postfix)
	if 'UchiMusume' in item['title']:
		return buildReleaseMessage(item, 'For my daughter, I might even be able to defeat the demon king', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractCrystalRainDescends(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Honey Stewed Squid' in item['tags']:
		return buildReleaseMessage(item, 'Honey Stewed Squid', vol, chp, frag=frag, postfix=postfix)
	if 'Bloom' in item['tags']:
		return buildReleaseMessage(item, 'Bloom', vol, chp, frag=frag, postfix=postfix)
	return False

def extractLasciviousImouto(item):
	# Convert "-" to "." so partial chapters like 'Chapter 02-31' convert to 02.31, and the
	# fragment works correctly.
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'].replace("-", "."))
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if ('The Beast of the 17th District' in item['tags'] or "the beast of the 17th district" in item['title'].lower()):
		return buildReleaseMessage(item, 'The Beast of the 17th District', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Le Festin de Vampire' in item['tags']:
		return buildReleaseMessage(item, 'Le Festin de Vampire', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWitchLife(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Witch Life' in item['tags']:
		return buildReleaseMessage(item, 'Witch Life', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractFirebirdsNest(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'no-fatigue' in item['tags']:
		return buildReleaseMessage(item, 'No Fatigue', vol, chp, frag=frag, postfix=postfix)
	if 'mondaiji' in item['tags']:
		return buildReleaseMessage(item, 'Mondaiji-tachi ga Isekai Kara Kuru Sou Desu yo?', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractNanjamora(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Endless Dantian' in item['tags']:
		return buildReleaseMessage(item, 'Endless Dantian', vol, chp, frag=frag, postfix=postfix)
	if 'Infinite Temptation' in item['tags']:
		return buildReleaseMessage(item, 'Infinite Temptation', vol, chp, frag=frag, postfix=postfix)
	if 'wushang jinshia' in item['tags']:
		return buildReleaseMessage(item, 'Wu Shang Jin Shia', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractSutekiDaNe(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Can I Not Marry?' in item['tags']:
		return buildReleaseMessage(item, 'Can I Not Marry? / Days of Cohabitation with the President', vol, chp, frag=frag, postfix=postfix)
	if "Black Bellied Prince's Stunning Abandoned Consort" in item['tags']:
		return buildReleaseMessage(item, "Black Bellied Prince's Stunning Abandoned Consort", vol, chp, frag=frag, postfix=postfix)

	print(item['title'])
	print(item['tags'])
	print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractNooblate(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	# Siiiiiigh. Plz spellcheck at least your title.
	if     'Kujibiki Tokushou : Musou Harem Ken' in item['title'] \
		or 'Kujibiku Tokushou : Musou Harem Ken' in item['title'] \
		or 'Kujibiki Tokushou: Musou Hāremu ken' in item['title'] \
		or 'Kujibiki Tokushou: Musou Harem Ken' in item['title'] \
		or 'Kujibiji Tokushou : Musou Harem Ken' in item['title']:
		return buildReleaseMessage(item, "Kujibiki Tokushou : Musou Harem Ken", vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractSilentTl(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Legend' in item['tags']:
		return buildReleaseMessage(item, "Legend", vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractCasProjectSite(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	return buildReleaseMessage(item, "Era of Cultivation", vol, chp, frag=frag, postfix=postfix)

####################################################################################################################################################
#
####################################################################################################################################################
def extractFrostfire10(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	return buildReleaseMessage(item, "Overlord", vol, chp, frag=frag, postfix=postfix)

####################################################################################################################################################
#
####################################################################################################################################################
def extractWalkingTheStorm(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	return buildReleaseMessage(item, "Joy of life", vol, chp, frag=frag, postfix=postfix)

####################################################################################################################################################
#
####################################################################################################################################################
def extractTranslatingZeTianJi(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	return buildReleaseMessage(item, "Ze Tian Ji ", vol, chp, frag=frag, postfix=postfix)

####################################################################################################################################################
#
####################################################################################################################################################
def extractWebNovelJapaneseTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Kizoku Yamemasu Shomin ni Narimasu' in item['tags']:
		return buildReleaseMessage(item, 'Kizoku Yamemasu Shomin ni Narimasu', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractMadaoTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'My Death Flags Show No Sign of Ending' in item['tags']:
		# These chapters are numbered "part n episode m"
		# Therefore, swap m,n
		chp, frag = frag, chp
		return buildReleaseMessage(item, 'Ore no Shibou Flag ga Todomaru Tokoro wo Shiranai', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractMonkTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Battle Emperor' in item['tags']:
		return buildReleaseMessage(item, 'Battle Emperor', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractSoojikisProject(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Weakest Skeleton' in item['tags'] or 'Home page' in item['tags']:
		return buildReleaseMessage(item, 'Kurasu marugoto jingai tensei -Saijyaku no sukeruton ni natta ore-', vol, chp, frag=frag, postfix=postfix)
	if 'Reincarnated as a Villager' in item['tags']:
		return buildReleaseMessage(item, 'Reincarnated as a Villager ~ Strongest Slow-life', vol, chp, frag=frag, postfix=postfix)
	if 'Yandere?' in item['tags'] and 'Weapons' in item['tags']:
		return buildReleaseMessage(item, 'Myself, weapons, and Yandere', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractMorrighanSucks(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Unlimited Anime Works' in item['title']:
		return buildReleaseMessage(item, 'Unlimited Anime Works', vol, chp, frag=frag, postfix=postfix)

	return False
####################################################################################################################################################
#
####################################################################################################################################################
def extractLunaris(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'World of Hidden Phoenix' in item['tags']:
		return buildReleaseMessage(item, 'World of Hidden Phoenix', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# General feedproxy stuff
# This is the sourcename for a whole pile of junk that goes
# through google somehow.
####################################################################################################################################################
def extractFeedProxy(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'The Man Picked up by the Gods' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Kamitachi ni Hirowareta Otoko', vol, chp, frag=frag, postfix=postfix)
	if 'The Man Picked up by the Gods -' in item['title'] and (chp or vol):
		return buildReleaseMessage(item, 'Kamitachi ni Hirowareta Otoko', vol, chp, frag=frag, postfix=postfix)

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

	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if not postfix and ":" in item['title']:
		postfix = item['title'].split(":")[-1]

	if 'Magic Academy' in item['tags']:
		return buildReleaseMessage(item, 'I was reincarnated as a Magic Academy!', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if "100 Luck" in item['tags']:
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

	if ('Hardcore OPness' in item['tags'] or 'HCOP' in item['tags']) and (chp or vol):
		return buildReleaseMessage(item, 'Hardcore OP-ness', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
# Broken!
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
def extractRequireCookie(item):
	# No structured data. Arrrgh
	return None

def extractBase(item):
	# vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	# if 'meg and seron' in item['tags'] and (chp or vol):
	# 	return buildReleaseMessage(item, 'Meg and Seron', vol, chp, frag=frag, postfix=postfix)

	# print(item['title'])
	# print(item['tags'])
	# print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

	return False

####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
#
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################

####################################################################################################################################################
#
####################################################################################################################################################
def extractZombieKnight(item):
	titleconcat = " ".join(item['tags']) + item['title']
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(titleconcat)
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	return buildReleaseMessage(item, 'The Zombie Knight', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

####################################################################################################################################################
#
####################################################################################################################################################
def extractAquarilasScenario(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'In That Moment of Suffering' in item['tags']:
		return buildReleaseMessage(item, 'In That Moment of Suffering', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractDynamisGaul(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Reincarnated by the God of Creation' in item['tags']:
		return buildReleaseMessage(item, 'Reincarnated by the God of Creation', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Status Meister' in item['tags']:
		return buildReleaseMessage(item, 'Status Meister', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractLegendofGalacticHeroes(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Part 1 - Dawn' in item['tags']:
		if not vol:
			vol = 1
		return buildReleaseMessage(item, 'Legend of Galactic Heroes', vol, chp, frag=frag, postfix=postfix)
	if 'Part 2 - Ambition' in item['tags']:
		if not vol:
			vol = 2
		return buildReleaseMessage(item, 'Legend of Galactic Heroes', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractRedDragonTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Kaettekite mo fantasy' in item['tags']:
		return buildReleaseMessage(item, 'Kaettekite mo Fantasy!?', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractTalesOfPaulTwister(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'The Fate of Paul Twister' in item['tags']:
		assert not vol
		vol = 2
		return buildReleaseMessage(item, 'The Tales of Paul Twister', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'The Return of Paul Twister' in item['tags']:
		assert not vol
		vol = 3
		return buildReleaseMessage(item, 'The Tales of Paul Twister', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractDeweyNightUnrolls(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Chaos Of Beauty' in item['tags']:
		return buildReleaseMessage(item, 'Chaos Of Beauty', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractPlainlyBored(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Empress with no Virtue'.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'Empress with no Virtue', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractSinsOfTheFathers(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	return buildReleaseMessage(item, 'Sins of the Fathers '.lower(), vol, chp, frag=frag, postfix=postfix, tl_type='oel')

####################################################################################################################################################
#
####################################################################################################################################################
def extractTheMustangTranslator(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'The Six Immortals' in item['tags']:
		return buildReleaseMessage(item, 'The Six Immortals', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractJoeglensTranslationSpace(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False


	if 'Parallel World Pharmacy' in item['tags']:
		chapter = re.search(r'(?:chapter|chap)\W*(\d+)', item['title'], flags=re.IGNORECASE)
		episode = re.search(r'(?:episode|ep)\W*(\d+)', item['title'], flags=re.IGNORECASE)
		if chapter and episode:
			chp = chapter.group(0)
			frag = episode.group(0)
			return buildReleaseMessage(item, 'Parallel World Pharmacy', vol, chp, frag=frag, postfix=postfix)
	if 'Slave Career Planner' in item['tags']:
		return buildReleaseMessage(item, 'The Successful Business of a Slave Career Planner', vol, chp, frag=frag, postfix=postfix)
	if 'Rokudenashi' in item['tags']:
		return buildReleaseMessage(item, 'Akashic Record of a Bastard Magic Instructor', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractLylisTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'The Unicorn Legion:' in item['title']:
		postfix = item['title'].split(":", 1)[-1]
		return buildReleaseMessage(item, 'The Unicorn Legion', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractCrazyForHENovels(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) and not "preview" in item['title']:
		return False

	chp = frag
	frag = None
	if '如果蜗牛有爱情 When A Snail Loves – 丁墨 Ding Mo (HE)(Incomplete)' in item['tags'] or 'When a snail loves' in item['tags']:
		return buildReleaseMessage(item, 'When A Snail Loves', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractPippiSite(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'FMTL – Chapter' in item['title']:
		return buildReleaseMessage(item, 'First Marriage Then Love', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractHelidwarf(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Alderamin on the Sky' in item['tags']:
		if not vol:
			vol = 2
		return buildReleaseMessage(item, 'Alderamin on the Sky', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractBathrobeKnight(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if not postfix and '-' in item['title']:
		postfix = item['title'].split("-")[-1]
	return buildReleaseMessage(item, 'The Bathrobe Knight', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWalkTheJiangHu(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'TTNH Chapter' in item['title']:
		return buildReleaseMessage(item, "Transcending the Nine Heavens", vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractUniversesWithMeaning(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Angel of Death' in item['title']:
		return buildReleaseMessage(item, 'Angel of Death', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'In The Name Of God' in item['title']:
		return buildReleaseMessage(item, 'In The Name Of God', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractFungShen(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Shrouded' in item['tags']:
		return buildReleaseMessage(item, 'Shrouded', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractGrowWithMe(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'zui wu dao' in item['tags']:
		# These parts are either volumes or chapters
		vol, chp, frag = frag, chp, 0
		return buildReleaseMessage(item, 'Zui Wu Dao', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractVolareTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Great Demon King' in item['tags']:
		return buildReleaseMessage(item, 'Great Demon King', vol, chp, frag=frag, postfix=postfix)
	if 'Sovereign of the Three Realms' in item['tags']:
		return buildReleaseMessage(item, 'Sovereign of the Three Realms', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractTaint(item):
	titletmp = item['title'] + " ".join(item['tags'])
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(titletmp)
	if not (chp or vol or frag) and not "preview" in item['title']:
		return False

	if 'Chapter Release' in item['tags'] and 'Taint' in item['tags'] and 'Main Story' in item['tags']:
		return buildReleaseMessage(item, 'Taint', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Chapter Release' in item['tags'] and 'Taint' in item['tags'] and 'Side Story' in item['tags']:
		postfix = "Side Story"
		return buildReleaseMessage(item, 'Taint', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractKumaOtou(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "I Kinda Came to Another World but where's the way home" in item['tags'] and 'translation' in item['tags']:
		return buildReleaseMessage(item, 'Isekai Kichattakedo Kaerimichi doko?', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractPriddlesTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Magic is Japanese' in item['tags']:
		return buildReleaseMessage(item, 'Magic is Japanese', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractNovelSaga(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Dragon Martial Emperor' in item['tags']:
		return buildReleaseMessage(item, 'Dragon Martial Emperor', vol, chp, frag=frag, postfix=postfix)
	if 'The Six Immortals' in item['tags']:
		return buildReleaseMessage(item, 'The Six Immortals', vol, chp, frag=frag, postfix=postfix)
	if 'Genius Sword Immortal' in item['tags']:
		return buildReleaseMessage(item, 'Genius Sword Immortal', vol, chp, frag=frag, postfix=postfix)
	if 'Martial God Space' in item['tags']:
		return buildReleaseMessage(item, 'Martial God Space', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractDarkTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if item['title'].lower().startswith("kuang shen"):
		return buildReleaseMessage(item, 'Kuang Shen', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith("sheng wang chapter"):
		return buildReleaseMessage(item, 'Sheng Wang', vol, chp, frag=frag, postfix=postfix)
	if "lord xue ying chapter" in item['title'].lower():
		return buildReleaseMessage(item, 'Lord Xue Ying', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWatermelonHelmets(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Dragon Life' in item['tags'] or 'Dragon Life: Chapter' in item['title']:
		return buildReleaseMessage(item, 'Dragon Life', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractRumanshisLair(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Isekai Cheat' in item['tags'] or 'Isekai Cheat' in item['title']:
		return buildReleaseMessage(item, 'Different World Reincarnation ~ Enjoying the new world as a cheat ~', vol, chp, frag=frag, postfix=postfix)
	if 'Other Worlds Monster Breeder' in item['tags'] or 'Other World’s Monster Breeder (PokeGod)'.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'Other World\'s Monster Breeder', vol, chp, frag=frag, postfix=postfix)
	if 'When I returned home, what I found was fantasy!?'.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'Kaettekite mo Fantasy!?', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractLuenTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Journey to Seek Past Reincarnations' in item['tags'] or item['title'].startswith('JTSPR'):
		return buildReleaseMessage(item, 'Journey to Seek Past Reincarnations', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractHeroicNovels(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Dragon Order of Flame' in item['tags']:
		return buildReleaseMessage(item, 'Dragon Order of Flame', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('The Hero Volume'):
		return buildReleaseMessage(item, 'The Hero', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Metatron Volume'):
		return buildReleaseMessage(item, 'Metatron', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractNotDailyTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Zombie Emperor' in item['tags']:
		return buildReleaseMessage(item, 'The Bloodshot One-Eyed Zombie Emperor', vol, chp, frag=frag, postfix=postfix)
	if 'Nidome no Yuusha' in item['tags']:
		return buildReleaseMessage(item, 'Nidome no Yuusha wa Fukushuu no Michi wo Warai Ayumu. ~Maou yo, Sekai no Hanbun wo Yaru Kara Ore to Fukushuu wo Shiyou~', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractEpyonTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'magic robot aluminare ch' in item['title'].lower():

		match = re.search(r'ch ?(\d+)\-(\d+)', item['title'])
		if match:
			chp  = match.group(1)
			frag = match.group(2)
			return buildReleaseMessage(item, 'Magic Robot Aluminare', vol, chp, frag=frag, postfix=postfix)
		return buildReleaseMessage(item, 'Magic Robot Aluminare', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWhiteTigerTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if item['title'].lower().startswith('mp volume'):
		return buildReleaseMessage(item, 'Martial Peak', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('ipash chapter'):
		return buildReleaseMessage(item, 'Martial Peak', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractRosyfantasy(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Chu Wang Fei' in item['tags']:
		return buildReleaseMessage(item, 'Chu Wang Fei', vol, chp, frag=frag, postfix=postfix)
	if 'Seven Unfortunate Lifetimes' in item['tags']:
		return buildReleaseMessage(item, 'Seven Unfortunate Lifetimes', vol, chp, frag=frag, postfix=postfix)
	if 'All Thanks to a Single Moment of Impulse' in item['tags']:
		return buildReleaseMessage(item, 'All Thanks to a Single Moment of Impulse', vol, chp, frag=frag, postfix=postfix)
	if 'White Calculation' in item['tags']:
		return buildReleaseMessage(item, 'White Calculation', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractKnokkroTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Eternal Life' in item['tags']:
		return buildReleaseMessage(item, 'Eternal Life', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractLilBlissNovels(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if ':' in item['title'] and 'Side Story' in item['title'] and not postfix:
		postfix = item['title'].split(":")[-1]
	if 'Wei Wei Yi Xiao Hen Qing Cheng' in item['tags']:
		return buildReleaseMessage(item, 'Wei Wei Yi Xiao Hen Qing Cheng', vol, chp, frag=frag, postfix=postfix)
	if 'Memory Lost' in item['tags']:
		return buildReleaseMessage(item, 'Memory Lost', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractLinkedTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if item['title'].startswith('A Record of a Mortal’s Journey to Immortality:'):
		if not postfix and ":" in item['title']:
			postfix = item['title'].split(":")[-1]
		return buildReleaseMessage(item, 'A Record of a Mortal’s Journey to Immortality', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWeleTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if item['title'].startswith('Sin City'):
		return buildReleaseMessage(item, 'Sin City', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('zhan xian'):
		return buildReleaseMessage(item, 'Zhan Xian', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractUDonateWeTranslate(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'ATG' in item['tags'] or ('Against the Gods' in item['title'] and 'Chapter' in item['title']):
		return buildReleaseMessage(item, 'Against the Gods', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractPaztok(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title']:
		return False

	if not postfix and ":" in item['title']:
		postfix = item['title'].split(":")[-1]

	if 'Paztok' in item['tags']:
		return buildReleaseMessage(item, 'Paztok', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractDramasBooksTea(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if "I Don't Like This World I Only Like You" in item['tags']:
		return buildReleaseMessage(item, "I Don't Like This World I Only Like You", vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractMiaomix539(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	titleclean = item['title'].lower().replace("“", "").replace("”", "")
	if not (chp or vol) or "preview" in titleclean:
		return False

	if "death march" in titleclean:
		extract = re.search(r'Death March ((\d+)\-(.+?).*)', titleclean, flags=re.IGNORECASE)
		if extract:
			try:
				postfix = extract.group(1)
				vol = int(extract.group(2))
				chp = int(extract.group(3))
				return buildReleaseMessage(item, 'Death March kara Hajimaru Isekai Kyusoukyoku (LN)', vol, chp, postfix=postfix)
			except ValueError:
				return False

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWIP(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	print(item['title'])
	print(item['tags'])
	print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

	return False






####################################################################################################################################################
#
####################################################################################################################################################
def extractPandafuqTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	# Fragments are written "Name {chapter} ({frag})". Arrrgh.

	return False


####################################################################################################################################################
#
####################################################################################################################################################
def extractCrackofDawnTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	print(item['title'])
	print(item['tags'])
	print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

	return False


####################################################################################################################################################
#
####################################################################################################################################################
def extractYoukoAdvent(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	# No chapter numbers in titles. Arrrgh

	return False