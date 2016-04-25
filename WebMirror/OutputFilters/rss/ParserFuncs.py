
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
	if 'Desumachi' in item['tags'] or 'Death March kara Hajimaru Isekai Kyousoukyoku' in item['title']:

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

		return buildReleaseMessage(item, 'Evil God Average', vol, chp, frag=frag, postfix=postfix)


	if 'Haunted' in item['tags']:
		return buildReleaseMessage(item, 'Haunted Duke’s Daughter', vol, chp, postfix=postfix)


	if 'Tilea’s Worries' in item['title']:
		return buildReleaseMessage(item, 'Tilea\'s Worries', vol, chp, postfix=postfix)
	if 'Tilea' in item['tags'] and 'Raid on the Capital' in item['title'] and not vol:
		return buildReleaseMessage(item, 'Tilea\'s Worries', 2, chp, postfix=postfix)
	if 'Tilea' in item['tags'] and 'Turf War' in item['title'] and not vol:
		return buildReleaseMessage(item, 'Tilea\'s Worries', 3, chp, postfix=postfix)


	if 'Kenkyo Kenjitu' in item['tags'] or 'Reika-sama' in item['title']:
		return buildReleaseMessage(item, 'Kenkyo Kenjitu', vol, chp, postfix=postfix)

	if 'The Bathroom Goddess' in item['tags']:
		return buildReleaseMessage(item, 'The Bathroom Goddess', vol, chp, postfix=postfix)
	if 'a wild boss appeared' in item['tags']:
		return buildReleaseMessage(item, 'A Wild Boss Appeared', vol, chp, postfix=postfix)

	if 'I’m Back in the Other World' in item['title']:
		return buildReleaseMessage(item, 'I\'m Back in the Other World', vol, chp)

	if 'Kazuha Axeplant’s Third Adventure:' in item['title']:
		return buildReleaseMessage(item, 'Kazuha Axeplant\'s Third Adventure', vol, chp)

	if "I'm the Final Boss!?" in item['tags']:
		return buildReleaseMessage(item, "I'm the Final Boss!?", vol, chp, tl_type='oel')

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
	if item['title'].startswith("Manowa"):
		return buildReleaseMessage(item, "Manowa Mamono Taosu Nouryoku Ubau Watashi Tsuyokunaru", vol, chp, frag=frag, postfix=postfix)
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
	ltags = [tmp.lower().replace("’", "'") for tmp in item['tags']]

	if 'announcement' in ltags:
		return False

	if 'The King’s Avatar Chapter ' in item['title'] or \
		item['title'].startswith("The King’s Avatar (QZGS)") or \
		item['title'].startswith("TKA Chapter "):
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
	if 'conquest' in ltags or 'Conquest Chapter' in item['title']:
		return buildReleaseMessage(item, 'Conquest', vol, chp, frag=frag, postfix=postfix)
	if 'shadow rogue' in ltags:
		return buildReleaseMessage(item, 'Shadow Rogue', vol, chp, frag=frag, postfix=postfix)
	if 'the divine elements' in ltags:
		return buildReleaseMessage(item, 'The Divine Elements', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'cult of the sacred runes' in ltags:
		return buildReleaseMessage(item, 'Cult of the Sacred Runes', vol, chp, frag=frag, postfix=postfix)
	if 'Blood Hourglass' in item['title']:
		return buildReleaseMessage(item, 'Blood Hourglass', vol, chp, frag=frag, postfix=postfix)
	if "A Dragon's Curiosity" in item['tags']:
		return buildReleaseMessage(item, "A Dragon's Curiosity", vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'RMJI' in item['tags']:
		return buildReleaseMessage(item, "A Record of A Mortal's Journey to Immortality", vol, chp, frag=frag, postfix=postfix)
	if 'The Nine Cauldrons' in item['tags']:
		return buildReleaseMessage(item, 'The Nine Cauldrons', vol, chp, frag=frag, postfix=postfix)
	if 'The Trembling World' in item['tags']:
		return buildReleaseMessage(item, 'The Trembling World', vol, chp, frag=frag, postfix=postfix)
	if 'Ancient Strengthening Technique' in item['tags']:
		return buildReleaseMessage(item, 'Ancient Strengthening Technique', vol, chp, frag=frag, postfix=postfix)
	if 'a record of a mortal\'s journey to immortality' in ltags:
		return buildReleaseMessage(item, 'A Record of a Mortal\'s Journey to Immortality', vol, chp, frag=frag, postfix=postfix)
	if 'martial world' in ltags:
		return buildReleaseMessage(item, 'Martial World', vol, chp, frag=frag, postfix=postfix)
	if "The Beginning After the End" in item['tags']:
		return buildReleaseMessage(item, "The Beginning After the End", vol, chp, frag=frag, postfix=postfix, tl_type='oel')

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
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False

	if 'Douluo Dalu' in item['tags']:
		# Volume name is only in the tags.
		proc_str = "%s %s" % (item['tags'], item['title'])
		proc_str = proc_str.replace("'", " ")
		chp, vol = extractChapterVol(proc_str)

		if not (chp and vol):
			return False
		return buildReleaseMessage(item, 'Douluo Dalu', vol, chp)

	if 'Immortal Executioner' in item['tags']:
		return buildReleaseMessage(item, 'Immortal Executioner', vol, chp, frag=frag, postfix=postfix)
	if 'Stellar War Storm' in item['tags']:
		return buildReleaseMessage(item, 'Stellar War Storm', vol, chp, frag=frag, postfix=postfix)
	if 'Bringing The Farm To Live In Another World' in item['tags']:
		return buildReleaseMessage(item, 'Bringing The Farm To Live In Another World', vol, chp, frag=frag, postfix=postfix)

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
		return buildReleaseMessage(item, "Shadow Rogue", vol, chp, frag=frag, postfix=postfix)
	if '[Chinese] Unique Legend' in item['tags'] or 'Unique Legend' in item['tags']:
		return buildReleaseMessage(item, "Unique Legend", vol, chp, frag=frag, postfix=postfix)
	if '[Japanese] Magi\'s Grandson' in item['tags'] or "[JP] Magi's Grandson" in item['tags']:
		return buildReleaseMessage(item, "Magi's Grandson", vol, chp, frag=frag, postfix=postfix)
	if '[Japanese / Hosted] Arifureta' in item['tags']:
		return buildReleaseMessage(item, "Arifureta", vol, chp, frag=frag, postfix=postfix)
	if '[Korean] 21st Century Archmage' in item['tags']:
		return buildReleaseMessage(item, "21st Century Archmage", vol, chp, frag=frag, postfix=postfix)
	if '[Chinese] Kill No More' in item['tags']:
		return buildReleaseMessage(item, "Kill No More", vol, chp, frag=frag, postfix=postfix)
	if "[JP] Duke's Daughter" in item['tags']:
		return buildReleaseMessage(item, "Good Sense of a Duke's Daughter", vol, chp, frag=frag, postfix=postfix)

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
	if 'Upgrade Specialist in Another World' in item['tags']:
		return buildReleaseMessage(item, 'Upgrade Specialist in Another World', vol, chp, frag=frag)
	if 'Renegade Immortal' in item['tags']:
		return buildReleaseMessage(item, 'Renegade Immortal', vol, chp, frag=frag)
	if 'Sovereign of the Three Realms' in item['tags']:
		return buildReleaseMessage(item, 'Sovereign of the Three Realms', vol, chp, frag=frag)

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	match = re.search(r'^Xian Ni Chapter \d+ ?[\-–]? ?(.*)$', item['title'])
	if match:
		return buildReleaseMessage(item, 'Xian Ni', vol, chp, postfix=match.group(1))

	return False

####################################################################################################################################################
# Calico x Tabby
####################################################################################################################################################
def extractCalicoxTabby(item):
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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

	if item['title'].startswith('A Tale of Two Shadows'):
		return buildReleaseMessage(item, 'A Tale of Two Shadows', vol, chp, frag=frag)
	if item['title'].startswith('Gate of Twilight'):
		return buildReleaseMessage(item, 'Gate of Twilight', vol, chp, frag=frag)

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

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
	if 'Elqueeness' in item['title']:
		return buildReleaseMessage(item, 'Spirit King Elqueeness', vol, chp, frag=frag)
	if '[Dark Mage]' in item['title'] or '[DarkMage]' in item['title']:
		return buildReleaseMessage(item, 'Dark Mage', vol, chp, frag=frag)
	if 'Dragon Maken War' in item['title']:
		return buildReleaseMessage(item, 'Dragon Maken War', vol, chp, frag=frag)

	return False

####################################################################################################################################################
# MadoSpicy TL
####################################################################################################################################################
def extractMadoSpicy(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Majin Tenseiki' in item['title']:
		return buildReleaseMessage(item, 'Majin Tenseiki', vol, chp, frag=frag)

	return False

####################################################################################################################################################
# DarkFish Translations
####################################################################################################################################################
def extractDarkFish(item):
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'She Professed Herself The Pupil Of The Wise Man'.lower() in item['title'].lower() or \
		'She Professed Herself The Pupil Of The Wise Man'.lower() in [tmp.lower() for tmp in item['tags']]:
		return buildReleaseMessage(item, 'Kenja no Deshi wo Nanoru Kenja', vol, chp, frag=frag)
	# if 'Majin Tenseiki' in item['title']:
	return False

def extractSaiakuTranslationsBlog(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False

	if item['title'].startswith('She Professed Herself The Pupil Of The Wiseman'):
		return buildReleaseMessage(item, 'Kenja no Deshi wo Nanoru Kenja', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# Manga0205 Translations
####################################################################################################################################################
def extractManga0205Translations(item):
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
	if 'Katte Kita Motoyuusha' in item['tags']:
		return buildReleaseMessage(item, 'Katte Kita Motoyuusha', vol, chp, frag=frag)
	if 'Riot Grasper' in item['tags']:
		return buildReleaseMessage(item, 'Riot Grasper', vol, chp, frag=frag)

	if 'E? Heibon Desu Yo??' in item['tags']:
		return buildReleaseMessage(item, 'E? Heibon Desu Yo??', vol, chp, frag=frag)

	if 'Right Grasper' in item['tags']:
		return buildReleaseMessage(item, 'Right Grasper ~Stealing Skills in the Other World~', vol, chp, frag=frag)

	if 'I, with house work and cooking, takes away the backbone of the Demon lord! The peerless house-husband starts from kidnapping!' in item['tags']:
		return buildReleaseMessage(item, 'I, with house work and cooking, takes away the backbone of the Demon lord! The peerless house-husband starts from kidnapping!', vol, chp, frag=frag)

	if 'Game nai ni haitte Doragon o hanto' in item['tags']:
		return buildReleaseMessage(item, 'Game nai ni haitte Doragon o hanto', vol, chp, frag=frag)
	if 'Yuusha Ga Onna Da to Dame Desu Ka?' in item['tags']:
		return buildReleaseMessage(item, 'Yuusha Ga Onna Da to Dame Desu Ka?', vol, chp, frag=frag)

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
def extractXCrossJ(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Character Analysis' in item['title']:
		return False

	if 'Cross Gun' in item['tags']:
		return buildReleaseMessage(item, 'Cross Gun', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	if 'Konjiki no Moji Tsukai' in item['title']:
		postfix = item['title'].split(":", 1)[-1].strip()
		return buildReleaseMessage(item, 'Konjiki no Wordmaster', vol, chp, frag=frag, postfix=postfix)
	if 'Shinwa Densetsu no Eiyuu no Isekaitan' in item['tags']:
		return buildReleaseMessage(item, 'Shinwa Densetsu no Eiyuu no Isekaitan', vol, chp, frag=frag, postfix=postfix)
	if 'Isekai Mahou wa Okureteru' in item['tags']:
		return buildReleaseMessage(item, 'Isekai Mahou wa Okureteru', vol, chp, frag=frag, postfix=postfix)
	if  'Nidome no Jinsei wo Isekai de' in item['tags']:
		return buildReleaseMessage(item,  'Nidome no Jinsei wo Isekai de', vol, chp, frag=frag, postfix=postfix)

	return False

def extractKirikoTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'KnW' in item['tags'] or 'KnW Chapter' in item['title']:
		postfix = item['title'].split(":", 1)[-1].strip()
		return buildReleaseMessage(item, 'Konjiki no Wordmaster', vol, chp, frag=frag, postfix=postfix)

	if 'Shinwa Densetsu' in item['tags']:
		return buildReleaseMessage(item, 'Shinwa Densetsu no Eiyuu no Isekaitan', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# Thunder Translations:
####################################################################################################################################################
def extractThunder(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Stellar Transformations' in item['tags'] and (vol or chp):
		return buildReleaseMessage(item, 'Stellar Transformations', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# Kiri Leaves:
####################################################################################################################################################
def extractKiri(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Tensei Oujo' in item['tags'] and (vol or chp):
		return buildReleaseMessage(item, 'Tensei Oujo wa Kyou mo Hata o Tatakioru', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# 中翻英圖書館 Translations
####################################################################################################################################################
def extractTuShuGuan(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'He Jing Kunlun' in item['tags'] and (vol or chp or postfix):
		return buildReleaseMessage(item, 'The Crane Startles Kunlun', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Lingson's Translations
####################################################################################################################################################
def extractLingson(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Legendary Moonlight Sculptor' in item['tags'] and any(['Volume' in tag for tag in item['tags']]):
		return buildReleaseMessage(item, 'Legendary Moonlight Sculptor', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Defiring
####################################################################################################################################################
def extractDefiring(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Ryuugoroshi no Sugosuhibi' in item['title'] or 'Ryuugoroshi no Sugosu Hibi' in item['tags']:
		return buildReleaseMessage(item, 'Ryugoroshi no Sugosuhibi', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Imoutolicious
####################################################################################################################################################
def extractImoutolicious(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Isekai Mahou Chapter' in item['title'] and 'Release' in item['title']:
		return buildReleaseMessage(item, 'Isekai Mahou wa Okureteru!', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Kerambit's Incisions
####################################################################################################################################################
def extractKerambit(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
		return buildReleaseMessage(item, 'Maou the Yuusha', vol, chp, frag=frag, postfix=postfix, tl_type="oel")
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
			postfix = item['title'].split(":", 1)[-1].strip()
		return buildReleaseMessage(item, "History's Number One Founder", vol, chp, frag=frag, postfix=postfix)
	if 'The Gate of Extinction' in item['tags']:
		if ":" in item['title']:
			postfix = item['title'].split(":", 1)[-1].strip()
		return buildReleaseMessage(item, "The Gate of Extinction", vol, chp, frag=frag, postfix=postfix)
	if "Shura's Wrath" in item['tags'] or "Shura\"s Wrath" in item['tags']:
		if ":" in item['title']:
			postfix = item['title'].split(":", 1)[-1].strip()
		return buildReleaseMessage(item, 'Shura\'s Wrath', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# Tomorolls
####################################################################################################################################################
def extractTomorolls(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Stellar Transformation' in item['tags']:
		return buildReleaseMessage(item, 'Stellar Transformations', vol, chp, frag=frag, postfix=postfix)
	if 'The Legendary Thief' in item['tags']:
		return buildReleaseMessage(item, 'Virtual World - The Legendary Thief', vol, chp, frag=frag, postfix=postfix)
	if 'SwallowedStar' in item['tags']:
		return buildReleaseMessage(item, 'Swallowed Star', vol, chp, frag=frag, postfix=postfix)
	if 'God and Devil World' in item['tags']:
		return buildReleaseMessage(item, 'God and Devil World', vol, chp, frag=frag, postfix=postfix)
	if 'Limitless Sword God' in item['tags']:
		return buildReleaseMessage(item, 'Limitless Sword God', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# Ln Addiction
####################################################################################################################################################
def extractLnAddiction(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if ('Hissou Dungeon Unei Houhou' in item['tags'] or 'Hisshou Dungeon Unei Houhou' in item['tags']) and (chp or frag):
		return buildReleaseMessage(item, 'Hisshou Dungeon Unei Houhou', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# Binggo & Corp Translations
####################################################################################################################################################
def extractBinggoCorp(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
	if 'Jikuu Mahou TL' in item['tags']:
		return buildReleaseMessage(item, 'Jikuu Mahou de Isekai to Chikyuu wo Ittarikitari', vol, chp, frag=frag, postfix=postfix)
	if 'Monster Musume' in item['tags']:
		return buildReleaseMessage(item, 'Monster Musume Harem o Tsukurou!', vol, chp, frag=frag, postfix=postfix)
	if 'Monster Musume' in item['tags']:
		return buildReleaseMessage(item, 'Parameter Remote Controller', vol, chp, frag=frag, postfix=postfix)
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
	if 'Isekai Ryouridou'.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'Isekai Ryouridou', vol, chp, frag=frag, postfix=postfix)
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
	if "Sefiria chap".lower() in item['title'].lower() \
		or "Sefi chap".lower() in item['title'].lower() :
		return buildReleaseMessage(item, 'Sefiria', vol, chp, frag=frag, postfix=postfix)
	if 'Master of Dungeon'.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'TMaster of Dungeon', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'TRTS(The Rude Time Stopper)'.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'The Rude Time Stopper', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Polymath Redux '.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'Polymath Redux', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'The Falcon Immortal'.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'The Falcon Immortal', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'The Last Guild'.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'The Last Guild: Remastered', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if '[Second Saga] Chapter'.lower() in item['title'].lower():
		return buildReleaseMessage(item, '[Second Saga]', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Inma no Hado chapter'.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'Inma no Hado', vol, chp, frag=frag, postfix=postfix)
	if 'Tensei Shoujo no Rirekisho'.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'Tensei Shoujo no Rirekisho', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Ark Machine Translations
####################################################################################################################################################
def extractArkMachineTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'NEET dakedo Hello Work ni Ittara Isekai ni Tsuretekareta' in item['tags']:
		return buildReleaseMessage(item, 'NEET dakedo Hello Work ni Ittara Isekai ni Tsuretekareta', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# Hokage Translations
####################################################################################################################################################
def extractHokageTrans(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'The Man Picked up by the Gods'.lower() in item['title'].lower() and (chp or vol):
		return buildReleaseMessage(item, 'The Man Picked up by the Gods', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Ruze Translations
####################################################################################################################################################
def extractRuzeTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Guang Zhi Zi' in item['title'] and (chp or vol):
		return buildReleaseMessage(item, 'Guang Zhi Zi', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Wuxia Translations
####################################################################################################################################################
def extractWuxiaTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Route to almightyness from 1HP' in item['title'] and (chp or vol):
		return buildReleaseMessage(item, 'HP1 kara Hajimeru Isekai Musou', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Tsuigeki Translations
####################################################################################################################################################
def extractTsuigeki(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Seiju no Kuni no Kinju Tsukai' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Seiju no Kuni no Kinju Tsukai', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Eros Workshop
####################################################################################################################################################
def extractErosWorkshop(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Young God Divine Armaments' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Young God Divine Armaments', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Forgetful Dreamer
####################################################################################################################################################
def extractForgetfulDreamer(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'ヤンデレ系乙女ゲーの世界に転生してしまったようです' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'It seems like I got reincarnated into the world of a Yandere Otome game', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Fudge Translations
####################################################################################################################################################
def extractFudgeTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'SoE' in item['title'] and (chp or vol):
		return buildReleaseMessage(item, 'The Sword of Emperor', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Henouji Translation
####################################################################################################################################################
def extractHenoujiTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Isekai Maou to Shoukan Shoujo Dorei Majutsu' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Isekai Maou to Shoukan Shoujo no Dorei Majutsu', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Iterations within a Thought-Eclipse
####################################################################################################################################################
def extractIterations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'SaeKano' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Saenai Heroine no Sodatekata', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Kaezar Translations
####################################################################################################################################################
def extractKaezar(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

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
		return buildReleaseMessage(item, 'Jaaku to Shite Akuratsu Naru Chika Teikoku Monogatari', vol, chp, frag=frag, postfix=postfix)
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'The Alchemist God' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Ascension of the Alchemist God', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# World of Watermelons
####################################################################################################################################################
def extractWatermelons(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Tensei Shitara Slime datta ken' in item['tags'] and chp:
		return buildReleaseMessage(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# 'Nohohon Translation'
####################################################################################################################################################
def extractNohohon(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Monster Musume Harem wo Tsukurou!' in item['tags']:
		return buildReleaseMessage(item, 'Monster Musume Harem o Tsukurou!', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# NEET Translations
####################################################################################################################################################
def extractNeetTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Marginal Operation' in item['tags']:
		return buildReleaseMessage(item, 'Marginal Operation', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# Kyakka
####################################################################################################################################################
def extractKyakka(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Juvenile Medical God' in item['tags']:
		return buildReleaseMessage(item, 'Shaonian Yixian', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# 'Alcsel Translations'
####################################################################################################################################################
def extractAlcsel(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

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
	if 'The Strongest Dan God' in item['tags']:
		return buildReleaseMessage(item, 'The Strongest Dan God', vol, chp, frag=frag, postfix=postfix)

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Shiro no Koukoku Monogatari ' in item['title']:
		return buildReleaseMessage(item, 'Shiro no Koukoku Monogatari', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# Ensj Translations
####################################################################################################################################################
def extractEnsjTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'King Shura' in item['tags']:
		return buildReleaseMessage(item, 'King Shura', vol, chp, frag=frag, postfix=postfix)
	if 'The Record of a Thousand Lives' in item['tags']:
		return buildReleaseMessage(item, 'The Record of a Thousand Lives', vol, chp, frag=frag, postfix=postfix)

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

	extractVol = re.search(r'\[[A-Z]+(\d+)\]', item['title'])
	if not vol and extractVol:
		vol = int(extractVol.group(1))


	extractChp = re.search(r'SECT\.(\d+) ', item['title'])
	if chp == 1 and "SECT." in item['title'] and extractChp:
		chp = int(extractChp.group(1))




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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'The Strongest Magical Beast' in item['tags'] and 'Chapter Release' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'The Strongest Magical Beast', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	if 'Apocalypse ЯR' in item['tags'] and 'Chapter Release' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Apocalypse ЯR', vol, chp, frag=frag, postfix=postfix)
	if 'Legend of Xing Feng' in item['tags']:
		return buildReleaseMessage(item, 'Legend of Xingfeng', vol, chp, frag=frag, postfix=postfix)
	if 'The Exceptional Godly Thief-The Good for Nothing Seventh Young Lady' in item['tags']:
		return buildReleaseMessage(item, 'The Good for Nothing Seventh Young Lady', vol, chp, frag=frag, postfix=postfix)

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

	if 'my disciple died yet again' in ltags:
		return buildReleaseMessage(item, 'My Disciple Died Yet Again', vol, chp, frag=frag)
	if 'monogatari no naka no hito' in ltags:
		return buildReleaseMessage(item, 'Monogatari no Naka no Hito', vol, chp, frag=frag, postfix=postfix)
	if 'purple river' in ltags:
		return buildReleaseMessage(item, 'Purple River', vol, chp, frag=frag, postfix=postfix)
	if 'omni-magician' in ltags:
		return buildReleaseMessage(item, 'Omni-Magician', vol, chp, frag=frag, postfix=postfix)
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
	if 'i, am playing the role of the older brother in hearthrob love revolution' in ltags:
		return buildReleaseMessage(item, 'I, am Playing the Role of the Older Brother in Heart-throb Love Revolution.', vol, chp, frag=frag, postfix=postfix)
	if 'botsuraku youtei nanode, kajishokunin wo mezasu' in ltags:
		return buildReleaseMessage(item, 'Botsuraku Youtei Nanode, Kajishokunin wo Mezasu', vol, chp, frag=frag, postfix=postfix)

	if 'isekai maou to shoukan shoujo dorei majutsu' in ltags:
		return buildReleaseMessage(item, 'Isekai Maou to Shoukan Shoujo no Dorei Majutsu', vol, chp, frag=frag, postfix=postfix)
	if 'Wife is Outrageous: His Evil Highness Comes Knocking' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Wife is Outrageous: His Evil Highness Comes Knocking', vol, chp, frag=frag, postfix=postfix)
	if 'I Decided to Not Compete and Quietly Create Dolls Instead' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'I Decided to Not Compete and Quietly Create Dolls Instead', vol, chp, frag=frag, postfix=postfix)
	if 'heavenly star' in ltags:
		return buildReleaseMessage(item, 'Heavenly Star', vol, chp, frag=frag, postfix=postfix)
	if 'otherworld nation founding' in ltags:
		return buildReleaseMessage(item, 'Otherworld Nation Founding Chronicles', vol, chp, frag=frag, postfix=postfix)
	if 'cultivating to become a great celestial' in ltags:
		return buildReleaseMessage(item, 'Cultivating to Become a Great Celestial', vol, chp, frag=frag, postfix=postfix)
	if 'time' in ltags:
		return buildReleaseMessage(item, 'Time', vol, chp, frag=frag, postfix=postfix)

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'The Nine Cauldrons' in item['tags']:
		return buildReleaseMessage(item, 'The Nine Cauldrons', vol, chp, frag=frag, postfix=postfix)
	if 'Conquest' in item['tags']:
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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Heavenly Calamity' in item['tags']:
		return buildReleaseMessage(item, 'Heavenly Calamity', vol, chp, frag=frag, postfix=postfix)
	if 'Magic Chef of Ice and Fire' in item['tags']:
		return buildReleaseMessage(item, 'Magic Chef of Ice and Fire', vol, chp, frag=frag, postfix=postfix)
	if 'The Legend of the Dragon King' in item['tags']:
		return buildReleaseMessage(item, 'The Legend of the Dragon King', vol, chp, frag=frag, postfix=postfix)
	if 'Zither Emperor' in item['tags']:
		return buildReleaseMessage(item, 'Zither Emperor', vol, chp, frag=frag, postfix=postfix)
	if 'Chapter Release' in item['tags']:
		if 'Child of Light' in item['tags'] or 'Guang Zhi Zi' in item['tags']:
			return buildReleaseMessage(item, 'Guang Zhi Zi', vol, chp, frag=frag, postfix=postfix)
		if 'Bing Huo Mo Chu' in item['tags'] or 'Magic Chef of Ice and Fire' in item['tags']:
			return buildReleaseMessage(item, 'Bing Huo Mo Chu', vol, chp, frag=frag, postfix=postfix)
		if 'Lord Xue Ying' in item['tags']:
			return buildReleaseMessage(item, 'Xue Ying Ling Zhu', vol, chp, frag=frag, postfix=postfix)
		if 'The Legend of the Dragon King' in item['tags']:
			return buildReleaseMessage(item, 'Xue Ying Ling Zhu', vol, chp, frag=frag, postfix=postfix)
		if ('dragon marked war god' in item['title'].lower().replace("-", " ") or
				'dmwg' in item['title'].lower() or
				'Dragon Marked War God' in item['tags']):
			return buildReleaseMessage(item, 'Dragon-Marked War God', vol, chp, frag=frag, postfix=postfix)
		if 'beseech the devil' in item['title'].lower():
			return buildReleaseMessage(item, 'Beseech the Devil', vol, chp, frag=frag, postfix=postfix)

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Third Prince Elmer' in item['tags']:
		return buildReleaseMessage(item,  'Third Prince Elmer', vol, chp, frag=frag, postfix=postfix)
	if 'Otoko Aruji' in item['tags']:
		return buildReleaseMessage(item,  'Otoko Aruji', vol, chp, frag=frag, postfix=postfix)
	if "Sword Saint's Disciple" in item['tags']:
		return buildReleaseMessage(item,  "Sword Saint's Disciple", vol, chp, frag=frag, postfix=postfix)
	if 'Doll Dungeon' in item['tags']:
		return buildReleaseMessage(item,  'Doll Dungeon', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractPeasKingdom(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	ltags = [tmp.lower() for tmp in item['tags']]
	if 'second chance' in ltags and (chp or vol):
		return buildReleaseMessage(item, 'Second Chance: a Wonderful New Life', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractCircusTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	ltags = [tmp.lower() for tmp in item['tags']]
	if 'gonna get captured' in ltags or 'Get Captured: Chapter' in item['title']:
		return buildReleaseMessage(item, "Like Hell I’m Gonna Get Captured!", vol, chp, frag=frag, postfix=postfix)

	if 'Girl Who Ate Death' in item['title']:
		return buildReleaseMessage(item, "Shinigami wo Tabeta Shouko", vol, chp, frag=frag, postfix=postfix)

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
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Shoya Kara Hajimeru Ai Aru Seikatsu' in item['tags']:
		return buildReleaseMessage(item, 'Shoya Kara Hajimeru Ai Aru Seikatsu', vol, chp, frag=frag, postfix=postfix)
	if 'Bishoujo wo Jouzu ni Nikubenki ni Suru Houhou' in item['tags']:
		return buildReleaseMessage(item, 'Bishoujo wo Jouzu ni Nikubenki ni Suru Houhou', vol, chp, frag=frag, postfix=postfix)
	if  'Riaru de Reberu Age Shitara Hobo Chītona Jinsei ni Natta' in item['tags']:
		return buildReleaseMessage(item,  'Riaru de Reberu Age Shitara Hobo Chītona Jinsei ni Natta', vol, chp, frag=frag, postfix=postfix)
	if 'Erogacha' in item['tags']:
		return buildReleaseMessage(item, 'Erogacha', vol, chp, frag=frag, postfix=postfix)
	if 'Ore no Sekai no Kouryakubon' in item['tags']:
		return buildReleaseMessage(item, 'Ore no Sekai no Kouryakubon', vol, chp, frag=frag, postfix=postfix)
	if 'Takarakuji de 40 oku Atatta Ndakedo i Sekai ni Ijū Suru' in item['tags']:
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
	if 'Levelmaker –' in item['title']:
		return buildReleaseMessage(item, 'Levelmaker -Raising Levels While Living in Another World-', vol, chp, frag=frag, postfix=postfix)
	if 'Isekai Tensei Harem' in item['title']:
		return buildReleaseMessage(item, 'Isekai Tensei Harem', vol, chp, frag=frag, postfix=postfix)
	if 'Undead Seeks Warmth' in item['title']:
		return buildReleaseMessage(item, 'Undead Seeks Warmth', vol, chp, frag=frag, postfix=postfix)
	if 'Raising Slaves in Another World While on a Journey' in item['title']:
		return buildReleaseMessage(item, 'Raising Slaves in Another World While on a Journey', vol, chp, frag=frag, postfix=postfix)
	if 'Occupation: Adventurer ; Race: Various' in item['title'] or 'Race: Various' in item['tags']:
		return buildReleaseMessage(item, 'Occupation: Adventurer ; Race: Various', vol, chp, frag=frag, postfix=postfix)
	if 'Yuusha ga onna da to dame desu ka?' in item['title']:
		return buildReleaseMessage(item, 'Yuusha ga onna da to dame desu ka?', vol, chp, frag=frag, postfix=postfix)
	if 'The Bears Bear a Bare Kuma' in item['title'] or 'Kuma Kuma Kuma Bear' in item['title']:
		return buildReleaseMessage(item, 'Kuma Kuma Kuma Bear', vol, chp, frag=frag, postfix=postfix)

	if 'Charmed?' in item['title']:
		return buildReleaseMessage(item, 'Charmed?', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
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
	if "Astarte’s Knight" in item['title']:
		return buildReleaseMessage(item, "Astarte's Knight", vol, chp, frag=frag, postfix=postfix)
	if "Queen’s Knight Kael" in item['title']:
		return buildReleaseMessage(item, "Queen's Knight Kael", vol, chp, frag=frag, postfix=postfix)
	if "Legend of Xingfeng" in item['title']:
		return buildReleaseMessage(item, "Legend of Xingfeng", vol, chp, frag=frag, postfix=postfix)

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

	if item['title'].lower().strip().startswith('king shura, chapter'):
		return buildReleaseMessage(item, 'King Shura', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().strip().startswith('devouring the heavens chapter'):
		return buildReleaseMessage(item, 'Devouring the Heavens', vol, chp, frag=frag, postfix=postfix)
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
	if 'Juvenile Medical God' in item['tags']:
		return buildReleaseMessage(item, 'Juvenile Medical God', vol, chp, frag=frag, postfix=postfix)
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
	if 'Ascending the Heavens' in item['tags']:
		return buildReleaseMessage(item, 'Ascending the Heavens', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
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
	if 'Loli Manko TL' in item['tags']:
		return buildReleaseMessage(item, 'Kyonkon na Ore ga Rori ma●ko Bishoujo wo Okashite Kopitte, Ohime-sama wo Torimodosu Isekai Tan', vol, chp, frag=frag, postfix=postfix)
	if 'Cheatman TL' in item['tags']:
		return buildReleaseMessage(item, 'Joudan Mitaina Chiito Nouryouku de Isekai ni Tensei shi, Sukikatte suru Hanashi', vol, chp, frag=frag, postfix=postfix)
	if 'Zombie Emperor TL' in item['tags']:
		return buildReleaseMessage(item, 'The Bloodshot One-Eyed Zombie Emperor', vol, chp, frag=frag, postfix=postfix)
	if 'Asuka TL' in item['tags']:
		return buildReleaseMessage(item, 'Asuka of the Scarlet Sky ~ The Female Hero who Degraded to a Licentious and Wicked Person~', vol, chp, frag=frag, postfix=postfix)
	if 'Flight, Invisibility, and Teleportation TL' in item['tags']:
		return buildReleaseMessage(item, 'If You Got the Power of Flight, Invisibility, and Teleportation, What Would You Do?', vol, chp, frag=frag, postfix=postfix)
	if 'Class TL' in item['tags']:
		return buildReleaseMessage(item, 'Dragged into the class transfer ~For some reason I was dragged into the transfer with the girl class so I will make a harem!~', vol, chp, frag=frag, postfix=postfix)
	if 'Kininaru TL' in item['tags']:
		return buildReleaseMessage(item, 'Kininaru Kanojo wo Tokoton Okashi Tsukusu Hanashi', vol, chp, frag=frag, postfix=postfix)
	if 'Grassland TL' in item['tags']:
		return buildReleaseMessage(item, 'Sougen no Okite ~Shii yatsu ga moteru, ii buzoku ni umarekawatta zo~', vol, chp, frag=frag, postfix=postfix)

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
	if "We live in dragon's peak" in item['tags']:
		return buildReleaseMessage(item, "We live in dragon's peak", vol, chp, frag=frag, postfix=postfix)
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
	if 'Xiao Qi Wait' in item['tags']:
		return buildReleaseMessage(item, 'Xiao Qi Wait', vol, chp, frag=frag, postfix=postfix)
	if 'Beloved Little Treasure' in item['tags']:
		return buildReleaseMessage(item, 'Beloved Little Treasure', vol, chp, frag=frag, postfix=postfix)
	if 'Real Fake Fiance' in item['tags']:
		return buildReleaseMessage(item, 'Real Fake Fiance', vol, chp, frag=frag, postfix=postfix)
	if 'Demoness Go See The Emperor' in item['tags']:
		return buildReleaseMessage(item, 'Demoness Go See The Emperor', vol, chp, frag=frag, postfix=postfix)
	if 'The Reluctant Bride Book I' in item['tags']:
		if not vol:
			vol = 1
		return buildReleaseMessage(item, 'The Reluctant Bride Book I', vol, chp, frag=frag, postfix=postfix)

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
	if 'CC' in item['tags']:
		return buildReleaseMessage(item, 'Cheating Craft', vol, chp, frag=frag, postfix=postfix)

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
	if 'Warlock of the Magus World' in item['tags']:
		return buildReleaseMessage(item, 'Warlock of the Magus World', vol, chp, frag=frag, postfix=postfix)

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

	if 'Coder Lee YongHo' in item['tags'] :
		return buildReleaseMessage(item, 'Coder Lee YongHo', vol, chp, frag=frag, postfix=postfix)
	if'God of Cooking' in item['tags'] :
		return buildReleaseMessage(item, 'God of Cooking', vol, chp, frag=frag, postfix=postfix)
	if 'God of Crime' in item['tags'] :
		return buildReleaseMessage(item, 'God of Crime', vol, chp, frag=frag, postfix=postfix)
	if "The Overlord's Elite is now a Human?!" in item['tags'] :
		return buildReleaseMessage(item, "The Overlord's Elite is now a Human?!", vol, chp, frag=frag, postfix=postfix)
	if 'The Bird That Drinks Tears' in item['tags'] :
		return buildReleaseMessage(item, 'The Bird That Drinks Tears', vol, chp, frag=frag, postfix=postfix)
	if 'Survival World RPG' in item['tags'] :
		return buildReleaseMessage(item, 'Survival World RPG', vol, chp, frag=frag, postfix=postfix)
	if 'Reincarnator' in item['tags'] :
		return buildReleaseMessage(item, 'Reincarnator', vol, chp, frag=frag, postfix=postfix)
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
	if 'Mai Kitsune Waifu Chapter' in item['title'] :
		return buildReleaseMessage(item, 'My Fox Immortal Wife', vol, chp, frag=frag, postfix=postfix)
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
	if 'God of Destruction' in item['tags'] :
		return buildReleaseMessage(item, 'God of Destruction', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'My Path of Justice' in item['tags'] :
		return buildReleaseMessage(item, 'My Path of Justice', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Truth and Myths' in item['tags'] :
		return buildReleaseMessage(item, 'Truth and Myths', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'World of Immortals' in item['tags'] :
		return buildReleaseMessage(item, 'World of Immortals', vol, chp, frag=frag, postfix=postfix)
	if 'Bu ni mi' in item['tags'] :
		return buildReleaseMessage(item, 'Bu ni mi', vol, chp, frag=frag, postfix=postfix)
	if 'Rinkan no Madoushi' in item['tags'] :
		return buildReleaseMessage(item, 'Rinkan no Madoushi', vol, chp, frag=frag, postfix=postfix)
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
	if 'Ochitekita'.lower() in item['title'].lower() or 'Ochitekita Naga to Majo no Kuni' in item['tags']:
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

	if 'Ore no Pet was Seijo-sama' in item['tags'] or 'Ore no Pet wa Seijo-sama' in item['tags']:
		return buildReleaseMessage(item, 'Ore no Pet was Seijo-sama', vol, chp, frag=frag, postfix=postfix)
	if 'M-chan wars' in item['tags']:
		return buildReleaseMessage(item, 'M-chan Wars: Rise and Fall of the Cat Tyrant', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Etranger of the Sky' in item['tags'] or 'Tenkyuu no Etranger' in item['tags']:
		return buildReleaseMessage(item, 'Spear of Thunder – Etranger of the Sky', vol, chp, frag=frag, postfix=postfix)
	if 'Yamato Nadeshiko' in item['tags']:
		return buildReleaseMessage(item, 'Yamato Nadeshiko, Koibana no Gotoku', vol, chp, frag=frag, postfix=postfix)

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
def extractProjectAccelerator(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Black Healer' in item['tags']:
		return buildReleaseMessage(item, 'Black Healer', vol, chp, frag=frag, postfix=postfix)
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
#
####################################################################################################################################################
def extractGrimdarkZTranslations(item):               # 'GrimdarkZ Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False

	if 'Devouring The Heavens' in item['tags']:
		return buildReleaseMessage(item, 'Devouring The Heavens', vol, chp, frag=frag, postfix=postfix)
	if 'Kuro no Hiera Glaphicos' in item['tags']:
		return buildReleaseMessage(item, 'Kuro no Hiera Glaphicos', vol, chp, frag=frag, postfix=postfix)

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


def extractDuckysEnglishTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractBadTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractLordofScrubs(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractRoastedTea(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractUndecentTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuAmagiBrilliantPark(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuFateApocrypha(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuFuyuuGakuennoAliceandShirley(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuGekkanoUtahimetoMaginoOu(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuGJBu(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuHaitoGensounoGrimgal(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuHentaiOujitoWarawanaiNeko(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuKonoSekaigaGameDatoOreDakegaShitteiru(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuKorewaZombieDesuka(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuKurenai(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuLoveYou(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuMaoyuuMaouYuusha(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuMayoChiki(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuOjamajoDoremi(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuOreimo(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuRokkanoYuusha(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuSaenaiHeroinenoSodatekata(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuSasamiSanGanbaranai(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuSeitokainoIchizon(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuSkyWorld(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuYahariOrenoSeishunLoveComewaMachigatteiru(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractSloth(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extract12Superlatives(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extract77Novel(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractGOChronicles(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNakulas(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractAlicetranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractAPearlyView(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractXantbos(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractATranslatorsRamblings(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractATravelersTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractAdamantineDragonintheCrystalWorld(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False

	if 'Crystal World' in item['tags']:
		return buildReleaseMessage(item, 'Adamantine Dragon in the Crystal World', vol, chp, frag=frag, postfix=postfix)
	return False
def extractAllsFairInLoveWar(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractAnonEmpire(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractAoriTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractAquaScans(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractArchivity(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractBearBearTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractBeRsErkTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractCNovels2C(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractCatScans(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractCavescans(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractCheddar(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractChineseWeabooTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractCircleofShards(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractCloudManor(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractCodeZerosBlog(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractCosmicTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractCurrentlyTLingBuniMi(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractDeadlyForgottenLegends(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractDefansTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractDescentSubs(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractDorayakiz(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractDreamAvenue(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractDuranDaruTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractDurasama(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Arifureta' in item['tags']:
		return buildReleaseMessage(item, 'Arifureta', vol, chp, frag=frag, postfix=postfix)
	if 'Manuke FPS' in item['tags']:
		return buildReleaseMessage(item, 'Manuke na FPS Player ga isekai e ochita baai', vol, chp, frag=frag, postfix=postfix)
	return False
def extractELYSIONTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractEmergencyExitsReleaseBlog(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractEndKun(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractEnte38translations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractEternalpath(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractEtheriaTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractEugeneRain(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractEyeofAdventure(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractEZTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractFightingDreamersScanlations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractFlickerHero(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractFuzionLife(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractGargoyleWebSerial(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractHamster428(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractHeartCrusadeScans(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractHelloTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractHellping(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractHendricksensama(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractInfiniteTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractIsolarium(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractIstiansWorkshop(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractItranslateln(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractJagaimo(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractKedelu(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractKisatosMLTs(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractKNTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractKrytyksTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractKurotsukiNovel(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractKyakkaTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractL2M(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractLastvoiceTranslator(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractLayzisheep(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractLightNoveltranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractLizardTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if'The Strongest Violent Soldier' in item['tags']:
		return buildReleaseMessage(item,'The Strongest Violent Soldier', vol, chp, frag=frag, postfix=postfix)
	return False
def extractLMSMachineTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractLorCromwell(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractMaounaAnokotomurabitoa(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractMartialGodTranslator(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractMidnightTranslationBlog(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractMnemeaa(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractMousouhaven(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractMystiqueTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanoDesuLightNovelTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNationalNEET(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNowhereNothing(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractOregaHeroineinEnglish(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractOtomeRevolution(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractPactWebSerial(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractPeaTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractPielordTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractPolyphonicStoryTranslationGroup(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractPopsiclete(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractPumpkinTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractQualityMistranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractRaisingAngelsDefection(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractRejectHero(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractRomanticDreamersSanctuary(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractSaberTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractSaurisTLBlog(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractSETSUNA86BLOG(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractShermaTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractShokyuuTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractSilverButterfly(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractSlimeLv1(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractSnowDust(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractStellarTransformationCon(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractSTLTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractStoneBurners(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractSunShowerFields(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractSuperPotatoTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractSymbiote(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTaptrans(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTerminusTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTheNamed(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTheSphere(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTheDefendTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTieshaunn(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTofubyu(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTranslationTreasureBox(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTranslationsFromOuterSpace(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTumbleIntoFantasy(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTusTrans(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractUnlimitedStoryWorks(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractUselessno4(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractVillageTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractWeavingstoriesandbuildingcastlesintheclouds(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractWhenTheHuntingPartyCame(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractWhimsicalLand(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractWordofCraft(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractWorldofSummie(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractWormACompleteWebSerial(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractWuxiwish(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractPridesFamiliarsMaidens(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractSoltarination(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractYiYueTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractYoutsubasilversBlog(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractZenTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractEvidasIndoRomance(item):                   # "Evida's Indo Romance"
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractXiaowen206sBlog(item):                     # "Xiaowen206's Blog"
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractAGreyWorld(item):                          # 'A Grey World'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractAliceTranslations(item):                   # 'Alice Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractAresNovels(item):                          # 'Ares Novels'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractBakaPervert(item):                         # 'Baka Pervert'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if "antihero" in item['title'].lower():
		return buildReleaseMessage(item, 'Ultimate Antihero', vol, chp, frag=frag, postfix=postfix)
	return False
def extractBladeOfHearts(item):                       # 'Blade of Hearts'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractBlublub(item):                             # 'Blublub'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractBooksMoviesAndBeyond(item):                # 'Books Movies and Beyond'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractCNovelTranlations(item):                  # 'C-Novel Tranlations…'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractCaveScans(item):                           # 'CaveScans'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractDistractedChinese(item):                   # 'Distracted Chinese'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractfgiLaNTranslations(item):                  # 'fgiLaN translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractGrowWithMe(item):                          # 'Grow with me'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractKuroTranslations(item):                    # 'Kuro Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractMousouHaven(item):                         # 'Mousou Haven'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractMyPurpleWorld(item):                       # 'My Purple World'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractMythicalPagoda(item):                      # 'Mythical Pagoda'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractN00bTranslations(item):                    # 'N00b Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNovelCow(item):                            # 'NovelCow'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractOpinisaya(item):                           # 'Opinisaya.com'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractPatriarchReliance(item):                   # 'Patriarch Reliance'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractPrideXReVamp(item):                        # 'Pride X ReVamp'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractRootOfEvil(item):                          # 'Root of Evil'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractSlothTranslationsBlog(item):               # 'Sloth Translations Blog'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if item['title'].startswith("Re:Master Magic "):
		return buildReleaseMessage(item, 'The Mage Will Master Magic Efficiently In His Second Life', vol, chp, frag=frag, postfix=postfix)

	return False
def extractSoltarinationScanlations (item):           # 'Soltarination Scanlations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractSweetACollections(item):                   # 'Sweet A Collections'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTenThousandHeavenControllingSword(item):   # 'Ten Thousand Heaven Controlling Sword'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTheAsianCult(item):                        # 'The Asian Cult'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTheLastSkull(item):                        # 'The Last Skull'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTowardsTheSky(item):                       # 'Towards the Sky~'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractXantDoesStuffAndThings(item):              # 'Xant Does Stuff and Things'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractCautrs(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractDOWsTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractHonyaku(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'OVRMMO' in item['tags']:
		return buildReleaseMessage(item, 'Toaru Ossan no VRMMO Katsudouki (WN)', vol, chp, frag=frag, postfix=postfix)
	if 'Wfb' in item['tags']:
		return buildReleaseMessage(item, 'Wizard with the flower blades', vol, chp, frag=frag, postfix=postfix, tl_type="oel")
	return False
def extractPandorasBook(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractRuisTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'A Mismatched Marriage: Records of Washed Away Injustices' in item['tags']:
		return buildReleaseMessage(item, 'A Mismatched Marriage: Records of Washed Away Injustices', vol, chp, frag=frag, postfix=postfix)
	return False
def extractWizThiefsNovels(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'My immortality It’s in a Death game' in item['title']:
		return buildReleaseMessage(item, 'My immortality It\'s in a Death game', vol, chp, frag=frag, postfix=postfix)
	if 'Thanks to a different world reincarnation' in item['title']:
		return buildReleaseMessage(item, 'Thanks to a different world reincarnation', vol, chp, frag=frag, postfix=postfix)
	if 'Grave “Z”' in item['title']:
		return buildReleaseMessage(item, 'Grave "Z"', vol, chp, frag=frag, postfix=postfix)
	return False
def extractAnotherParallelWorld(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractAnotherWorldTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Depths of Labyrinth' in item['tags']:
		return buildReleaseMessage(item, 'Aim for the Deepest Part of the Different World\'s Labyrinth', vol, chp, frag=frag, postfix=postfix)
	if 'Because, Janitor-san Is Not a Hero' in item['tags']:
		return buildReleaseMessage(item, 'Because, Janitor-san Is Not a Hero', vol, chp, frag=frag, postfix=postfix)
	if 'World Death Game' in item['tags']:
		return buildReleaseMessage(item, 'The World is Fun as it has Become a Death Game', vol, chp, frag=frag, postfix=postfix)
	return False
def extractAyaxWorld(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractBijinsans(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Benkyou no Kamisama wa Hitomishiri' in item['tags']:
		return buildReleaseMessage(item, 'Benkyou no Kamisama wa Hitomishiri', vol, chp, frag=frag, postfix=postfix)
	return False
def extractBluefireTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractChronaZero(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'tensei jinsei' in item['tags']:
		return buildReleaseMessage(item, 'Cheat Aru Kedo Mattari Kurashitai《Tensei Jinsei o Tanoshimou!》', vol, chp, frag=frag, postfix=postfix)
	if 'Level up by walking' in item['tags']:
		return buildReleaseMessage(item, 'Level up By Walking: in 10 thousand steps I will be level 10000', vol, chp, frag=frag, postfix=postfix)

	if 'When you actually went to be another world not as the Hero but as the Slave and then...' in item['tags']:
		return buildReleaseMessage(item, 'When you actually went to be another world not as the Hero but as the Slave and then...', vol, chp, frag=frag, postfix=postfix)

	return False
def extractChrononTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False

	item['title'] = item['title'].replace("’", "")

	if "Weapons cheat".lower() in item['title'].lower():
		return buildReleaseMessage(item, "Modern weapons cheat in another world", vol, chp, frag=frag, postfix=postfix)
	if "Heavenly Tribulation".lower() in item['title'].lower():
		return buildReleaseMessage(item, "Heavenly Tribulation", vol, chp, frag=frag, postfix=postfix)
	if "I can speak".lower() in item['title'].lower():
		return buildReleaseMessage(item, "I Can Speak with Animals and Demons", vol, chp, frag=frag, postfix=postfix)

	return False
def extractCloudTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractCookiePastaTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractCrappyMachineTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Blade Online' in item['tags']:
		return buildReleaseMessage(item, 'Blade Online', vol, chp, frag=frag, postfix=postfix)
	if "Another World's Savior" in item['tags']:
		return buildReleaseMessage(item, "Another World's Savior", vol, chp, frag=frag, postfix=postfix)
	return False
def extractDailyDallying(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if "Conquering Hero's Heroines" in item['tags']:
		return buildReleaseMessage(item, 'Stealing Hero\'s Lovers', vol, chp, frag=frag, postfix=postfix)
	if 'Nidome no Yuusha' in item['tags']:
		return buildReleaseMessage(item, 'Nidome no Yuusha', vol, chp, frag=frag, postfix=postfix)
	return False
def extractDekinaiDiary(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Konjiki no Word Master' in item['tags']:
		return buildReleaseMessage(item, 'Konjiki no Word Master', vol, chp, frag=frag, postfix=postfix)
	return False
def extractDisappointingTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'GSB' in item['tags']:
		return buildReleaseMessage(item, 'Galaxy Shattering Blade', vol, chp, frag=frag, postfix=postfix)
	return False
def extractFaketypist(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'The Magician wants Normality' in item['tags']:
		return buildReleaseMessage(item, 'Madoushi wa Heibon wo Nozomu', vol, chp, frag=frag, postfix=postfix)
	return False
def extractFalamarTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Isekai ni kanaderu densetsu' in item['tags']:
		return buildReleaseMessage(item, 'Isekai ni kanaderu densetsu ~toki wo tomeru mono~', vol, chp, frag=frag, postfix=postfix)
	if 'The road to become a transition master in another world' in item['tags']:
		return buildReleaseMessage(item, 'The Road to Become a Transition Master in Another World', vol, chp, frag=frag, postfix=postfix)
	return False
def extractFalinmer(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractGaochaoTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Otherworldly Evil Monarch' in item['tags']:
		return buildReleaseMessage(item, 'Otherworldly Evil Monarch', vol, chp, frag=frag, postfix=postfix)
	return False
def extractHyorinmaruBlog(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if item['title'].lower().strip().startswith("martial world – ") or 'Martial World' in item['tags']:
		return buildReleaseMessage(item, 'Martial World', vol, chp, frag=frag, postfix=postfix)
	return False
def extractJanukeTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractJoiedeVivre(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractKakkokari(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Stunning Edge' in item['tags']:
		return buildReleaseMessage(item, 'Stunning Edge', vol, chp, frag=frag, postfix=postfix)
	if 'KKDB' in item['tags']:
		return buildReleaseMessage(item, 'Koushirou Kujou the Detective Butler', vol, chp, frag=frag, postfix=postfix)
	return False
def extractKokumaTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractLickymeeTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Medusa' in item['tags']:
		return buildReleaseMessage(item, 'Regarding the Story of My Wife, Medusa', vol, chp, frag=frag, postfix=postfix)
	if 'OreOjou' in item['tags']:
		return buildReleaseMessage(item, 'Ore ga Ojousama Gakkou ni "Shomin Sample" Toshite Rachirareta Ken', vol, chp, frag=frag, postfix=postfix)
	return False
def extractLittleTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractLynfamily(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNakimushi(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Renai Kakumei Onii-chan' in item['tags']:
		return buildReleaseMessage(item, 'I, am Playing the Role of the Older Brother in Heart-throb Love Revolution.', vol, chp, frag=frag, postfix=postfix)
	return False
def extractNepustation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Cheat Majutsu' in item['tags']:
		return buildReleaseMessage(item, 'Cheat Majutsu De Unmei Wo Nejifuseru', vol, chp, frag=frag, postfix=postfix)
	return False
def extractNinjaNUF(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractPekaboBlog(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractPenguinOverlordTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractPettankoTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractPremiumRedTea(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractPsicernTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractQualideaofScumandaGoldCoin(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractRiptranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractSenjiQcreations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Sandstorm' in item['tags'] and 'Release' in item['tags']:
		return buildReleaseMessage(item, 'Sandstorm Story', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
def extractSnowyPublications(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'New Release: ' in item['title']:
		return buildReleaseMessage(item, 'Whisper of the Nightingale', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
def extractSolstar24(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'jin xiu wei yang' in item['tags']:
		return buildReleaseMessage(item, 'Jin Xiu Wei Yang', vol, chp, frag=frag, postfix=postfix)
	if 'dao qing' in item['tags']:
		return buildReleaseMessage(item, 'Dao Qing', vol, chp, frag=frag, postfix=postfix)
	return False
def extractSpringScents(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTaidadonoTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTalesofTheForgottenslayer(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'the botched summoning' in item['tags']:
		return buildReleaseMessage(item, 'The Botched Summoning', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
def extractTheIronTeeth(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractThisWorldWork(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTLSyosetsu(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if item['title'].lower().strip().startswith('defiled hero chapter'):
		return buildReleaseMessage(item, 'Defiled Hero', vol, chp, frag=frag, postfix=postfix)
	return False
def extractTranslatingForYourPleasure(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if "The Inverted Dragon's Scale" in item['tags']:
		return buildReleaseMessage(item, "The Inverted Dragon's Scale", vol, chp, frag=frag, postfix=postfix)
	return False
def extractTrungNguyen(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Bringing the Farm to Live in Another World' in item['title'] or \
		'Bringing the Farm...' in item['title']:
		return buildReleaseMessage(item, 'Bringing the Farm to Live in Another World', vol, chp, frag=frag, postfix=postfix)
	return False
def extractTurtleandHareTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Time (对的时间对的人)' in item['title']:
		return buildReleaseMessage(item, 'Time', vol, chp, frag=frag, postfix=postfix)
	return False
def extractWelcomeToTheUnderdark(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractWuxiaTranslators(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'World Defying Dan God' in item['tags']:
		return buildReleaseMessage(item, 'World Defying Dan God', vol, chp, frag=frag, postfix=postfix)
	return False
def extractAltorocTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Shadow Rogue' in item['tags']:
		return buildReleaseMessage(item, 'Shadow Rogue', vol, chp, frag=frag, postfix=postfix)
	return False
def extractTentativelyUnderconstruction(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTatakauShishoLightNovelTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractDragonMT(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Dragon Life' in item['tags']:
		return buildReleaseMessage(item, 'Dragon Life', vol, chp, frag=frag, postfix=postfix)

	return False


def extractTinkerbellsan(item):                     # 'Tinkerbell-san'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Caught in my Own Trap' in item['tags']:
		return buildReleaseMessage(item, 'Caught in my Own Trap', vol, chp, frag=frag, postfix=postfix)
	return False
def extractUnlimitedNovelFailures(item):            # 'Unlimited Novel Failures'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTwig(item):                              # 'Twig'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractTwelveMonthsofMay(item):                 # 'Twelve Months of May'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'My Mister Ostrich' in item['tags'] and 'English translation' in item['tags']:
		return buildReleaseMessage(item, 'Wo De Tuo Niao Xian Sheng', vol, chp, frag=frag, postfix=postfix)
	return False
def extractNovelsGround(item):                      # 'Novels Ground'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Legend of the Cultivation God' in item['tags'] or 'LOTCG' in item['tags']:
		return buildReleaseMessage(item, 'Legend of the Cultivation God', vol, chp, frag=frag, postfix=postfix)
	if 'Miracle Throne' in item['tags'] or 'LOTCG' in item['tags']:
		return buildReleaseMessage(item, 'Miracle Throne', vol, chp, frag=frag, postfix=postfix)
	return False
def extractAsd398(item):                            # 'asd398'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if "Don't tell me this is the true history of the Three Kingdoms!" in item['tags']:
		return buildReleaseMessage(item, "Don't tell me this is the true history of the Three Kingdoms!", vol, chp, frag=frag, postfix=postfix)
	if 'Leading an Explosive Revolution in Another World!' in item['tags']:
		return buildReleaseMessage(item, 'Leading an Explosive Revolution in Another World!', vol, chp, frag=frag, postfix=postfix)
	return False
def extractLittleNovelTranslation(item):            # 'Little Novel Translation'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'GTI Release' in item['tags']:
		return buildReleaseMessage(item, 'Godly Thief Incarnation', vol, chp, frag=frag, postfix=postfix)
	return False
def extractReadMeTranslations(item):                # 'Read Me Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractBallKickingGangBoss(item):               # "'Ball'-Kicking Gang Boss"
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'jinsei' in item['tags']:
		return buildReleaseMessage(item, "I'll Live My Second Life!", vol, chp, frag=frag, postfix=postfix)
	return False
def extractFakTranslations(item):                   # 'Fak Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Shrouding the Heavens' in item['tags']:
		return buildReleaseMessage(item, 'Shrouding the Heavens', vol, chp, frag=frag, postfix=postfix)
	return False
def extractAmeryEdge(item):                         # 'Amery Edge'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False

	if 'Your Highness, I Know My Wrong' in item['tags'] or 'Your Highness, I Know My Wrongs' in item['tags']:
		return buildReleaseMessage(item, 'Your Highness, I Know My Wrong', vol, chp, frag=frag, postfix=postfix)
	if '108 Star Maidens of Destiny' in item['tags']:
		return buildReleaseMessage(item, '108 Star Maidens of Destiny', vol, chp, frag=frag, postfix=postfix)
	if 'Zombie Girl, Where Are You?' in item['tags']:
		return buildReleaseMessage(item, 'Zombie Girl, Where Are You?', vol, chp, frag=frag, postfix=postfix)

	return False
def extractRidwanTrans(item):                       # 'RidwanTrans'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractRinOtakuBlog(item):                      # 'RinOtakuBlog'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Netooku Otoko' in item['tags']:
		return buildReleaseMessage(item, 'Netooku Otoko no Tanoshii Isekai Boueki', vol, chp, frag=frag, postfix=postfix)
	if 'Sonohi Sekai ga Kawatta' in item['tags']:
		return buildReleaseMessage(item, 'Sonohi Sekai ga Kawatta', vol, chp, frag=frag, postfix=postfix)
	return False
def extractShell2lyCNovelSite(item):                # 'Shell2ly C-Novel Site'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractMonkotosTranslations(item):              # "Monkoto's Translations"
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractLittleShanksTranslations(item):          # 'LittleShanks Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractWLTranslations(item):                    # 'WL Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Chapter Releases' in item['tags'] and 'OSI' in item['tags']:
		return buildReleaseMessage(item, 'One Sword to Immortality', vol, chp, frag=frag, postfix=postfix)
	return False
def extractHellYeah524(item):                       # 'Hell Yeah 524'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if item['tags'] == ['Uncategorized'] and item['title'].startswith("Chapter"):
		return buildReleaseMessage(item, 'Awakening – 仿如昨日', vol, chp, frag=frag, postfix=postfix)
	if item['tags'] == ['Uncategorized'] and item['title'].startswith("Shadow Rogue: "):
		return buildReleaseMessage(item, 'Shadow Rogue', vol, chp, frag=frag, postfix=postfix)
	return False
def extractTarableTranslations(item):               # 'Tarable Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractBayabuscoTranslation(item):              # 'Bayabusco Translation'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractBruinTranslation(item):                  # 'Bruin Translation'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractDHHTranslations(item):                   # 'DHH Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractEpithetic(item):                         # 'Epithetic'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractJunJuntianxia(item):                     # 'Jun Juntianxia'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractKawaiiDaikon(item):                      # 'Kawaii Daikon'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractLingTranslatesSometimes(item):           # 'Ling Translates Sometimes'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractKyoptionslibrary(item):     # 'kyoptionslibrary.blogspot.com'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractSnowTranslations(item):                  # 'Snow Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractDadIsHeroFanTranslations(item):          # 'DadIsHero Fan Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractUnnamedtranslations(item):  # 'unnamedtranslations.blogspot.com'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractRedLanternArchives(item):                # 'Red Lantern Archives'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Outaishihi ni Nante Naritakunai!!' in item['tags']:
		return buildReleaseMessage(item, 'Outaishihi ni Nante Naritakunai!!', vol, chp, frag=frag, postfix=postfix)
	return False
def extractLohithbbTLs(item):                       # 'Lohithbb TLs'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractHikkinoMoriTranslations(item):           # 'Hikki no Mori Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractDemerithTranslation(item):               # 'Demerith Translation'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractMTLCrap(item):                           # 'MTLCrap'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractAnneAndCindy(item):                      # 'Anne And Cindy'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNovelisation(item):                      # 'Novelisation'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNTRHolic(item):                          # 'NTRHolic'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractDeliciousTranslations(item):             # 'Delicious Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractStarrydawnTranslations(item):            # 'Starrydawn Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractSkullSquadron(item):                     # 'Skull Squadron'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractSleepyTranslations(item):                # 'Sleepy Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractLypheonMachineTranslation(item):         # 'Lypheon Machine Translation'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNoodletownTranslated(item):              # 'Noodletown Translated'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False



def extractZeonic(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractU3000(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNanowaveTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractHeroicLegendOfArslanTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractDreamlessWindowsTranslation(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractKoongKoongTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extract天才創造すなわち百合(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractForwardSlash(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Isekai ni Demodori Shimashita?' in item['tags']:
		return buildReleaseMessage(item, 'Isekai ni Demodori Shimashita?', vol, chp, frag=frag, postfix=postfix)

	return False
def extractKeyoTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractMojoTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractZxzxzxsBlog(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def extractAngry(item):                       # 'ヾ(。￣□￣)ﾂ'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def extract一期一会万歳(item):                 # '一期一会, 万歳!'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def extract睡眠中毒(item):                     # '睡眠中毒'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def extract輝く世界(item):                     # '輝く世界'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def extractNovelTrans(item):               # 'Novel Trans'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False





def extractEmruyshitTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractNegaTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Kaette Kita Motoyuusha' in item['tags']:
		return buildReleaseMessage(item, 'Kaette Kita Motoyuusha', vol, chp, frag=frag, postfix=postfix)
	if 'Takami no Kago' in item['tags']:
		return buildReleaseMessage(item, 'Takami no Kago', vol, chp, frag=frag, postfix=postfix)
	return False
def extractNightFallTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractOyasumiReads(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractSpiritualTranscription(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False

	if 'TEO' in item['tags'] or 'The Empyrean Overlord' in item['tags']:
		return buildReleaseMessage(item, 'The Empyrean Overlord', vol, chp, frag=frag, postfix=postfix)


	return False
def extractTryTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False


def extractRealmOfChaos(item):               #'Realm of Chaos'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def extractAlbertKenoreijou(item):           #'Albert Kenoreijou'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def extractPiggyBottleTranslations(item):    #'PiggyBottle Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if item['title'].lower().startswith('beseech the devil'):
		return buildReleaseMessage(item, 'Beseech the Devil', vol, chp, frag=frag, postfix=postfix)
	return False

def extractSandwichKingdom(item):            #'Sandwich Kingdom'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'sougen no okite' in item['tags']:
		return buildReleaseMessage(item, 'Sougen no Okite ~Shii yatsu ga moteru, ii buzoku ni umarekawatta zo~', vol, chp, frag=frag, postfix=postfix)
	if 'kininaru kanojo wo tokoton okashi tsukusu hanshi' in item['tags']:
		return buildReleaseMessage(item, 'Kininaru Kanojo wo Totokon Okashi Tsukusu Hanashi', vol, chp, frag=frag, postfix=postfix)
	return False

def extractTyrantsEyeTranslations(item):     #'Tyrant\'s Eye Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def extractKONDEETranslations(item):         #'KONDEE Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def extractUkel2x(item):                     #'Ukel2x'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if item['title'].lower().startswith('volume'):
		return buildReleaseMessage(item, 'Kokugensou wo Item Cheat de Ikinuku', vol, chp, frag=frag, postfix=postfix)
	return False

def extractProcrasTranslation(item):         #'ProcrasTranslation'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def extractNovelsJapan(item):                #'Novels Japan'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if item['title'].lower().endswith('loner dungeon'):
		return buildReleaseMessage(item, 'I who is a Loner, Using cheats adapts to the Dungeon', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().endswith('vending machine'):
		return buildReleaseMessage(item, 'I was Reborn as a Vending Machine, Wandering in the Dungeon', vol, chp, frag=frag, postfix=postfix)
	return False

def extract7DaysTrial(item):                 #'7 Days Trial'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'content' in item['tags']:
		return buildReleaseMessage(item, 'War of the Supreme', vol, chp, frag=frag, postfix=postfix)
	return False

def extractDokuHanaTranslations(item):       #'DokuHana Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def extractEnsigsWritings(item):             #'Ensig\'s Writings'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False



####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################


def extractTrinityArchive(item):                      # 'Trinity Archive'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Summoned Slaughterer' in item['tags']:
		return buildReleaseMessage(item, 'Summoned Slaughterer', vol, chp, frag=frag, postfix=postfix)
	return False
def extractAranTranslations(item):                    # 'Aran Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if item['title'].startswith("IGE – "):
		return buildReleaseMessage(item, 'Imperial God Emperor', vol, chp, frag=frag, postfix=postfix)
	return False
def extractChubbyCheeks(item):                        # 'ChubbyCheeks'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'A Mistaken Marriage Match: Mysteries in the Imperial Harem' in item['tags']:
		return buildReleaseMessage(item, 'A Mistaken Marriage Match: Mysteries in the Imperial Harem', vol, chp, frag=frag, postfix=postfix)
	return False
def extractTseirpTranslations(item):                  # 'Tseirp Translations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'IS SS' in item['title'] and not postfix:
		postfix = "Side Story"
	if item['title'].startswith("IS "):
		return buildReleaseMessage(item, 'Invincible Saint ~Salaryman, the Path I Walk to Survive in This Other World~', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith("GC "):
		return buildReleaseMessage(item, 'I\'ve Became Able to Do Anything With My Growth Cheat, but I Can\'t Seem to Get Out of Being Jobless', vol, chp, frag=frag, postfix=postfix)
	return False
def extractQualiTeaTranslations(item):                # 'QualiTeaTranslations'
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Romance of Dragons and Snakes' in item['tags']:
		return buildReleaseMessage(item, 'Romance of Dragons and Snakes', vol, chp, frag=frag, postfix=postfix)
	return False


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
	if 'Jianghu Road is Curved' in item['tags']:
		return buildReleaseMessage(item, 'Jianghu Road is Curved', vol, chp, frag=frag, postfix=postfix)

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

	if item['title'].startswith('Jobless'):
		return buildReleaseMessage(item, 'I Aim to Be an Adventurer with the Jobclass of "Jobless"', vol, chp, frag=frag, postfix=postfix)

	if 'The Harem Was a Forced Goal' in item['tags'] or 'THWAFG' in item['title']:
		if "SS" in item['title'] and not postfix:
			postfix = "Side Story"
		return buildReleaseMessage(item, 'The Harem Was a Forced Goal', vol, chp, frag=frag, postfix=postfix)
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
	if "Stealing Hero's Lovers" in item['tags']:
		return buildReleaseMessage(item, "Stealing Hero's Lovers", vol, chp, frag=frag, postfix=postfix)
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

	if item['title'].lower().startswith('sin city'):
		return buildReleaseMessage(item, 'Sin City', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('zhan xian'):
		return buildReleaseMessage(item, 'Zhan Xian', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('heaven awakening path'):
		return buildReleaseMessage(item, 'Heaven Awakening Path', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('immortal executioner'):
		return buildReleaseMessage(item, 'Immortal Executioner', vol, chp, frag=frag, postfix=postfix)

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
	if 'The Youthful You Who Was So Beautiful' in item['tags']:
		return buildReleaseMessage(item, 'The Youthful You Who Was So Beautiful', vol, chp, frag=frag, postfix=postfix)

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
def extractEccentricTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "ILK" in item['tags']:
		return buildReleaseMessage(item, "Invincible Leveling King", vol, chp, frag=frag, postfix=postfix)
	if 'ATF' in item['tags']:
		return buildReleaseMessage(item, "After Transformation, Mine and Her Wild Fantasy", vol, chp, frag=frag, postfix=postfix)
	if 'DTW' in item['tags']:
		return buildReleaseMessage(item, "Doctoring the World", vol, chp, frag=frag, postfix=postfix)
	if 'TKDG' in item['tags']:
		return buildReleaseMessage(item, 'The Kind Death God', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractECWebnovel(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if item['title'].lower().startswith("volume"):
		return buildReleaseMessage(item, "EC", vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith("great merchant - dao ming"):
		return buildReleaseMessage(item, "Great Merchant - Dao Ming", vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractLightNovelsTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'I Just About Became a Living Cheat when Raising My Level in the Real Life' in item['tags'] \
		or 'I Became a Living Cheat' in item['tags']:
		return buildReleaseMessage(item, "I Just About Became a Living Cheat when Raising My Level in the Real World", vol, chp, frag=frag, postfix=postfix)
	if 'HimeKishi Ga Classmate!' in item['tags']:
		return buildReleaseMessage(item, "Himekishi ga Classmate! ~ Isekai Cheat de Dorei ka Harem~", vol, chp, frag=frag, postfix=postfix)
	if 'Re:Master Magic' in item['tags']:
		return buildReleaseMessage(item, "The Mage Will Master Magic Efficiently In His Second Life", vol, chp, frag=frag, postfix=postfix)
	if 'The Man Who Would Be King' in item['tags']:
		return buildReleaseMessage(item, 'The Man Who Would Be King', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWillfulCasual(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Chu Wang Fei' in item['tags']:
		return buildReleaseMessage(item, "Chu Wang Fei", vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractIntenseDesSugar(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Congratulation Empress' in item['tags']:
		return buildReleaseMessage(item, 'Congratulation Empress', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractTheBeginningAfterTheEnd(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if ":" in item['title'] and not postfix:
		postfix = item['title'].split(":")[-1]
	return buildReleaseMessage(item, 'The Beginning After The End', vol, chp, frag=frag, postfix=postfix, tl_type='oel')


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