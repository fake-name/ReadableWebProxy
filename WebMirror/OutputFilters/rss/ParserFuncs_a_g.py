
# pylint: disable=C0112,R0911,R0912,W0612

from WebMirror.OutputFilters.util.MessageConstructors import buildReleaseMessage
from WebMirror.OutputFilters.util.TitleParsers import extractChapterVol
from WebMirror.OutputFilters.util.TitleParsers import extractChapterVolFragment
from WebMirror.OutputFilters.util.TitleParsers import extractVolChapterFragmentPostfix

import re

####################################################################################################################################################
def extractFlowerBridgeToo(item):
	'''
	# FlowerBridgeToo

	'''
	# Seriously, you were too lazy to type out the *tags*?
	# You only have to do it ONCE!
	# if 'MGA Translation' in item['tags']:
	# 	chp, vol = extractChapterVol(item['title'])
	# 	# Also called "Martial God Asura"
	# 	return buildReleaseMessage(item, 'Xiuluo Wushen', vol, chp)
	# elif 'Xian Ni' in item['tags'] or 'Xian Ni Translation' in item['tags']:
	# 	chp, vol = extractChapterVol(item['title'])
	# 	return buildReleaseMessage(item, 'Xian Ni', vol, chp)
	# elif 'JMG Translation' in item['tags']:  # Series was dropped, have lots of old releases
	# 	chp, vol = extractChapterVol(item['title'])
	# 	return buildReleaseMessage(item, 'Shaonian Yixian', vol, chp)

	# Return none since they've apparently migrated to releasing only on wuxiaworld
	return None


####################################################################################################################################################
def extractGravityTranslation(item):
	'''
	# Gravity Translation
	also
	# Gravity Tales
	# GravityTales

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	ltags = [tmp.lower().replace("’", "'") for tmp in item['tags']]

	if 'announcement' in ltags:
		return None

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
	if 'terror paradise' in ltags:
		return buildReleaseMessage(item, 'Terror Paradise', vol, chp, frag=frag, postfix=postfix)
	if 'the divine elements' in ltags or 'the divine element' in ltags:
		return buildReleaseMessage(item, 'The Divine Elements', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'cult of the sacred runes' in ltags or item['title'].startswith("Cult of the Sacred Runes"):
		return buildReleaseMessage(item, 'Cult of the Sacred Runes', vol, chp, frag=frag, postfix=postfix)
	if 'Blood Hourglass' in item['title']:
		return buildReleaseMessage(item, 'Blood Hourglass', vol, chp, frag=frag, postfix=postfix)
	if "A Dragon's Curiosity" in item['tags']:
		return buildReleaseMessage(item, "A Dragon's Curiosity", vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if (
			'RMJI' in item['tags'] or
			(item['title'].startswith('RMJI') and 'Release' in item['title']) or
			item['title'].lower().startswith("a record of a mortal’s journey to immortality – chapter")
		):
		return buildReleaseMessage(item, "A Record of A Mortal's Journey to Immortality", vol, chp, frag=frag, postfix=postfix)
	if 'The Nine Cauldrons' in item['tags'] or item['title'].startswith('The Nine Cauldrons Chapter') or item['title'].startswith('The Nine Cauldrons book'):
		return buildReleaseMessage(item, 'The Nine Cauldrons', vol, chp, frag=frag, postfix=postfix)
	if 'The Trembling World' in item['tags']:
		return buildReleaseMessage(item, 'The Trembling World', vol, chp, frag=frag, postfix=postfix)
	if 'Ancient Strengthening Technique' in item['tags'] or item['title'].lower().startswith("ancient strengthening technique: chapter"):
		return buildReleaseMessage(item, 'Ancient Strengthening Technique', vol, chp, frag=frag, postfix=postfix)
	if 'Nine Heavenly Thunder Manual' in item['tags']:
		return buildReleaseMessage(item, 'Nine Heavenly Thunder Manual', vol, chp, frag=frag, postfix=postfix)
	if 'a record of a mortal\'s journey to immortality' in ltags or item['title'].startswith('RMJI '):
		return buildReleaseMessage(item, 'A Record of a Mortal\'s Journey to Immortality', vol, chp, frag=frag, postfix=postfix)
	if 'martial world' in ltags or item['title'].startswith('MW Chapter') or item['title'].startswith('Martial World Chapter'):
		return buildReleaseMessage(item, 'Martial World', vol, chp, frag=frag, postfix=postfix)
	if 'ancient godly monarch' in ltags:
		return buildReleaseMessage(item, 'Ancient Godly Monarch', vol, chp, frag=frag, postfix=postfix)
	if "i'm really a superstar" in ltags or item['title'].lower().startswith("i’m really a superstar chapter"):
		return buildReleaseMessage(item, "I'm Really a Superstar", vol, chp, frag=frag, postfix=postfix)
	if "The Beginning After the End" in item['tags'] or item['title'].lower().startswith('the beginning after the end'):
		return buildReleaseMessage(item, "The Beginning After the End", vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	if item['title'].lower().startswith('chaotic lightning cultivation chapter'):
		return buildReleaseMessage(item, 'Chaotic Lightning Cultivation', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('a dragon’s curiosity chapter'):
		return buildReleaseMessage(item, 'A Dragon’s Curiosity', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('paradise of the demons and gods chapter'):
		return buildReleaseMessage(item, 'Paradise of the Demons and Gods', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('lord xue ying chapters'):
		return buildReleaseMessage(item, 'Lord Xue Ying', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('chaotic sword god chapter'):
		return buildReleaseMessage(item, 'Chaotic Sword God', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('era of shamans chapter'):
		return buildReleaseMessage(item, 'Era of Shamans', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('jiu shen chapter'):
		return buildReleaseMessage(item, 'Jiu Shen', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('true martial world chapter'):
		return buildReleaseMessage(item, 'True Martial World', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('reincarnator'):
		return buildReleaseMessage(item, 'Reincarnator', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith("king of gods – "):
		return buildReleaseMessage(item, "King of Gods", vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('iras'):
		return buildReleaseMessage(item, 'I’m Really a Superstar', vol, chp, frag=frag, postfix=postfix)
	if 'chaotic lightning cultivation' in ltags:
		return buildReleaseMessage(item, 'Chaotic Lightning Cultivation', vol, chp, frag=frag, postfix=postfix)
	if "the king's avatar" in ltags:
		return buildReleaseMessage(item, "The King's Avatar", vol, chp, frag=frag, postfix=postfix)
	if 'ze tian ji' in ltags or 'way of choices' in ltags:
		return buildReleaseMessage(item, 'Ze Tian Ji', vol, chp, frag=frag, postfix=postfix)

	if 'str' in ltags:
		return buildReleaseMessage(item, 'Sovereign of the Three Realms', vol, chp, frag=frag, postfix=postfix)
	if 'dimensional sovereign' in ltags:
		return buildReleaseMessage(item, 'Dimensional Sovereign', vol, chp, frag=frag, postfix=postfix)
	if 'dungeon hunter' in ltags:
		return buildReleaseMessage(item, 'Dungeon Hunter', vol, chp, frag=frag, postfix=postfix)
	if 'king of gods'  in ltags:
		return buildReleaseMessage(item, 'King of Gods' , vol, chp, frag=frag, postfix=postfix)
	if 'overthrowing fate' in ltags:
		return buildReleaseMessage(item, 'Overthrowing Fate', vol, chp, frag=frag, postfix=postfix)
	if 'paradise of the demons and gods' in ltags or item['title'].lower().startswith("Paradise of the Demons and Gods "):
		return buildReleaseMessage(item, 'Paradise of the Demons and Gods', vol, chp, frag=frag, postfix=postfix)
	if 'reincarnator' in ltags:
		return buildReleaseMessage(item, 'Reincarnator', vol, chp, frag=frag, postfix=postfix)
	if 'the experimental log of the crazy lich' in ltags or item['title'].lower().startswith("the experimental log of the crazy lich chapter"):
		return buildReleaseMessage(item, 'The Experimental Log of the Crazy Lich', vol, chp, frag=frag, postfix=postfix)
	if 'king of gods' in ltags:
		return buildReleaseMessage(item, 'King of Gods', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith("Blue Phoenix – Chapter"):
		return buildReleaseMessage(item, 'Blue Phoenix', vol, chp, frag=frag, postfix=postfix, tl_type='oel')


	return False



####################################################################################################################################################
def extractBlueSilverTranslations(item):
	'''
	# Blue Silver Translations

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

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
def extractAlyschuCo(item):
	'''
	# Alyschu & Co

	'''
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
def extractCalicoxTabby(item):
	'''
	# Calico x Tabby

	'''
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Meow Meow Meow' in item['tags']:
		return buildReleaseMessage(item, 'Meow Meow Meow', vol, chp, frag=frag)

	return False



