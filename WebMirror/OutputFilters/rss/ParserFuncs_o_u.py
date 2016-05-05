
from WebMirror.OutputFilters.util.MessageConstructors import buildReleaseMessage
from WebMirror.OutputFilters.util.TitleParsers import extractChapterVol
from WebMirror.OutputFilters.util.TitleParsers import extractChapterVolFragment
from WebMirror.OutputFilters.util.TitleParsers import extractVolChapterFragmentPostfix

import re

####################################################################################################################################################
def extractSousetsuka(item):
	'''
	# Sousetsuka
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Desumachi' in item['tags'] or 'Death March kara Hajimaru Isekai Kyousoukyoku' in item['title']:

		extract = re.search(r'Kyousoukyoku (\d+)\-(\d+)', item['title'])
		if extract and not vol:
			vol = int(extract.group(1))
			chp = int(extract.group(2))
		return buildReleaseMessage(item, "Death March kara Hajimaru Isekai Kyousoukyoku", vol, chp, frag=frag, postfix=postfix)

	return False



####################################################################################################################################################
def extractOniichanyamete(item):
	'''
	お兄ちゃん、やめてぇ！ / Onii-chan Yamete
	'''
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
	return False




####################################################################################################################################################
def extractTheLazy9(item):
	'''
	# TheLazy9
	'''

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
def extractPikaTranslations(item):
	'''
	# Pika Translations

	'''
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
def extractShinTranslations(item):
	'''
	# Shin Translations

	'''
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if 'THE NEW GATE' in item['tags'] and not 'Status Update' in item['tags']:
		if chp and vol and frag:
			return buildReleaseMessage(item, 'The New Gate', vol, chp, frag=frag)
	return False



####################################################################################################################################################
def extractScryaTranslations(item):
	'''
	# Scrya Translations

	'''
	chp, vol, frag = extractChapterVolFragment(item['title'])

	if "So What if It's an RPG World!?" in item['tags']:
		return buildReleaseMessage(item, "So What if It's an RPG World!?", vol, chp, frag=frag)

	if 'My Disciple Died Yet Again' in item['tags']:
		return buildReleaseMessage(item, 'My Disciple Died Yet Again', vol, chp, frag=frag)

	return False



####################################################################################################################################################

def extractSkythewood(item):
	'''
	# Skythewood translations

	'''
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
def extractThatGuyOverThere(item):
	'''
	# That Guy Over There

	'''
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
def extractOtterspaceTranslation(item):
	'''
	# Otterspace Translation

	'''
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
def extractTrippTl(item):
	'''
	# Tripp Translations

	'''
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Majin Tenseiki' in item['title']:
		return buildReleaseMessage(item, 'Majin Tenseiki', vol, chp, frag=frag)

	return False


def extractSaiakuTranslationsBlog(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False

	if item['title'].startswith('She Professed Herself The Pupil Of The Wiseman'):
		return buildReleaseMessage(item, 'Kenja no Deshi wo Nanoru Kenja', vol, chp, frag=frag, postfix=postfix)
	return False



####################################################################################################################################################
def extractRaisingTheDead(item):
	'''
	# extractRaisingTheDead

	'''
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
def extractTensaiTranslations(item):
	'''
	# Tensai Translations

	'''
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Spirit Migration' in item['tags']:
		return buildReleaseMessage(item, 'Spirit Migration', vol, chp, frag=frag)

	if 'Tsuyokute New Saga' in item['tags']:
		return buildReleaseMessage(item, 'Tsuyokute New Saga', vol, chp, frag=frag)

	return False



####################################################################################################################################################
def extractThunder(item):
	'''
	# Thunder Translations:

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Stellar Transformations' in item['tags'] and (vol or chp):
		return buildReleaseMessage(item, 'Stellar Transformations', vol, chp, frag=frag, postfix=postfix)
	return False



