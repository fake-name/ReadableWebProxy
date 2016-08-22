
# pylint: disable=C0112,R0911,R0912,W0612

from WebMirror.OutputFilters.util.MessageConstructors import buildReleaseMessage
from WebMirror.OutputFilters.util.TitleParsers import extractChapterVolFragment
from WebMirror.OutputFilters.util.TitleParsers import extractVolChapterFragmentPostfix

import re

####################################################################################################################################################
def extractYoraikun(item):
	'''
	# Yoraikun
	'''

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
def extractWuxiaworld(item):
	'''
	# Wuxiaworld

	'''
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
	if 'Gate of Revelation' in item['tags']:
		return buildReleaseMessage(item, 'The Gate of Revelation', vol, chp, frag=frag)
	if 'Upgrade Specialist in Another World' in item['tags']:
		return buildReleaseMessage(item, 'Upgrade Specialist in Another World', vol, chp, frag=frag)
	if 'Renegade Immortal' in item['tags']:
		return buildReleaseMessage(item, 'Renegade Immortal', vol, chp, frag=frag)
	if 'Sovereign of the Three Realms' in item['tags']:
		return buildReleaseMessage(item, 'Sovereign of the Three Realms', vol, chp, frag=frag)
	if 'Terror Infinity' in item['tags']:
		return buildReleaseMessage(item, 'Terror Infinity', vol, chp, frag=frag)
	if 'Warlock of the Magus World' in item['tags']:
		return buildReleaseMessage(item, 'Warlock of the Magus World', vol, chp, frag=frag)
	if 'Spirit Realm' in item['tags']:
		return buildReleaseMessage(item, 'Spirit Realm', vol, chp, frag=frag)

	return False