####################################################################################################################################################
def extractDarkFish(item):
	'''
	# DarkFish Translations

	'''
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'She Professed Herself The Pupil Of The Wise Man'.lower() in item['title'].lower() or \
		'She Professed Herself The Pupil Of The Wise Man'.lower() in [tmp.lower() for tmp in item['tags']]:
		return buildReleaseMessage(item, 'Kenja no Deshi wo Nanoru Kenja', vol, chp, frag=frag)
	# if 'Majin Tenseiki' in item['title']:
	return False


####################################################################################################################################################
def extractAzureSky(item):
	'''
	# extractAzureSky

	'''
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
def extractClicky(item):
	'''
	# Clicky Click Translation

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'MEMORIZE' in item['tags']:
		return buildReleaseMessage(item, 'MEMORIZE', vol, chp, frag=frag, postfix=postfix)
	if 'R8CM' in item['tags']:
		return buildReleaseMessage(item, 'Revolution of the 8th Class Mage', vol, chp, frag=frag, postfix=postfix)
	if 'Dusk Howler' in item['tags']:
		return buildReleaseMessage(item, 'Dusk Howler', vol, chp, frag=frag, postfix=postfix)
	if 'Legendary Moonlight Sculptor' in item['tags'] and any(['Volume' in tag for tag in item['tags']]):
		return buildReleaseMessage(item, 'Legendary Moonlight Sculptor', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractDefiring(item):
	'''
	# Defiring

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'World teacher'.lower() in item['title'].lower() or 'World teacher' in item['tags']:
		return buildReleaseMessage(item, 'World teacher', vol, chp, frag=frag, postfix=postfix)
	if 'Shinka no Mi' in item['title']:
		return buildReleaseMessage(item, 'Shinka no Mi', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractFanatical(item):
	'''
	# Fanatical Translations

	'''
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
	if "Together Forever" in item['tags']:
		return buildReleaseMessage(item, "Together Forever", vol, chp, frag=frag, postfix=postfix)
	if 'Your Humble Servant is Guilty!' in item['tags']:
		return buildReleaseMessage(item, 'Your Humble Servant is Guilty!', vol, chp, frag=frag, postfix=postfix)
	if 'Stewed Squid with Honey' in item['tags']:
		return buildReleaseMessage(item, 'Stewed Squid with Honey', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractGiraffe(item):
	'''
	# Giraffe Corps

	'''
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
def extractGuhehe(item):
	'''
	# guhehe.TRANSLATIONS

	'''
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
def extractGilaTranslation(item):
	'''
	# Gila Translation Monster

	'''
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
def extractAFlappyTeddyBird(item):
	'''
	# A Flappy Teddy Bird

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'The Black Knight who was stronger than even the Hero' in item['title']:
		return buildReleaseMessage(item, 'The Black Knight Who Was Stronger than Even the Hero', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
def extractBinggoCorp(item):
	'''
	# Binggo & Corp Translations

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Jiang Ye' in item['title'] and "Chapter" in item['title']:
		return buildReleaseMessage(item, 'Jiang Ye', vol, chp, frag=frag, postfix=postfix)
	if 'Ze Tian Ji' in item['title'] and "Chapter" in item['title']:
		return buildReleaseMessage(item, 'Ze Tian Ji', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
def extractArkMachineTranslations(item):
	'''
	# Ark Machine Translations

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'ark volume' in item['title'].lower():
		return buildReleaseMessage(item, 'Ark', vol, chp, frag=frag, postfix=postfix)

	if 'ark the legend volume' in item['title'].lower() or \
		'ATL' in item['tags']:
		return buildReleaseMessage(item, 'Ark The Legend', vol, chp, frag=frag, postfix=postfix)

	if 'lms volume' in item['title'].lower():
		return buildReleaseMessage(item, 'Legendary Moonlight Sculptor', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractAvert(item):
	'''
	# Avert Translations

	'''

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
def extractBinhjamin(item):
	'''
	# Binhjamin

	'''

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
def extractBureiDan(item):
	'''
	# Burei Dan Works

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Isekai Canceller' in item['tags'] and (chp or vol or frag or postfix):
		return buildReleaseMessage(item, 'Isekai Canceller', vol, chp, frag=frag, postfix=postfix)
	if 'Kenja ni Natta' in item['tags'] and (chp or vol or frag or postfix):
		return buildReleaseMessage(item, 'Kenja ni Natta', vol, chp, frag=frag, postfix=postfix)
	if 'Han-Ryuu Shoujo no Dorei Raifu' in item['tags'] and (chp or vol or frag or postfix):
		return buildReleaseMessage(item, 'Han-Ryuu Shoujo no Dorei Raifu', vol, chp, frag=frag, postfix=postfix)
	if 'To Aru Ninki Jikkou Player no VRMMO Funtou Ki' in item['tags'] and (chp or vol or frag or postfix):
		return buildReleaseMessage(item, 'To Aru Ninki Jikkou Player no VRMMO Funtou Ki', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
def extractErosWorkshop(item):
	'''
	# Eros Workshop

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Young God Divine Armaments' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Young God Divine Armaments', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractForgetfulDreamer(item):
	'''
	# Forgetful Dreamer

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'ヤンデレ系乙女ゲーの世界に転生してしまったようです' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'It seems like I got reincarnated into the world of a Yandere Otome game', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractFudgeTranslations(item):
	'''
	# Fudge Translations

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'SoE' in item['title'] and (chp or vol):
		return buildReleaseMessage(item, 'The Sword of Emperor', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith("Emperor of Solo Play Chapter") and (chp or vol):
		return buildReleaseMessage(item, 'Emperor of Solo Play', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractEnTruceTranslations(item):
	'''
	# EnTruce Translations

	'''
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
def extractClownTrans(item):
	'''
	# 'Translated by a Clown'

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Tensei Shitara Slime datta ken' in item['tags'] and chp:
		return buildReleaseMessage(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractAsherahBlue(item):
	'''
	# 'AsherahBlue's Notebook'

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Juvenile Medical God' in item['tags']:
		return buildReleaseMessage(item, 'Shaonian Yixian', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractAlcsel(item):
	'''
	# 'Alcsel Translations'

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'AR Chapter' in item['title']:
		return buildReleaseMessage(item, 'Assassin Reborn', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractGuroTranslation(item):
	'''
	# 'GuroTranslation'

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	ltags = [tmp.lower() for tmp in item['tags']]

	if 'tensei shitara slime datta ken' in ltags:
		return buildReleaseMessage(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)
	if '1000 nin no homunkurusu no shoujo tachi ni kakomarete isekai kenkoku' in ltags:
		return buildReleaseMessage(item, '1000 nin no Homunkurusu no Shoujo tachi ni Kakomarete Isekai Kenkoku', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractEnsjTranslations(item):
	'''
	# Ensj Translations

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'King Shura' in item['tags']:
		return buildReleaseMessage(item, 'King Shura', vol, chp, frag=frag, postfix=postfix)
	if 'The Record of a Thousand Lives' in item['tags']:
		return buildReleaseMessage(item, 'The Record of a Thousand Lives', vol, chp, frag=frag, postfix=postfix)
	if 'Running Away From The Hero!' in item['tags']:
		if not frag:
			match = re.search(r'\((\d+)\)', item['title'])
			if match:
				frag = int(match.group(1))

		return buildReleaseMessage(item, 'Running Away From The Hero!', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# B
def extractCeLn(item):
	'''

	####################################################################################################################################################
	'''
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
#
####################################################################################################################################################
def extractDreadfulDecoding(item):
	'''

	'''
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
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Because the world has changed into a death game is funny' in item['tags'] and (chp or vol or "Prologue" in postfix):
		return buildReleaseMessage(item, 'Sekai ga death game ni natta no de tanoshii desu', vol, chp, frag=frag, postfix=postfix)

	return False


####################################################################################################################################################
#
####################################################################################################################################################
def extractBakaDogeza(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if "chapter" in item['title'].lower() and (vol or chp):
		return buildReleaseMessage(item, 'Knights & Magic', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractCNovelProj(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Please Be More Serious' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Please Be More Serious', vol, chp, frag=frag, postfix=postfix)

	if 'Still Not Wanting to Forget' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Still Not Wanting to Forget', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractBeehugger(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Battle Emperor' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Battle Emperor', vol, chp, frag=frag, postfix=postfix)
	if 'Sword Spirit' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Sword Spirit', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractBuBuJingXinTrans(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'bu bu jing xin' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Bu Bu Jing Xin', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractEroLightNovelTranslations(item):
	'''

	'''
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
def extractA0132(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if chp or vol:
		return buildReleaseMessage(item, 'Terror Infinity', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractCircusTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'German Translation' in item['tags']:
		return None
	if 'Turkish Translation' in item['tags']:
		return None
	if 'Spanish translation' in item['tags']:
		return None

	if chp or vol:
		return buildReleaseMessage(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractDistractedTranslations(item):
	'''

	'''
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
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if chp:
		return buildReleaseMessage(item, "Forgotten Conqueror", vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractAzurro(item):
	'''

	'''
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
	if "The CEO's Pregnant Wife (总裁的孕妻)" in item['tags']:
		return buildReleaseMessage(item, "The CEO's Pregnant Wife", vol, chp, frag=frag, postfix=postfix)
	if 'The Wolf Husband and The Green Plum Wife (狼竹马与青梅妻)' in item['tags']:
		return buildReleaseMessage(item, 'The Wolf Husband and The Green Plum Wife', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractCloversNook(item):
	'''

	'''
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
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	return buildReleaseMessage(item, 'Douluo Dalu 2 - Jueshi Tangmen', vol, chp, frag=frag, postfix=postfix)


####################################################################################################################################################
#
####################################################################################################################################################
def extractDreamsOfJianghu(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False



	bad = [
			'pictures',
		]

	if any([tmp in item['tags'] for tmp in bad]):
		return None

	if 'TBVW' in item['tags']:
		return buildReleaseMessage(item, 'To Be A Virtuous Wife', vol, chp, frag=frag, postfix=postfix)
	if 'WC' in item['tags']:
		return buildReleaseMessage(item, 'World of Cultivation', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractDaoSeekerBlog(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Otherworldly Evil Monarch' in item['tags'] or 'Chapter' in item['title']:
		return buildReleaseMessage(item, 'Otherworldly Evil Monarch', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractCeruleonice(item):
	'''

	'''
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
def extractBeginningAfterTheEnd(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if "Chapter" in item['title']:
		return buildReleaseMessage(item, 'The Beginning After The End', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractBcat00(item):
	'''

	'''
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
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Xian Ni' in item['title']:
		return buildReleaseMessage(item, 'Xian Ni', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractCtrlAlcala(item):
	'''

	'''
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
def extractAnathema(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	return buildReleaseMessage(item, 'Anathema', vol, chp, frag=frag, postfix=postfix, tl_type='oel')


####################################################################################################################################################
#
####################################################################################################################################################
def extractDawningHowls(item):
	'''

	'''
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
def extractGoddessGrantMeaGirlfriend(item):
	'''

	'''
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
	'''

	'''

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
def extractChineseBLTranslations(item):
	'''

	'''
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
def extractDiwasteman(item):
	'''

	'''
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
def extractAndrew9495(item):
	'''

	'''
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
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Skill Taker' in item['tags'] or 'Skill Taker Ch' in item['title']:
		return buildReleaseMessage(item, 'Skill Taker’s World Domination ~ Building a Slave Harem from Scratch', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractCrystalRainDescends(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Honey Stewed Squid' in item['tags']:
		return buildReleaseMessage(item, 'Honey Stewed Squid', vol, chp, frag=frag, postfix=postfix)
	if 'Bloom' in item['tags']:
		return buildReleaseMessage(item, 'Bloom', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractFirebirdsNest(item):
	'''

	'''
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
def extractCasProjectSite(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	return buildReleaseMessage(item, "Era of Cultivation", vol, chp, frag=frag, postfix=postfix)


####################################################################################################################################################
#
####################################################################################################################################################
def extractFrostfire10(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	return buildReleaseMessage(item, "Overlord", vol, chp, frag=frag, postfix=postfix)



####################################################################################################################################################
#
####################################################################################################################################################
def extractGrimdarkZTranslations(item):
	'''
	# 'GrimdarkZ Translations'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

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
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if item['title'].startswith("Comment"):
		return None

	if 'The Man Picked up by the Gods' in item['tags']:
		return buildReleaseMessage(item, 'Kamitachi ni Hirowareta Otoko', vol, chp, frag=frag, postfix=postfix)
	if 'Goblin Kingdom' in item['tags']:
		return buildReleaseMessage(item, 'Goblin Kingdom', vol, chp, frag=frag, postfix=postfix)
	if 'The Man Picked up by the Gods -' in item['title']:
		return buildReleaseMessage(item, 'Kamitachi ni Hirowareta Otoko', vol, chp, frag=frag, postfix=postfix)
	if 'Goblin Kingdom -' in item['title']:
		return buildReleaseMessage(item, 'Goblin no Oukoku', vol, chp, frag=frag, postfix=postfix)
	if 'Growth Cheat' in item['tags']:
		return buildReleaseMessage(item, 'I\'ve Became Able to Do Anything With My Growth Cheat, but I Can\'t Seem to Get Out of Being Jobless', vol, chp, frag=frag, postfix=postfix)
	if 'Invincible Saint' in item['tags']:
		return buildReleaseMessage(item, 'Invincible Saint ~Salaryman, the Path I Walk to Survive in This Other World~', vol, chp, frag=frag, postfix=postfix)
	if 'I came back but the world is still a fantasy' in item['tags']:
		return buildReleaseMessage(item, 'Kaettekite mo Fantasy!?', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractDragomirCM(item):
	'''
	# DragomirCM

	'''
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






def  extractGrowWithMe(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'zui wu dao' in item['tags']:
		# These parts are either volumes or chapters
		vol, chp, frag = frag, chp, 0
		return buildReleaseMessage(item, 'Zui Wu Dao', vol, chp, frag=frag, postfix=postfix)

	if re.search(r'Your Highness[\W\-\. ]+I know my wrongs\.?', item['title'], re.IGNORECASE):
		return buildReleaseMessage(item, 'Your Highness, I Know My Wrongs', vol, chp, frag=frag, postfix=postfix)


	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractDHHTranslations(item):
	'''
	# 'DHH Translations'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if "god's left hand" in item['tags']:
		return buildReleaseMessage(item, "god's left hand", vol, chp, frag=frag, postfix=postfix)
	return False

def  extractEmruyshitTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractAquarilasScenario(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'In That Moment of Suffering' in item['tags']:
		return buildReleaseMessage(item, 'In That Moment of Suffering', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractCNovelTranlations(item):
	'''
	# 'C-Novel Tranlations…'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractEtheriaTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractBayabuscoTranslation(item):
	'''
	# 'Bayabusco Translation'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if "World Teacher".lower() in item['title'].lower():
		return buildReleaseMessage(item, "World Teacher", vol, chp, frag=frag, postfix=postfix)
	return False

def  extractChrononTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

	item['title'] = item['title'].replace("’", "")

	if "Weapons cheat".lower() in item['title'].lower():
		return buildReleaseMessage(item, "Modern weapons cheat in another world", vol, chp, frag=frag, postfix=postfix)
	if "Heavenly Tribulation".lower() in item['title'].lower():
		return buildReleaseMessage(item, "Heavenly Tribulation", vol, chp, frag=frag, postfix=postfix)
	if "I can speak".lower() in item['title'].lower():
		return buildReleaseMessage(item, "I Can Speak with Animals and Demons", vol, chp, frag=frag, postfix=postfix)
	if "I Bought a Girl".lower() in item['title'].lower():
		return buildReleaseMessage(item, "I Bought a Girl", vol, chp, frag=frag, postfix=postfix)
	if "Girl Corps".lower() in item['title'].lower():
		return buildReleaseMessage(item, "Girl Corps", vol, chp, frag=frag, postfix=postfix)
	if "Modern Weapons".lower() in item['title'].lower():
		return buildReleaseMessage(item, "Modern weapons cheat in another world", vol, chp, frag=frag, postfix=postfix)
	if "Upper World".lower() in item['title'].lower():
		return buildReleaseMessage(item, "Reincarnation ~ From the lower world to the upper world", vol, chp, frag=frag, postfix=postfix)
	if "I work as a healer".lower() in item['title'].lower():
		return buildReleaseMessage(item, "I Work As A Healer In Another World's Labyrinth City", vol, chp, frag=frag, postfix=postfix)

	return False

def  extractDailyDallying(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if "Conquering Hero's Heroines" in item['tags']:
		return buildReleaseMessage(item, 'Stealing Hero\'s Lovers', vol, chp, frag=frag, postfix=postfix)
	if 'Nidome no Yuusha' in item['tags']:
		return buildReleaseMessage(item, 'Nidome no Yuusha', vol, chp, frag=frag, postfix=postfix)
	if "Nobunaga's Imouto" in item['tags']:
		return buildReleaseMessage(item, "Nobunaga's Younger Sister is My Wife", vol, chp, frag=frag, postfix=postfix)
	return False

def  extractDistractedChinese(item):
	'''
	# 'Distracted Chinese'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractAnonEmpire(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractECWebnovel(item):
	'''

	'''
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

def  extractDorayakiz(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractEccentricTranslations(item):
	'''

	'''
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
	if 'SPO' in item['tags']:
		return buildReleaseMessage(item, 'Single Player Only', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractDeweyNightUnrolls(item):
	'''

	'''
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

def  extractAquaScans(item):
	'''

	'''
	if 'Manga' in item['tags']:
		return None

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractEternalpath(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractBruinTranslation(item):
	'''
	# 'Bruin Translation'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if not item['title']:
		return False
	if item['tags'] == ['Uncategorized'] and item['title'].startswith('Volume'):
		return buildReleaseMessage(item, 'Otherworldly Evil Monarch', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractBluefireTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractCaveScans(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractBooksMoviesAndBeyond(item):
	'''
	# 'Books Movies and Beyond'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractBlublub(item):
	'''
	# 'Blublub'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractfgiLaNTranslations(item):
	'''
	# 'fgiLaN translations'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'kimi no na wa' in item['tags']:
		return buildReleaseMessage(item, 'kimi no na wa', vol, chp, frag=frag, postfix=postfix)
	if 'shuumatsu nani shitemasu ka? isogashii desu ka? sukutte moratte ii desu ka?' in item['tags']:
		return buildReleaseMessage(item, 'shuumatsu nani shitemasu ka? isogashii desu ka? sukutte moratte ii desu ka?', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractDramasBooksTea(item):
	'''

	'''
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

def  extractGargoyleWebSerial(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractDescentSubs(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractGaochaoTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Otherworldly Evil Monarch' in item['tags']:
		return buildReleaseMessage(item, 'Otherworldly Evil Monarch', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractDOWsTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractDragonMT(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Dragon Life' in item['tags']:
		return buildReleaseMessage(item, 'Dragon Life', vol, chp, frag=frag, postfix=postfix)

	return False



def  extractCNovels2C(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractBathrobeKnight(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if not postfix and '-' in item['title']:
		postfix = item['title'].split("-")[-1]
	return buildReleaseMessage(item, 'The Bathrobe Knight', vol, chp, frag=frag, postfix=postfix, tl_type='oel')


####################################################################################################################################################
#
####################################################################################################################################################

def  extractEndKun(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractCosmicTranslation(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractBakaPervert(item):
	'''
	# 'Baka Pervert'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if "antihero" in item['title'].lower():
		return buildReleaseMessage(item, 'Ultimate Antihero', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('hxh'):
		return buildReleaseMessage(item, 'Hybrid x Heart Magis Academy Ataraxia', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('magika vol'):
		return buildReleaseMessage(item, 'Magika No Kenshi To Shoukan Maou', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractAsd398(item):
	'''
	# 'asd398'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if "Don't tell me this is the true history of the Three Kingdoms!" in item['tags']:
		return buildReleaseMessage(item, "Don't tell me this is the true history of the Three Kingdoms!", vol, chp, frag=frag, postfix=postfix)
	if 'Leading an Explosive Revolution in Another World!' in item['tags']:
		return buildReleaseMessage(item, 'Leading an Explosive Revolution in Another World!', vol, chp, frag=frag, postfix=postfix)
	if 'No Battle No Life' in item['tags']:
		return buildReleaseMessage(item, 'No Battle No Life', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractCrazyForHENovels(item):
	'''

	'''
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

def  extractAngry(item):
	'''
	# 'ヾ(。￣□￣)ﾂ'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def  extractChubbyCheeks(item):
	'''
	# 'ChubbyCheeks'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'A Mistaken Marriage Match: Mysteries in the Imperial Harem' in item['tags']:
		return buildReleaseMessage(item, 'A Mistaken Marriage Match: Mysteries in the Imperial Harem', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractDynamisGaul(item):
	'''

	'''
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

def  extractEyeofAdventure(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractAyaxWorld(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractFalinmer(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

	match = re.search(r'(\d+)\-(\d+)', item['title'])
	if not vol and match:
		vol = match.group(1)
		chp = match.group(2)

	if item['title'].lower().startswith("mcm") and not "raw" in item['title'].lower():
		return buildReleaseMessage(item, 'Magi Craft Meister', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractBearBearTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractBeRsErkTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractDefansTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractCrappyMachineTranslation(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Blade Online' in item['tags']:
		return buildReleaseMessage(item, 'Blade Online', vol, chp, frag=frag, postfix=postfix)
	if "Another World's Savior" in item['tags']:
		return buildReleaseMessage(item, "Another World's Savior", vol, chp, frag=frag, postfix=postfix)
	return False

def  extractAGreyWorld(item):
	'''
	# 'A Grey World'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractChronaZero(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'tensei jinsei' in item['tags']:
		return buildReleaseMessage(item, 'Cheat Aru Kedo Mattari Kurashitai《Tensei Jinsei o Tanoshimou!》', vol, chp, frag=frag, postfix=postfix)
	if 'Level up by walking' in item['tags']:
		return buildReleaseMessage(item, 'Level up By Walking: in 10 thousand steps I will be level 10000', vol, chp, frag=frag, postfix=postfix)

	if 'When you actually went to be another world not as the Hero but as the Slave and then...' in item['tags']:
		return buildReleaseMessage(item, 'When you actually went to be another world not as the Hero but as the Slave and then...', vol, chp, frag=frag, postfix=postfix)

	return False

def  extractFightingDreamersScanlations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Light Novel' in item['tags'] and 'Slayers Special' in item['tags']:
		return buildReleaseMessage(item, 'Slayers Special', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractDarkTranslations(item):
	'''

	'''
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

def  extractEZTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractFlickerHero(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractBallKickingGangBoss(item):
	'''
	# "'Ball'-Kicking Gang Boss"
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'jinsei' in item['tags']:
		return buildReleaseMessage(item, "I'll Live My Second Life!", vol, chp, frag=frag, postfix=postfix)
	return False

def  extractAPearlyView(item):
	'''

	'''
	if 'K-Drama Recaps' in item['tags']:
		return None
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractAoriTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'WT' in item['tags']:
		return buildReleaseMessage(item, "World Teacher - Different World Style Education Agent", vol, chp, frag=frag, postfix=postfix)
	if 'Lv2' in item['tags']:
		return buildReleaseMessage(item, "Ex-Hero Candidate's, Who Turned Out To Be A Cheat From Lv2, Laid-back Life In Another World", vol, chp, frag=frag, postfix=postfix)
	return False

def  extractCloudTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractDadIsHeroFanTranslations(item):
	'''
	# 'DadIsHero Fan Translations'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractDuranDaruTranslation(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractFungShen(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Shrouded' in item['tags']:
		return buildReleaseMessage(item, 'Shrouded', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractEpyonTranslations(item):
	'''

	'''
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

def  extractAliceTranslations(item):
	'''
	# 'Alice Translations'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractAdamantineDragonintheCrystalWorld(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

	if 'Crystal World' in item['tags']:
		return buildReleaseMessage(item, 'Adamantine Dragon in the Crystal World', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False

def  extractFakTranslations(item):
	'''
	# 'Fak Translations'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Shrouding the Heavens' in item['tags'] or 'STH' in item['tags']:
		return buildReleaseMessage(item, 'Shrouding the Heavens', vol, chp, frag=frag, postfix=postfix)
	if 'KGGD' in item['tags']:
		return buildReleaseMessage(item, 'Killing Grounds of Gods and Devils', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractDemerithTranslation(item):

	'''
	# 'Demerith Translation'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractAnotherWorldTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Depths of Labyrinth' in item['tags']:
		return buildReleaseMessage(item, 'Aim for the Deepest Part of the Different World\'s Labyrinth', vol, chp, frag=frag, postfix=postfix)
	if 'Because, Janitor-san Is Not a Hero' in item['tags']:
		return buildReleaseMessage(item, 'Because, Janitor-san Is Not a Hero', vol, chp, frag=frag, postfix=postfix)
	if 'World Death Game' in item['tags']:
		return buildReleaseMessage(item, 'The World is Fun as it has Become a Death Game', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractDeadlyForgottenLegends(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractAlbertKenoreijou(item):
	'''
	#'Albert Kenoreijou'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def  extractDuckysEnglishTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractDekinaiDiary(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Konjiki no Word Master' in item['tags']:
		return buildReleaseMessage(item, 'Konjiki no Word Master', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractBijinsans(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Benkyou no Kamisama wa Hitomishiri' in item['tags']:
		return buildReleaseMessage(item, 'Benkyou no Kamisama wa Hitomishiri', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractArchivity(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractCheddar(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractAllsFairInLoveWar(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractEnte38translations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractCatScans(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractAmeryEdge(item):
	'''
	# 'Amery Edge'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

	if 'Articles' in item['tags'] or 'Guides' in item['tags']:
		return None

	if 'Your Highness, I Know My Wrong' in item['tags'] or 'Your Highness, I Know My Wrongs' in item['tags']:
		return buildReleaseMessage(item, 'Your Highness, I Know My Wrong', vol, chp, frag=frag, postfix=postfix)
	if '108 Star Maidens of Destiny' in item['tags']:
		return buildReleaseMessage(item, '108 Star Maidens of Destiny', vol, chp, frag=frag, postfix=postfix)
	if 'Zombie Girl, Where Are You?' in item['tags']:
		return buildReleaseMessage(item, 'Zombie Girl, Where Are You?', vol, chp, frag=frag, postfix=postfix)
	if 'Ultimate Assassin System' in item['tags']:
		return buildReleaseMessage(item, 'Ultimate Assassin System', vol, chp, frag=frag, postfix=postfix)
	if 'Assassin Farmer' in item['tags']:
		return buildReleaseMessage(item, 'Assassin Farmer', vol, chp, frag=frag, postfix=postfix)
	if 'I Am A Killer' in item['tags']:
		return buildReleaseMessage(item, 'I Am A Killer', vol, chp, frag=frag, postfix=postfix)
	if '108 Maidens of Destiny' in item['tags']:
		return buildReleaseMessage(item, '108 Maidens of Destiny', vol, chp, frag=frag, postfix=postfix)

	return False

def  extractDokuHanaTranslations(item):
	'''
	#'DokuHana Translations'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def  extractDurasama(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Arifureta' in item['tags']:
		return buildReleaseMessage(item, 'Arifureta', vol, chp, frag=frag, postfix=postfix)
	if 'Manuke FPS' in item['tags']:
		return buildReleaseMessage(item, 'Manuke na FPS Player ga isekai e ochita baai', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractCurrentlyTLingBuniMi(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

	if item['title'].startswith("[BNM]"):
		return buildReleaseMessage(item, 'Bu ni Mi wo Sasagete Hyaku to Yonen. Elf de Yarinaosu Musha Shugyou', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith("[DD]"):
		return buildReleaseMessage(item, 'Doll Dungeon', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith("[HCLS]"):
		return buildReleaseMessage(item, 'High Comprehension Low Strength', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractGOChronicles(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractDisappointingTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'GSB' in item['tags']:
		return buildReleaseMessage(item, 'Galaxy Shattering Blade', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractForwardSlash(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Isekai ni Demodori Shimashita?' in item['tags']:
		return buildReleaseMessage(item, 'Isekai ni Demodori Shimashita?', vol, chp, frag=frag, postfix=postfix)

	return False

def  extractCodeZerosBlog(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractFalamarTranslation(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Isekai ni kanaderu densetsu' in item['tags']:
		return buildReleaseMessage(item, 'Isekai ni kanaderu densetsu ~toki wo tomeru mono~', vol, chp, frag=frag, postfix=postfix)
	if 'The road to become a transition master in another world' in item['tags']:
		return buildReleaseMessage(item, 'The Road to Become a Transition Master in Another World', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractEpithetic(item):
	'''
	# 'Epithetic'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractAresNovels(item):
	'''
	# 'Ares Novels'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractBladeOfHearts(item):
	'''
	# 'Blade of Hearts'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractATravelersTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractCautrs(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractEmergencyExitsReleaseBlog(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractFaketypist(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'The Magician wants Normality' in item['tags']:
		return buildReleaseMessage(item, 'Madoushi wa Heibon wo Nozomu', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractDeliciousTranslations(item):
	'''
	# 'Delicious Translations'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if item['title'].startswith('Pet Charm'):
		return buildReleaseMessage(item, 'Pet Charm', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('School Beauty Personal Bodyguard'):
		return buildReleaseMessage(item, 'School Beauty Personal Bodyguard', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractBadTranslation(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractDreamlessWindowsTranslation(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractChineseWeabooTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractFuzionLife(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractDreamAvenue(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractAlicetranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractCircleofShards(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if re.match(r"^Chapter \d+", item['title'], re.IGNORECASE):
		return buildReleaseMessage(item, 'Circle of Shards', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False

def  extractCloudManor(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Book of Sun & Moon Swordplay' in item['tags']:
		return buildReleaseMessage(item, 'Book of Sun & Moon Swordplay', vol, chp, frag=frag, postfix=postfix)
	if 'It is a Straight Road' in item['tags']:
		return buildReleaseMessage(item, 'It is a Straight Road', vol, chp, frag=frag, postfix=postfix)
	if 'Pursuit of Liao Yue Murderer' in item['tags']:
		return buildReleaseMessage(item, 'Pursuit of Liao Yue Murderer', vol, chp, frag=frag, postfix=postfix)
	if 'Rice Pot Next Door' in item['tags']:
		return buildReleaseMessage(item, 'Rice Pot Next Door', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractEnsigsWritings(item):
	'''
	#'Ensig\'s Writings'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Sword-shisho' in item['tags']:
		return buildReleaseMessage(item, 'I was a Sword when I Reincarnated!', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Gentle Demon' in item['tags']:
		return buildReleaseMessage(item, 'Demon Noble Girl ~Tale of a Gentle Demon~', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Undead(?) Life' in item['tags']:
		return buildReleaseMessage(item, 'Life(?) as an Undead', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False





def  extractAnotherParallelWorld(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractCrackofDawnTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	return False


####################################################################################################################################################
#
####################################################################################################################################################

def  extractEugeneRain(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractAnneAndCindy(item):
	'''
	# 'Anne And Cindy'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractATranslatorsRamblings(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractEvidasIndoRomance(item):
	'''
	# "Evida's Indo Romance"
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractELYSIONTranslation(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractAltorocTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Shadow Rogue' in item['tags']:
		return buildReleaseMessage(item, 'Shadow Rogue', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractAranTranslations(item):
	'''

	# 'Aran Translations'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if item['title'].startswith("IGE – "):
		return buildReleaseMessage(item, 'Imperial God Emperor', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith("IDS – "):
		return buildReleaseMessage(item, 'Inverted Dragon\'s Scale', vol, chp, frag=frag, postfix=postfix)
	return False

def extractBluePhoenix(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if item['title'].startswith("Chapter") and item['tags'] == ['Uncategorized']:
		return buildReleaseMessage(item, 'Blue Phoenix', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if item['title'].startswith("Blue Phoenix Chapter ") and item['tags'] == ['Uncategorized']:
		return buildReleaseMessage(item, 'Blue Phoenix', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if item['title'].startswith("Overthrowing Fate Chapter ") and item['tags'] == ['Uncategorized']:
		return buildReleaseMessage(item, 'Overthrowing Fate', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False
def extractDemonTranslations(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'The Gate Of Good Fortune' in item['tags'] or item['title'].startswith('New TGOGF Chapter Release!!'):
		return buildReleaseMessage(item, 'The Gate Of Good Fortune', vol, chp, frag=frag, postfix=postfix)
	if 'The Unsuspecting Journey' in item['tags']:
		return buildReleaseMessage(item, 'The Unsuspecting Journey', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False

def extractAlternativeProjects(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractApolloTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractElementalCobalt(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if item['title'].lower().startswith('arifureta chapter'):
		return buildReleaseMessage(item, 'Arifureta Shokugyou de Sekai Saikyou', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('requiem to the stars'):
		return buildReleaseMessage(item, 'Requiem to the Stars', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False

def extractExtantVisions(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Lily Ex Machina' in item['tags']:
		return buildReleaseMessage(item, 'Lily Ex Machina', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False

def extractAnanasParfait(item):
	"""
	Ananas Parfait
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'The Sorcerer Laughs in the Mirror' in item['tags']:
		return buildReleaseMessage(item, 'The Sorcerer Laughs in the Mirror', vol, chp, frag=frag, postfix=postfix)
	return False
def extractAnimeMangaTranslations(item):
	"""
	Anime, manga, translations
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

	bad = [
			'Read Online',
			'Download',
			'comic',
			'Anime',
			'Manga',
			'Robotech',
			'Alpen Rose',
			'Watch Online',
		]

	if any([tmp in item['tags'] for tmp in bad]):
		return None
	if "[Chang Sheng] BABY" in item['title']:
		return None
	if "[RAW]" in item['title']:
		return None

	return False
def extractAnkouTranslations(item):
	"""
	Ankou Translations
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractAntheor(item):
	"""
	Antheor
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Hisshou Dungeon Unei Houhou' in item['tags'] or 'HDUH Annoucement' in item['tags']:
		return buildReleaseMessage(item, 'Hisshou Dungeon Unei Houhou', vol, chp, frag=frag, postfix=postfix)
	if 'KYNE Announcement' in item['tags']:
		return buildReleaseMessage(item, 'Kami Sumeragi Yuusha no eiyuutan 《Ryokou Tan》', vol, chp, frag=frag, postfix=postfix)
	return False
def extractBo(item):
	"""
	Bo
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractChaosWords(item):
	"""
	Chaos Words
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractChinaLightNovel(item):
	"""
	China Light Novel
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractChineseNovelTranslated(item):
	"""
	Chinese Novel Translated
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractChocolateCosmosTranslations(item):
	"""
	ChocolateCosmos Translations
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractDatebayoBlog(item):
	"""
	Datebayo Blog
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractDaupao(item):
	"""
	Daupao
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractDeepAzureSky(item):
	"""
	Deep Azure Sky
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractDemonScorpionTranslations(item):
	"""
	Demon Scorpion Translations
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractDwrfTL(item):
	"""
	Dwrf TL
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractExMachinaAsia(item):
	"""
	ExMachina.Asia
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractFakeFruitsTranslations(item):
	"""
	Fake Fruits Translations
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractFantasyBooksLive(item):
	"""
	fantasy-books.live
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

	snames = [
		'Heavenward On Golden Wings',
		'The Abandoned',
		'Regarding The Life of A Certain Fallen Noble',
		'Orphans of a Dead Nation',
		'Life and Times of Mitch and Akki',
		'God\'s Island',
		'Black Titan',
		'Aeterna Saga',
		'Fighting God',
		'Antagonist Rewind',
		'Black Watch Asylum',
		'Three Lifetimes',
		'Magical Tournament',
		'Villainess',
		'Walking With Giants',
		'Invincible Level Up',
		'The Royal Princess Fox',
	]

	tlut = {tmp.lower():tmp for tmp in snames}

	tlut['pygmalion'] = 'Pygmalion Is Planting Seeds'

	ltags = [tmp.lower() for tmp in item['tags']]
	for key, value in tlut.items():
		if key in ltags:
			if "/translations/" in item['linkUrl']:
				tl_type = 'translated'
			else:
				tl_type = 'oel'

			return buildReleaseMessage(item, value, vol, chp, frag=frag, postfix=postfix, tl_type='tl_type')



	return False

def extractForKalimdor(item):
	"""
	For Kalimdor
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

	if item['title'].startswith('Bringing The Farm To Live In Another World'):
		return buildReleaseMessage(item, 'Bringing The Farm To Live In Another World', vol, chp, frag=frag, postfix=postfix)
	if 'BTFTLIAW' in item['tags']:
		return buildReleaseMessage(item, 'Bringing The Farm To Live In Another World', vol, chp, frag=frag, postfix=postfix)
	return False
def extractForthemoneyTranslations(item):
	"""
	Forthemoney Translations
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

	return False
def extractGirlyNovels(item):
	"""
	Girly Novels
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractEllionoraTranslation(item):
	"""
	Ellionora Translation
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False



def extractAPurpleBlob(item):
	'''
	A Purple Blob
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if re.match(r"^Nirvana in Fire Chapter \d+", item['title'], re.IGNORECASE):
		return buildReleaseMessage(item, "Nirvana in Fire", vol, chp, frag=frag, postfix=postfix)
	return False

def extractAbsurdTranslation(item):
	'''
	Absurd Translation
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

	if re.match(r"^I Kinda Came to Another World \– \d+$", item['title'], re.IGNORECASE):
		return buildReleaseMessage(item, "I Kinda Came to Another World, but Where’s the Way Home?", vol, chp, frag=frag, postfix=postfix)
	if re.match(r"^Isekai ni Kanaderu Denset[su][su] \– \d+$", item['title'], re.IGNORECASE):
		return buildReleaseMessage(item, "Isekai ni kanaderu densetsu ~Toki wo Tomeru Mono~", vol, chp, frag=frag, postfix=postfix)
	if re.match(r"^Magi’s grandson – \d+$", item['title'], re.IGNORECASE):
		return buildReleaseMessage(item, "Magi’s Grandson", vol, chp, frag=frag, postfix=postfix)
	return False

def extractAeRoSoL31(item):
	'''
	AeRoSoL31
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractAinushiTranslations愛主の翻訳(item):
	'''
	Ainushi Translations 愛主の翻訳
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractAJRG(item):
	'''
	AJRG
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractAlchyrdoesthings(item):
	'''
	Alchyr does things
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractAlmightyAthlete(item):
	'''
	Almighty Athlete
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractAsthmaticSpiderTranslations(item):
	'''
	Asthmatic Spider Translations
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Grimoire X Reverse' in item['tags']:
		return buildReleaseMessage(item, 'Grimoire X Reverse', vol, chp, frag=frag, postfix=postfix)
	if 'Sleep Learning' in item['tags']:
		return buildReleaseMessage(item, 'Sleep Learning', vol, chp, frag=frag, postfix=postfix)
	return False

def extractAsuraTales(item):
	'''
	Asura Tales
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractAvaritiakun(item):
	'''
	Avaritia-kun
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractAvertTranslations(item):
	'''
	Avert Translations~
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

	if re.match(r"^Release:? fuyo shoukan mahou? vol ?\d+ chapter \d+", item['title'], re.IGNORECASE):
		return buildReleaseMessage(item, "Boku wa Isekai de Fuyo Mahou to Shoukan Mahou wo Tenbin ni Kakeru", vol, chp, frag=frag, postfix=postfix)
	return False

def extractBionicarkTranslations(item):
	'''
	Bionicark Translations
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractCagedBramblingsInAPavilion(item):
	'''
	Caged Bramblings In A Pavilion
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractChaoticSwordTranslations(item):
	'''
	Chaotic Sword Translations
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractChaoticTranslations(item):
	'''
	Chaotic Translations
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractChimpsMTLSpot(item):
	'''
	Chimp\'s MTL Spot
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractCircaTranslations(item):
	'''
	Circa Translations
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractClesesiaBlogspot(item):
	'''
	Clesesia Blogspot~
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractDaikyunTranslations(item):
	'''
	Daikyun Translations
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if item['title'].lower().startswith("the evil organization’s recruitment ad: "):
		return buildReleaseMessage(item, 'The Evil Organization’s Recruitment Ad', vol, chp, frag=frag, postfix=postfix)
	return False

def extractDysrySummaries(item):
	'''
	Dysry Summaries
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Summary' in item['tags']:
		return None

	return False

def extractEGSmartTranslation(item):
	'''
	EG-Smart-Translation
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractEGSNBlog(item):
	'''
	EGSN Blog
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractEndofDoomMTL(item):
	'''
	End of Doom MTL
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

	if 'Doom Lord' in item['tags']:
		return buildReleaseMessage(item, 'Doom Lord', vol, chp, frag=frag, postfix=postfix)

	return False

def extractEternalDreamlandTranslation(item):
	'''
	Eternal Dreamland Translation
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Amorous Slave Girl' in item['tags']:
		return buildReleaseMessage(item, 'Amorous Slave Girl', vol, chp, frag=frag, postfix=postfix)
	if 'Dragon Blood Warrior' in item['tags']:
		return buildReleaseMessage(item, 'Dragon Blood Warrior', vol, chp, frag=frag, postfix=postfix)
	if 'Love Affair With Sister-In-Law' in item['tags']:
		return buildReleaseMessage(item, 'Love Affair With Sister-In-Law', vol, chp, frag=frag, postfix=postfix)
	if 'Peerless Demonic Lord' in item['tags']:
		return buildReleaseMessage(item, 'Peerless Demonic Lord', vol, chp, frag=frag, postfix=postfix)
	return False

def extractExplore(item):
	'''
	Explore
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractExpNull(item):
	'''
	ExpNull
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractFailTranslations(item):
	'''
	FailTranslations
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractFairlyAccurateTranslations(item):
	'''
	Fairly Accurate Translations
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

	if item['title'].lower().startswith("Card Disciple – Chapter"):
		return buildReleaseMessage(item, 'Card Disciple', vol, chp, frag=frag, postfix=postfix)
	return False

def extractFakeFruitTranslation(item):
	'''
	Fake Fruit Translation
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Bringing the Supermarket to the Apocalypse' in item['tags']:
		return buildReleaseMessage(item, 'Bringing the Supermarket to the Apocalypse', vol, chp, frag=frag, postfix=postfix)
	return False

def extractFantasyNovels(item):
	'''
	Fantasy Novels
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractFeelsBadTranslations(item):
	'''
	Feels Bad Translations
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractFrozensLazyBlog(item):
	'''
	Frozen\'s Lazy Blog
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractFuwaFuwaTales(item):
	'''
	Fuwa Fuwa Tales
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractGrandlation(item):
	'''
	Grandlation
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractGurosLibraryofStories(item):
	'''
	Guro\'s Library of Stories
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractChinaNovelNet(item):
	'''
	China Novel.net
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if item['title'].startswith("Shura’s Wrath Chapter"):
		return buildReleaseMessage(item, 'Shura’s Wrath', vol, chp, frag=frag, postfix=postfix)

	return False



def extractACupofMemory(item):
	'''
	'A Cup of Memory'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractALittleMirageTranslation(item):
	'''
	'A Little Mirage Translation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractABCpwip(item):
	'''
	'ABCpwip'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractAfterTranslations(item):
	'''
	'After;Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractAiHristDreamTranslations(item):
	'''
	'Ai Hrist Dream Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractAlpenGlowTranslations(item):
	'''
	'Alpen Glow Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractAndromedaBoul(item):
	'''
	'Andromeda & Boul'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractAnkydonsLair(item):
	'''
	"Ankydon's Lair"
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractBLNovelObsession(item):
	'''
	'BL Novel Obsession'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractChauffeurTranslations(item):
	'''
	'Chauffeur Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractChoyceClub(item):
	'''
	'Choyce.club'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractChroniclesofGaia(item):
	'''
	'Chronicles of Gaia'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractDailyDoseNovels(item):
	'''
	'Daily Dose Novels'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractDrakeTranslations(item):
	'''
	'Drake Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractDuskTales(item):
	'''
	'Dusk Tales'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractEndofthedays42(item):
	'''
	'End of the days42'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractEveningBoatTranslations(item):
	'''
	'Evening Boat Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractFeelsBadTranslation(item):
	'''
	'Feels Bad Translation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractFriendshipIsPower(item):
	'''
	'Friendship Is Power'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False