####################################################################################################################################################
def extractTuShuGuan(item):
	'''
	# 中翻英圖書館 Translations

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'He Jing Kunlun' in item['tags'] and (vol or chp or postfix):
		return buildReleaseMessage(item, 'The Crane Startles Kunlun', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
def extractSwordAndGame(item):
	'''
	# Sword And Game

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'The Rising of the Shield Hero' in item['tags'] and 'chapter' in [tmp.lower() for tmp in item['tags']]:
		return buildReleaseMessage(item, 'The Rise of the Shield Hero', vol, chp, frag=frag, postfix=postfix)
	if 'Ark' in item['tags'] and (vol or chp or postfix):
		return buildReleaseMessage(item, 'Ark', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractOhanashimi(item):
	'''
	# Ohanashimi

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if ":" in item['title']:
		postfix = item['title'].split(":", 1)[-1]

	if 'Seijo no Kaifuku Mahou' in item['tags']:
		return buildReleaseMessage(item, 'Seijo no Kaifuku Mahou ga Dou Mitemo Ore no Rekkaban na Ken ni Tsuite', vol, chp, frag=frag, postfix=postfix)
	if 'Tate no Yuusha' in item['tags']:
		return buildReleaseMessage(item, 'The Rise of the Shield Hero', vol, chp, frag=frag, postfix=postfix)
	if 'No Fatigue' in item['tags'] or item['title'].lower().startswith("nf: "):
		return buildReleaseMessage(item, 'NO FATIGUE ~24 Jikan Tatakaeru Otoko no Tenseitan~', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractOmegaHarem(item):
	'''
	# Omega Harem Translations

	'''
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
def extractPuttty(item):
	'''
	# putttytranslations

	'''
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
def extractRisingDragons(item):
	'''
	# Rising Dragons Translation

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'God and Devil World' in item['tags'] and 'Release' in item['tags']:
		return buildReleaseMessage(item, 'Shenmo Xitong', vol, chp, frag=frag, postfix=postfix)
	return False


####################################################################################################################################################
def extractSylver(item):
	'''
	# Sylver Translations

	'''
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
def extractTomorolls(item):
	'''
	# Tomorolls

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Cicada as Dragon' in item['tags'] or 'Semi Datte Tensei Sureba Ryuu Ni Naru' in item['title']:
		return buildReleaseMessage(item, 'Cicada as Dragon', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
def extractTotokk(item):
	'''
	# Totokk\'s Translations

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	# Lawl, title typo
	if '[SYWZ] Chapter' in item['title'] or '[SWYZ] Chapter' in item['title'] \
		or '[SYWZ]' in item['title'] or 'Shen Yin Wang Zuo, Chapter' in item['title']:
		return buildReleaseMessage(item, 'Shen Yin Wang Zuo', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
def extractTranslationNations(item):
	'''
	# Translation Nations

	'''
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
def extractTonyYonKa(item):
	'''
	# tony-yon-ka.blogspot.com (the blog title is stupidly long)

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Manowa' in item['title'] and chp:
		return buildReleaseMessage(item, 'Manowa Mamono Taosu Nouryoku Ubau Watashi Tsuyokunaru', vol, chp, frag=frag, postfix=postfix)
	if 'Vampire Princess' in item['title'] and chp:
		return buildReleaseMessage(item, 'Kyuuketsu Hime wa Barairo no Yume o Miru', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
def extractRebirthOnlineWorld(item):
	'''

	'''
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
def extractRuzeTranslations(item):
	'''
	# Ruze Translations

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Guang Zhi Zi' in item['title'] and (chp or vol):
		return buildReleaseMessage(item, 'Guang Zhi Zi', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractTsuigeki(item):
	'''
	# Tsuigeki Translations

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Seiju no Kuni no Kinju Tsukai' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Seiju no Kuni no Kinju Tsukai', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractUnchainedTranslation(item):
	'''
	# Unchained Translation

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'The Alchemist God' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Ascension of the Alchemist God', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractShikkakuTranslations(item):
	'''
	# Shikkaku Translations

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if "kuro no maou" in item['title'].lower():
		return buildReleaseMessage(item, 'Kuro no Maou', vol, chp, frag=frag, postfix=postfix)
	if 'KENS' in item['tags']:
		return buildReleaseMessage(item, 'Kamigoroshi no Eiyuu to Nanatsu no Seiyaku', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractRhinabolla(item):
	'''
	# Rhinabolla

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Hachi-nan Chapter' in item['title'] and not 'draft' in item['title'].lower():
		return buildReleaseMessage(item, 'Hachinan tte, Sore wa nai Deshou!', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractSotranslations(item):
	'''
	# Supreme Origin Translations

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'hachi-nan chapter' in item['title'].lower() and not 'draft' in item['title'].lower():
		return buildReleaseMessage(item, 'Hachinan tte, Sore wa nai Deshou!', vol, chp, frag=frag, postfix=postfix)

	if 'the devil of an angel chapter' in item['title'].lower() and not 'draft' in item['title'].lower():
		return buildReleaseMessage(item, 'The Devil of an Angel Chapter', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractTurb0(item):
	'''
	# Turb0 Translation

	'''
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
def extractShiroyukineko(item):
	'''
	# 'Shiroyukineko Translations'

	'''
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
# '桜翻訳! | Light novel translations'
####################################################################################################################################################
def extractSakurahonyaku(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'hyouketsu kyoukai no eden' in item['tags']:
		return buildReleaseMessage(item, 'Hyouketsu Kyoukai no Eden', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractRancer(item):
	'''

	'''
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
def extractRadiantTranslations(item):
	'''

	'''
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
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if any('volume' in tag.lower() for tag in item['tags']) and (chp or vol):
		return buildReleaseMessage(item, 'Tales of MU', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractPeasKingdom(item):
	'''

	'''
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
def extractSolitaryTranslation(item):
	'''

	'''
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
	'''

	'''
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
	'''

	'''
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
def extractShinsori(item):
	'''

	'''
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
	'''

	'''
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
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "teaser" in item['title'].lower():
		return False

	if 'Isekai Mahou....' in item['tags']:
		return buildReleaseMessage(item, 'Isekai Mahou wa Okureteru!', vol, chp, frag=frag, postfix=postfix)


	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractTotallyInsaneTranslation(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "PMG" in item['tags']:
		return buildReleaseMessage(item, "Peerless Martial God", vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractTrungtNguyen(item):
	'''

	'''
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
	'''

	'''
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
def extractOneManArmy(item):
	'''

	'''
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
def extractOKTranslation(item):
	'''

	'''
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
	'''

	'''
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
def extractRainbowTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Myriad of Shades' in item['tags']:
		return buildReleaseMessage(item, 'Myriad of Shades', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractOmgitsaray(item):
	'''

	'''
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
	'''

	'''
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
	'''

	'''

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
def extractPrinceRevolution(item):
	'''

	'''
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
def extractUntunedTranslation(item):
	'''

	'''
	title = item['title'].replace(" III(", " vol 3 (") \
		.replace(" III:",                  " vol 3:") \
		.replace(" II:",                   " vol 2:") \
		.replace(" I:",                    " vol 1:") \
		.replace(" IV:",                   " vol 4:") \
		.replace(" V:",                    " vol 5:")

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(title)
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'meg and seron' in item['tags'] and chp and vol:
		return buildReleaseMessage(item, 'Meg and Seron', vol, chp, frag=frag, postfix=postfix)

	if 'lillia and treize' in item['tags'] and chp and vol:
		return buildReleaseMessage(item, 'Lillia to Treize', vol, chp, frag=frag, postfix=postfix)


	# TODO: Needs the facility to parse roman numerals!

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractRumorsBlock(item):
	'''

	'''
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
	'''

	'''
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
	'''

	'''
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
def extractSubudai11(item):
	'''

	'''
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
def extractOneSecondSpring(item):
	'''

	'''
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
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Godly Hunter' in item['tags'] :
		return buildReleaseMessage(item, 'Godly Hunter', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractRoxism(item):
	'''

	'''
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
def extractSilvasLibrary(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if "Silva's Diary - Zero no Tsukaima" in item['tags'] :
		return buildReleaseMessage(item, "Silva's Diary - Zero no Tsukaima", vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'God of Destruction' in item['tags'] :
		return buildReleaseMessage(item, 'God of Destruction', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'God of Chaos' in item['tags'] :
		return buildReleaseMessage(item, 'God of Chaos', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'My Path of Justice' in item['tags'] or 'MPJ1' in item['tags']:
		return buildReleaseMessage(item, 'My Path of Justice', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Truth and Myths' in item['tags'] :
		return buildReleaseMessage(item, 'Truth and Myths', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Soft Spoken Brutality' in item['tags'] :
		return buildReleaseMessage(item, 'Soft Spoken Brutality', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'World of Immortals' in item['tags'] :
		return buildReleaseMessage(item, 'World of Immortals', vol, chp, frag=frag, postfix=postfix)
	if 'Bu ni mi' in item['tags'] :
		return buildReleaseMessage(item, 'Bu ni mi', vol, chp, frag=frag, postfix=postfix)
	if 'Rinkan no Madoushi' in item['tags'] :
		return buildReleaseMessage(item, 'Rinkan no Madoushi', vol, chp, frag=frag, postfix=postfix)
	if 'Arifureta' in item['tags'] :
		return buildReleaseMessage(item, 'Arifureta Shokugyou de Sekai Saikyou', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractOriginNovels(item):
	'''

	'''
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
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if "Chapter" in item['tags'] and 'ascension' in item['tags'] :
		return buildReleaseMessage(item, 'The Ascension Chronicle', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractTsukigomori(item):
	'''

	'''
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
def extractSutekiDaNe(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Can I Not Marry?' in item['tags']:
		return buildReleaseMessage(item, 'Can I Not Marry? / Days of Cohabitation with the President', vol, chp, frag=frag, postfix=postfix)
	if "Black Bellied Prince's Stunning Abandoned Consort" in item['tags']:
		return buildReleaseMessage(item, "Black Bellied Prince's Stunning Abandoned Consort", vol, chp, frag=frag, postfix=postfix)


	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractSilentTl(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Legend' in item['tags']:
		return buildReleaseMessage(item, "Legend", vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractTranslatingZeTianJi(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	return buildReleaseMessage(item, "Ze Tian Ji ", vol, chp, frag=frag, postfix=postfix)



####################################################################################################################################################
#
####################################################################################################################################################
def extractSoojikisProject(item):
	'''

	'''
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
def extractProjectAccelerator(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Black Healer' in item['tags']:
		return buildReleaseMessage(item, 'Black Healer', vol, chp, frag=frag, postfix=postfix)
	return False










def  extractPrideXReVamp(item):
	'''
	# 'Pride X ReVamp'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractRaisingAngelsDefection(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractProcrasTranslation(item):
	'''
	#'ProcrasTranslation'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Slowlife' in item['tags']:
		return buildReleaseMessage(item, 'Tensei Shite Inaka de Slowlife wo Okuritai', vol, chp, frag=frag, postfix=postfix)
	return False


def  extractPeaTranslation(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractPekaboBlog(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTerminusTranslation(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTaint(item):
	'''

	'''
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

def  extractUselessno4(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractPettankoTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if item['title'].startswith('Isekai C-mart Hanjouki'):
		return buildReleaseMessage(item, 'Isekai C-mart Hanjouki', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractQualityMistranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractShell2lyCNovelSite(item):
	'''
	# 'Shell2ly C-Novel Site'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False

	fragfound = re.search(r'\((\d+)\)', item['title'])
	if not frag and fragfound:
		frag = int(fragfound.group(1))
	if 'MMSTEM' in  item['tags']:
		return buildReleaseMessage(item, 'Madam, Master Said to Eat Meal', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractOregaHeroineinEnglish(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractSnowyPublications(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'New Release: ' in item['title']:
		return buildReleaseMessage(item, 'Whisper of the Nightingale', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False

def  extractPandorasBook(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractSlothTranslationsBlog(item):
	'''
	# 'Sloth Translations Blog'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if item['title'].startswith("Re:Master Magic "):
		return buildReleaseMessage(item, 'The Mage Will Master Magic Efficiently In His Second Life', vol, chp, frag=frag, postfix=postfix)

	return False

def  extractPatriarchReliance(item):
	'''
	# 'Patriarch Reliance'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False

	# Shitty assumption, if there is no prefix, it's probably a God and Devil World release.
	if re.match(r"Chapters? \d+", item['title']):
		return buildReleaseMessage(item, 'God and Devil World', vol, chp, frag=frag, postfix=postfix)

	return False

def  extractTentativelyUnderconstruction(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTwig(item):
	'''
	# 'Twig'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractSunShowerFields(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTinkerbellsan(item):
	'''
	# 'Tinkerbell-san'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Caught in my Own Trap' in item['tags']:
		return buildReleaseMessage(item, 'Caught in my Own Trap', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractPenguinOverlordTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractPactWebSerial(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTatakauShishoLightNovelTranslation(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractShokyuuTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractPriddlesTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Magic is Japanese' in item['tags']:
		return buildReleaseMessage(item, 'Magic is Japanese', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractTyrantsEyeTranslations(item):
	'''
	#'Tyrant\'s Eye Translations'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False


def  extractTheLastSkull(item):
	'''
	# 'The Last Skull'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTranslationsFromOuterSpace(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractRuisTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'A Mismatched Marriage: Records of Washed Away Injustices' in item['tags']:
		return buildReleaseMessage(item, 'A Mismatched Marriage: Records of Washed Away Injustices', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractSenjiQcreations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Sandstorm' in item['tags'] and 'Release' in item['tags']:
		return buildReleaseMessage(item, 'Sandstorm Story', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False

def  extractPsicernTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractSymbiote(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractUnlimitedStoryWorks(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTalesOfPaulTwister(item):
	'''

	'''
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

def  extractRejectHero(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractRealmOfChaos(item):
	'''
	#'Realm of Chaos'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False

	if 'Myriad of Shades' in item['tags']:
		names = [tmp for tmp in item['tags'] if tmp in ['Celest Ambrosia', 'Kiriko', 'Melanie Ambrosia', 'Shana Bonnet', 'Silvia', 'XCrossJ', 'Ghost']]
		postfix_out = ", ".join(names)
		if postfix:
			postfix_out +=  " - " + postfix
		return buildReleaseMessage(item, 'Myriad of Shades', vol, chp, frag=frag, postfix=postfix_out, tl_type='oel')
	return False

def  extractTieshaunn(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractSTLTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTowardsTheSky(item):
	'''
	# 'Towards the Sky~'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractSinsOfTheFathers(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	return buildReleaseMessage(item, 'Sins of the Fathers '.lower(), vol, chp, frag=frag, postfix=postfix, tl_type='oel')

####################################################################################################################################################
#
####################################################################################################################################################

def  extractTofubyu(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractSkullSquadron(item):
	'''
	# 'Skull Squadron'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractSuperPotatoTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractU3000(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractStarrydawnTranslations(item):
	'''
	# 'Starrydawn Translations'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractSnowTranslations(item):
	'''
	# 'Snow Translations'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTalesofTheForgottenslayer(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'the botched summoning' in item['tags']:
		return buildReleaseMessage(item, 'The Botched Summoning', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False

def  extractShermaTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractPumpkinTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractPremiumRedTea(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTseirpTranslations(item):
	'''
	# 'Tseirp Translations'
	'''
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

def  extractStoneBurners(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractPandafuqTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	# Fragments are written "Name {chapter} ({frag})". Arrrgh.

	return False


####################################################################################################################################################
#
####################################################################################################################################################

def  extractPippiSite(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'FMTL – Chapter' in item['title']:
		return buildReleaseMessage(item, 'First Marriage Then Love', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractSweetACollections(item):
	'''
	# 'Sweet A Collections'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractRoastedTea(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractSpringScents(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractOpinisaya(item):
	'''
	# 'Opinisaya.com'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTaidadonoTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractSaurisTLBlog(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractSilverButterfly(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTheSphere(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractSnowDust(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractRiptranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTheBeginningAfterTheEnd(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if ":" in item['title'] and not postfix:
		postfix = item['title'].split(":")[-1]
	return buildReleaseMessage(item, 'The Beginning After The End', vol, chp, frag=frag, postfix=postfix, tl_type='oel')


####################################################################################################################################################
#
####################################################################################################################################################

def  extractSoltarinationScanlations (item):
	'''
	# 'Soltarination Scanlations'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractRosyFantasy(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Yu Ren' in item['tags']:
		return buildReleaseMessage(item, 'Yu Ren', vol, chp, frag=frag, postfix=postfix)
	if 'Chu Wang Fei' in item['tags']:
		return buildReleaseMessage(item, 'Chu Wang Fei', vol, chp, frag=frag, postfix=postfix)
	if 'Seven Unfortunate Lifetimes' in item['tags']:
		return buildReleaseMessage(item, 'Seven Unfortunate Lifetimes', vol, chp, frag=frag, postfix=postfix)
	if 'All Thanks to a Single Moment of Impulse' in item['tags']:
		return buildReleaseMessage(item, 'All Thanks to a Single Moment of Impulse', vol, chp, frag=frag, postfix=postfix)
	if 'White Calculation' in item['tags']:
		return buildReleaseMessage(item, 'White Calculation', vol, chp, frag=frag, postfix=postfix)
	if "demon wang's gold medal status favorite fei" in item['tags'] or \
		item['title'].startswith('DWGMSFF') or \
		"demon's wang golden favorite fei" in item['tags']:
		return buildReleaseMessage(item, "Demon Wang's Golden Favorite Fei", vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractTrungNguyen(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Bringing the Farm to Live in Another World' in item['title'] or \
		'Bringing the Farm...' in item['title']:
		return buildReleaseMessage(item, 'Bringing the Farm to Live in Another World', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractRedDragonTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Kaettekite mo fantasy' in item['tags']:
		return buildReleaseMessage(item, 'Kaettekite mo Fantasy!?', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractThisWorldWork(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractSandwichKingdom(item):
	'''
	#'Sandwich Kingdom'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'sougen no okite' in item['tags']:
		return buildReleaseMessage(item, 'Sougen no Okite ~Shii yatsu ga moteru, ii buzoku ni umarekawatta zo~', vol, chp, frag=frag, postfix=postfix)
	if 'kininaru kanojo wo tokoton okashi tsukusu hanshi' in item['tags']:
		return buildReleaseMessage(item, 'Kininaru Kanojo wo Totokon Okashi Tsukusu Hanashi', vol, chp, frag=frag, postfix=postfix)
	if 'game sekai tenseishitara' in item['tags']:
		return buildReleaseMessage(item, 'After Reincarnating Into This Game World I Seemed to Have Taken Over the Control of Status', vol, chp, frag=frag, postfix=postfix)
	return False


def  extractRinOtakuBlog(item):
	'''
	# 'RinOtakuBlog'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Netooku Otoko' in item['tags']:
		return buildReleaseMessage(item, 'Netooku Otoko no Tanoshii Isekai Boueki', vol, chp, frag=frag, postfix=postfix)
	if 'Sonohi Sekai ga Kawatta' in item['tags']:
		return buildReleaseMessage(item, 'Sonohi Sekai ga Kawatta', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractTheNamed(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTarableTranslations(item):
	'''
	# 'Tarable Translations'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractReadMeTranslations(item):
	'''
	# 'Read Me Translations'
	'''
	ttmp = item['title'].replace("My CEO Wife Chap.", "My CEO Wife Chapter")
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(ttmp)
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if item['title'].startswith("My CEO Wife Chap. "):
		return buildReleaseMessage(item, 'Wo De Meinu Zongcai Laopo', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractTheAsianCult(item):
	'''
	# 'The Asian Cult'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractPolyphonicStoryTranslationGroup(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractPridesFamiliarsMaidens(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTheMustangTranslator(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'The Six Immortals' in item['tags']:
		return buildReleaseMessage(item, 'The Six Immortals', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractPopsiclete(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTurtleandHareTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Time (对的时间对的人)' in item['title'] or 'Time (对的时间对的人)' in item['tags']:
		return buildReleaseMessage(item, 'Time', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractSaberTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractRomanticDreamersSanctuary(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTLSyosetsu(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if item['title'].lower().strip().startswith('defiled hero chapter'):
		return buildReleaseMessage(item, 'Defiled Hero', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractQualideaofScumandaGoldCoin(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractSoltarination(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractPlainlyBored(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Empress with no Virtue'.lower() in item['title'].lower():
		return buildReleaseMessage(item, 'Empress with no Virtue', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractTheDefendTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractSlimeLv1(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractUniversesWithMeaning(item):
	'''

	'''
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

def  extractOtomeRevolution(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractSleepyTranslations(item):
	'''
	# 'Sleepy Translations'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTheIronTeeth(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractUndecentTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTenThousandHeavenControllingSword(item):
	'''
	# 'Ten Thousand Heaven Controlling Sword'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTaptrans(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractRidwanTrans(item):
	'''
	# 'RidwanTrans'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Isekai Meikyuu no Saishinbu wo Mezasou' in item['title']:
		extract = re.search(r'Chapter (\d+)\-(\d+)', item['title'], re.IGNORECASE)
		if extract and not frag:
			chp  = int(extract.group(1))
			frag = int(extract.group(2))
		return buildReleaseMessage(item, 'Isekai Meikyuu no Saishinbu wo Mezasou', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractOyasumiReads(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractUDonateWeTranslate(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'ATG' in item['tags'] or ('Against the Gods' in item['title'] and 'Chapter' in item['title']):
		return buildReleaseMessage(item, 'Against the Gods', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractPiggyBottleTranslations(item):
	'''
	#'PiggyBottle Translations'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if item['title'].lower().startswith('beseech the devil'):
		return buildReleaseMessage(item, 'Beseech the Devil', vol, chp, frag=frag, postfix=postfix)
	return False


def  extractRumanshisLair(item):
	'''

	'''
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

def  extractSpiritualTranscription(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False

	if 'TEO' in item['tags'] or 'The Empyrean Overlord' in item['tags']:
		return buildReleaseMessage(item, 'The Empyrean Overlord', vol, chp, frag=frag, postfix=postfix)


	return False

def  extractPaztok(item):
	'''

	'''
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

def  extractTranslationTreasureBox(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractRedLanternArchives(item):
	'''
	# 'Red Lantern Archives'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Outaishihi ni Nante Naritakunai!!' in item['tags']:
		return buildReleaseMessage(item, 'Outaishihi ni Nante Naritakunai!!', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractTranslatingForYourPleasure(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if "The Inverted Dragon's Scale" in item['tags']:
		return buildReleaseMessage(item, "The Inverted Dragon's Scale", vol, chp, frag=frag, postfix=postfix)
	return False

def  extractSETSUNA86BLOG(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTryTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False



def  extractTrinityArchive(item):
	'''
	# 'Trinity Archive'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Summoned Slaughterer' in item['tags']:
		return buildReleaseMessage(item, 'Summoned Slaughterer', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractPielordTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTwelveMonthsofMay(item):
	'''
	# 'Twelve Months of May'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'My Mister Ostrich' in item['tags'] and 'English translation' in item['tags']:
		return buildReleaseMessage(item, 'Wo De Tuo Niao Xian Sheng', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractUkel2x(item):
	'''
	#'Ukel2x'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if item['title'].lower().startswith('volume'):
		return buildReleaseMessage(item, 'Kokugensou wo Item Cheat de Ikinuku', vol, chp, frag=frag, postfix=postfix)
	return False


def  extractRootOfEvil(item):
	'''
	# 'Root of Evil'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractStellarTransformationCon(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractUnnamedtranslations(item):
	'''
	# 'unnamedtranslations.blogspot.com'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTusTrans(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractTumbleIntoFantasy(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractQualiTeaTranslations(item):
	'''
	# 'QualiTeaTranslations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False

	if 'Harry Potter and the Rise of the Ordinary Person' in item['tags']:
		return None

	if 'Romance of Dragons and Snakes' in item['tags']:
		return buildReleaseMessage(item, 'Romance of Dragons and Snakes', vol, chp, frag=frag, postfix=postfix)
	return False


####################################################################################################################################################
#
####################################################################################################################################################

def  extractSolstar24(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'jin xiu wei yang' in item['tags']:
		return buildReleaseMessage(item, 'Jin Xiu Wei Yang', vol, chp, frag=frag, postfix=postfix)
	if 'dao qing' in item['tags']:
		return buildReleaseMessage(item, 'Dao Qing', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractSloth(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def  extractUnlimitedNovelFailures(item):
	'''
	# 'Unlimited Novel Failures'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False

def extractRinkageTranslation(item):
	'''
	'Rinkage Translation'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'Netooku Otoko no Tanoshii Isekai Boueki' in item['tags']:
		return buildReleaseMessage(item, 'Netooku Otoko no Tanoshii Isekai Boueki', vol, chp, frag=frag, postfix=postfix)
	if 'Atelier Tanaka' in item['tags']:
		return buildReleaseMessage(item, 'Atelier Tanaka', vol, chp, frag=frag, postfix=postfix)
	if 'Din No Monshou' in item['tags']:
		return buildReleaseMessage(item, 'Din No Monshou', vol, chp, frag=frag, postfix=postfix)
	return False
def extractSelkinNovel(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	return False
def extractStartlingSurprisesAtEveryStep(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return False
	if 'bu bu jing xin' in item['tags']:
		return buildReleaseMessage(item, 'Bu Bu Jing Xin', vol, chp, frag=frag, postfix=postfix)
	return False