####################################################################################################################################################
def extractZiruTranslations(item):
	'''
	# Ziru's Musings | Translations~

	'''
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
def extractVoidTranslations(item):
	'''
	# Void Translations

	'''
	chp, vol, dummy_frag = extractChapterVolFragment(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	match = re.search(r'^Xian Ni Chapter \d+ ?[\-–]? ?(.*)$', item['title'])
	if match:
		return buildReleaseMessage(item, 'Xian Ni', vol, chp, postfix=match.group(1))

	return False




def extractXCrossJ(item):
	'''

	'''
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

####################################################################################################################################################
def extractWuxiaTranslations(item):
	'''
	# Wuxia Translations

	'''
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
def extract1HP(item):
	'''
	# 1HP

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Route to almightyness from 1HP' in item['title'] and (chp or vol):
		return buildReleaseMessage(item, 'HP1 kara Hajimeru Isekai Musou', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractWatermelons(item):
	'''
	# World of Watermelons

	'''
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
def extractWCCTranslation(item):
	'''
	# WCC Translation

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if "chapter" in item['title'].lower():
		if ":" in item['title']:
			postfix = item['title'].split(":", 1)[-1]
		return buildReleaseMessage(item, 'World Customize Creator', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# 'yukkuri-literature-service'
####################################################################################################################################################
def extractYukkuri(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if '10 nen goshi no HikiNEET o Yamete Gaishutsushitara Jitaku goto Isekai ni Ten’ishiteta' in item['tags'] or \
		 'When I was going out from my house to stop become a Hiki-NEET after 10 years I was transported to another world' in item['tags']:
		return buildReleaseMessage(item, '10 nen goshi no HikiNEET o Yamete Gaishutsushitara Jitaku goto Isekai ni Ten’ishiteta', vol, chp, frag=frag, postfix=postfix)
	elif 'Takarakuji de 40 Oku Atattanda kedo Isekai ni Ijuusuru' in item['tags'] or \
		'Takarakuji de 40 Oku Atattanda kedo Isekai ni Ijuusuru.' in item['title']:
		return buildReleaseMessage(item, 'Takarakuji de 40 Oku Atattanda kedo Isekai ni Ijuusuru', vol, chp, frag=frag, postfix=postfix)
	elif 'Tenseisha wa Cheat o Nozomanai' in item['tags']:
		return buildReleaseMessage(item, 'Tenseisha wa Cheat o Nozomanai', vol, chp, frag=frag, postfix=postfix)
	elif 'Genjitsushugisha no Oukoku Kaizouki' in item['tags'] or item['title'].startswith("Genjitsushugisha no Oukoku Kaizouki"):
		return buildReleaseMessage(item, 'Genjitsushugisha no Oukoku Kaizouki', vol, chp, frag=frag, postfix=postfix)
	elif 'I Won 4 Billion in a Lottery But I Went to Another World' in item['tags']:
		return buildReleaseMessage(item, 'Takarakuji de 40 Oku Atattanda kedo Isekai ni Ijuusuru', vol, chp, frag=frag, postfix=postfix)
	elif  'The Curious Girl and The Traveler' in item['tags']:
		return buildReleaseMessage(item,  'The Curious Girl and The Traveler', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	elif  'Yukkuri Oniisan' in item['tags']:
		return buildReleaseMessage(item,  'Yukkuri Oniisan', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	elif  'The Valtras Myth' in item['tags']:
		return buildReleaseMessage(item,  'The Valtras Myth', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False


####################################################################################################################################################
#
####################################################################################################################################################
def extract87Percent(item):
	'''

	'''
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
def extractWuxiaSociety(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'The Heaven Sword and Dragon Sabre' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'The Heaven Sword and Dragon Sabre', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWuxiaHeroes(item):
	'''

	'''
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
def extractYoujinsite(item):
	'''

	'''
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
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'The Other World Dining Hall' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'The Other World Dining Hall', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractZSW(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Shen Mu' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Shen Mu', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractXantAndMinions(item):
	'''

	'''
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


	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWatDaMeow(item):
	'''

	'''

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
def extractWolfieTranslation(item):
	'''

	'''
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
def extractVerathragana(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if "Chapter" in item['title']:
		return buildReleaseMessage(item, 'The Prince Of Nilfheim', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWitchLife(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Witch Life' in item['tags']:
		return buildReleaseMessage(item, 'Witch Life', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWalkingTheStorm(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	return buildReleaseMessage(item, "Joy of life", vol, chp, frag=frag, postfix=postfix)


####################################################################################################################################################
#
####################################################################################################################################################
def extractWebNovelJapaneseTranslation(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Kizoku Yamemasu Shomin ni Narimasu' in item['tags']:
		return buildReleaseMessage(item, 'Kizoku Yamemasu Shomin ni Narimasu', vol, chp, frag=frag, postfix=postfix)

	return False








def  extractWeleTranslation(item):
	'''

	'''
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

def  extractWalkTheJiangHu(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'TTNH Chapter' in item['title']:
		return buildReleaseMessage(item, "Transcending the Nine Heavens", vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractYiYueTranslation(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractZxzxzxsBlog(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def  extract一期一会万歳(item):
	'''
	# '一期一会, 万歳!'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def  extractWhenTheHuntingPartyCame(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractXiaowen206sBlog(item):
	'''
	# "Xiaowen206's Blog"
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractWhiteTigerTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if item['title'].lower().startswith('mp volume'):
		return buildReleaseMessage(item, 'Martial Peak', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('ipash chapter'):
		return buildReleaseMessage(item, 'Martial Peak', vol, chp, frag=frag, postfix=postfix)

	return False

def  extractWhiteNightSite(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'What Came to Mind During My Third Time in Another World Was to for Now, Get Naked.' in item['tags']:
		return buildReleaseMessage(item, 'What Came to Mind During My Third Time in Another World Was to for Now, Get Naked.', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractZombieKnight(item):
	'''

	'''
	titleconcat = " ".join(item['tags']) + item['title']
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(titleconcat)
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	return buildReleaseMessage(item, 'The Zombie Knight', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

####################################################################################################################################################
#
####################################################################################################################################################

def  extractWuxiwish(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractWIP(item):
	'''

	'''
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

def  extractZenTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractWorldofSummie(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractWizThiefsNovels(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'My immortality It’s in a Death game' in item['title']:
		return buildReleaseMessage(item, 'My immortality It\'s in a Death game', vol, chp, frag=frag, postfix=postfix)
	if 'Thanks to a different world reincarnation' in item['title']:
		return buildReleaseMessage(item, 'Thanks to a different world reincarnation', vol, chp, frag=frag, postfix=postfix)
	if 'Grave “Z”' in item['title']:
		return buildReleaseMessage(item, 'Grave "Z"', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractVillageTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractWuxiaTranslators(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'World Defying Dan God' in item['tags']:
		return buildReleaseMessage(item, 'World Defying Dan God', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractWillfulCasual(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Chu Wang Fei' in item['tags']:
		return buildReleaseMessage(item, "Chu Wang Fei", vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractVolareTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Great Demon King' in item['tags']:
		return buildReleaseMessage(item, 'Great Demon King', vol, chp, frag=frag, postfix=postfix)
	if 'Sovereign of the Three Realms' in item['tags']:
		return buildReleaseMessage(item, 'Sovereign of the Three Realms', vol, chp, frag=frag, postfix=postfix)
	if 'Age of Lazurite' in item['tags']:
		return buildReleaseMessage(item, 'Age of Lazurite, Tower of Glass', vol, chp, frag=frag, postfix=postfix)
	if 'Apartment from Hell' in item['tags']:
		return buildReleaseMessage(item, "Apartment from Hell", vol, chp, frag=frag, postfix=postfix)
	if 'Celestial Employee' in item['tags']:
		return buildReleaseMessage(item, "Celestial Employee", vol, chp, frag=frag, postfix=postfix)
	if 'Cultivation Chat Group' in item['tags']:
		return buildReleaseMessage(item, "Cultivation Chat Group", vol, chp, frag=frag, postfix=postfix)
	if 'Falling Dreams of Fang Hua' in item['tags']:
		return buildReleaseMessage(item, "Falling Dreams of Fang Hua", vol, chp, frag=frag, postfix=postfix)
	if 'My Wife is a Beautiful CEO' in item['tags']:
		return buildReleaseMessage(item, "My Wife is a Beautiful CEO", vol, chp, frag=frag, postfix=postfix)
	if 'Release that Witch' in item['tags']:
		return buildReleaseMessage(item, "Release that Witch", vol, chp, frag=frag, postfix=postfix)
	if 'Sword Spirit' in item['tags']:
		return buildReleaseMessage(item, "Sword Spirit", vol, chp, frag=frag, postfix=postfix)
	if "Demon Wang's Favorite Fei" in item['tags']:
		return buildReleaseMessage(item, "Demon Wang's Golden Favorite Fei", vol, chp, frag=frag, postfix=postfix)
	if 'True Cultivators' in item['tags']:
		return buildReleaseMessage(item, 'The Strong, The Few, True Cultivators on Campus', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractZeonic(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extract天才創造すなわち百合(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractWhimsicalLand(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extract12Superlatives(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractWeavingstoriesandbuildingcastlesintheclouds(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractWelcomeToTheUnderdark(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extract輝く世界(item):
	'''
	# '輝く世界'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def  extractYoutsubasilversBlog(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractWatermelonHelmets(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Dragon Life' in item['tags'] or 'Dragon Life: Chapter' in item['title']:
		return buildReleaseMessage(item, 'Dragon Life', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractXantDoesStuffAndThings(item):
	'''
	# 'Xant Does Stuff and Things'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractXantbos(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractWordofCraft(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Toaru Ossan no VRMMO katsudouki' in item['tags']:
		return buildReleaseMessage(item, 'Toaru Ossan no VRMMO katsudouki', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractWLTranslations(item):
	'''
	# 'WL Translations'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Chapter Releases' in item['tags'] and ('OSI' in item['tags'] or item['title'].startswith("OSI Chapter")):
		return buildReleaseMessage(item, 'One Sword to Immortality', vol, chp, frag=frag, postfix=postfix)
	return False

def  extract睡眠中毒(item):
	'''
	# '睡眠中毒'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def  extractYoukoAdvent(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	# No chapter numbers in titles. Arrrgh

	return False

def  extractWormACompleteWebSerial(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extract7DaysTrial(item):
	'''
	#'7 Days Trial'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'content' in item['tags']:
		return buildReleaseMessage(item, 'War of the Supreme', vol, chp, frag=frag, postfix=postfix)
	return False


def  extract77Novel(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractWishUponAHope(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractWumsTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractXianxiaTales(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractYamiTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractZeroTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractV7Silent(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

	if 'The Demon Queen is My Fiancée!' in item['tags']:
		return buildReleaseMessage(item, 'The Demon Queen is My Fiancée!', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Getcha Skills' in item['tags']:
		return buildReleaseMessage(item, 'Getcha Skills', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False


def extractWarriorWriting(item):
	"""
	Warrior Writing
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractWigglyTranslation(item):
	"""
	Wiggly Translation
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if item['title'].startswith("Man Huang Feng Bao: "):
		return buildReleaseMessage(item, 'Man Huang Feng Bao', vol, chp, frag=frag, postfix=postfix)
	return False
def extractWorldofHope(item):
	"""
	World of Hope
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractWorldTurtleTranslations(item):
	"""
	World Turtle Translations
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractYasashiHonyaku(item):
	"""
	Yasashi Honyaku
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractYeagdrasil(item):
	"""
	Yeagdrasil
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractYourMajestyPleaseCalmDown(item):
	"""
	Your Majesty Please Calm Down
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extract書櫃(item):
	"""
	『書櫃』
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extract閒人ONLINE(item):
	"""
	閒人 • O N L I N E
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Great Tang Idyll' in item['tags']:
		return buildReleaseMessage(item, 'Great Tang Idyll', vol, chp, frag=frag, postfix=postfix)
	return False

