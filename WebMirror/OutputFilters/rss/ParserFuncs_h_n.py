
from WebMirror.OutputFilters.util.MessageConstructors import buildReleaseMessage
from WebMirror.OutputFilters.util.TitleParsers import extractChapterVol
from WebMirror.OutputFilters.util.TitleParsers import extractChapterVolFragment
from WebMirror.OutputFilters.util.TitleParsers import extractVolChapterFragmentPostfix

import re


####################################################################################################################################################
def extractJaptem(item):
	'''
	# Japtem

	'''
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
def extractLygarTranslations(item):
	'''
	# Lygar Translations

	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if ('elf tensei' in item['tags'] or 'elf tensei' in item['title'].lower()) and not 'news' in item['tags']:
		return buildReleaseMessage(item, 'Elf Tensei Kara no Cheat Kenkoku-ki', vol, chp, frag=frag, postfix=postfix)
	if 'Himekishi ga Classmate' in item['tags'] and not 'poll' in item['tags']:
		return buildReleaseMessage(item, 'Himekishi ga Classmate! ~ Isekai Cheat de Dorei ka Harem~', vol, chp, frag=frag, postfix=postfix)

	return False




####################################################################################################################################################
def extractMadoSpicy(item):
	'''
	# MadoSpicy TL

	'''
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
def extractHotCocoa(item):
	'''
	# Hot Cocoa Translations

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
def extractManga0205Translations(item):
	'''
	# Manga0205 Translations

	'''
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
def extractKnW(item):
	'''
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

	'''
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





def extractKirikoTranslations(item):
	'''

	'''
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
def extractKiri(item):
	'''
	# Kiri Leaves:

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Tensei Oujo' in item['tags'] and (vol or chp):
		return buildReleaseMessage(item, 'Tensei Oujo wa Kyou mo Hata o Tatakioru', vol, chp, frag=frag, postfix=postfix)

	return False



####################################################################################################################################################
def extractLingson(item):
	'''
	# Lingson's Translations

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'The Legendary Thief' in item['tags'] and (vol or chp or postfix):
		return buildReleaseMessage(item, 'Virtual World - The Legendary Thief', vol, chp, frag=frag, postfix=postfix)
	if 'ALBT Chapter Release' in item['tags'] and (vol or chp or postfix):
		return buildReleaseMessage(item, 'Assassin Landlord Beauty Tenants', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractHajiko(item):
	'''
	# Hajiko translation

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Ryuugoroshi no Sugosuhibi' in item['title'] or 'Ryuugoroshi no Sugosu Hibi' in item['tags']:
		return buildReleaseMessage(item, 'Ryugoroshi no Sugosuhibi', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractImoutolicious(item):
	'''
	# Imoutolicious

	'''
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
def extractIsekaiMahou(item):
	'''
	# Isekai Mahou Translations!

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Isekai Mahou Chapter' in item['title'] and 'Release' in item['title']:
		return buildReleaseMessage(item, 'Isekai Mahou wa Okureteru!', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractKerambit(item):
	'''
	# Kerambit's Incisions

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Yobidasa' in item['tags'] and (vol or chp):
		if not postfix and ":" in item['title']:
			postfix = item['title'].split(":")[-1]

		return buildReleaseMessage(item, 'Yobidasareta Satsuriku-sha', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
def extractMahoutsuki(item):
	'''
	# Mahoutsuki Translation

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	# Only ever worked on Le Festin de Vampire
	if 'Uncategorized' in item['tags'] and chp and ("Chapter" in item['title'] or "prologue" in item['title']):
		return buildReleaseMessage(item, 'Le Festin de Vampire', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
def extractMaouTheYuusha(item):
	'''
	# Maou the Yuusha

	'''
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
def extractNightbreeze(item):
	'''
	# Nightbreeze Translations

	'''
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
def extractLnAddiction(item):
	'''
	# Ln Addiction

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if ('Hissou Dungeon Unei Houhou' in item['tags'] or 'Hisshou Dungeon Unei Houhou' in item['tags']) and (chp or frag):
		return buildReleaseMessage(item, 'Hisshou Dungeon Unei Houhou', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
def extractNEET(item):
	'''
	# Lazy NEET Translations

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'NEET dakedo Hello Work ni Ittara Isekai ni Tsuretekareta' in item['tags']:
		return buildReleaseMessage(item, 'NEET dakedo Hello Work ni Ittara Isekai ni Tsuretekareta', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
def extractHokageTrans(item):
	'''
	# Hokage Translations

	'''
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
def extractNeoTranslations(item):
	'''
	# Neo Translations

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'The Man Picked up by the Gods'.lower() in item['title'].lower() and (chp or vol):
		return buildReleaseMessage(item, 'The Man Picked up by the Gods', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractHenoujiTranslation(item):
	'''
	# Henouji Translation

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Get Naked' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Kazuha Axeplant’s Third Adventure', vol, chp, frag=frag, postfix=postfix)

	if ('Tensai Slime' in item['tags'] or 'Tensei Slime' in item['tags']) and  (chp or vol):
		return buildReleaseMessage(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractInfiniteNovelTranslations(item):
	'''
	# Infinite Novel Translations

	'''
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
def extractIsekaiTranslation(item):
	'''
	# Isekai Soul-Cyborg Translations

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Isekai Maou to Shoukan Shoujo Dorei Majutsu' in item['tags'] and (chp or vol) and not "manga" in item['title'].lower():
		if chp == 11 and frag == 10:
			return False
		return buildReleaseMessage(item, 'Isekai Maou to Shoukan Shoujo no Dorei Majutsu', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractIterations(item):
	'''
	# Iterations within a Thought-Eclipse

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'SaeKano' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Saenai Heroine no Sodatekata', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractKaezar(item):
	'''
	# Kaezar Translations

	'''
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
def extractLarvyde(item):
	'''
	# Larvyde Translation

	'''
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
def extractIzra709(item):
	'''
	# izra709 | B Group no Shounen Translations

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if not postfix and "–" in item['title']:
		postfix = item['title'].split('–')[-1]

	if 'monohito chapter' in item['title'].lower():
		return buildReleaseMessage(item, 'Monogatari no Naka no Hito', vol, chp, frag=frag, postfix=postfix)
	if 'b group chapter' in item['title'].lower():
		return buildReleaseMessage(item, 'B Group no Shounen', vol, chp, frag=frag, postfix=postfix)
	if 'assassin chapter' in item['title'].lower():
		return buildReleaseMessage(item, 'Other World Assassin Life of a Man who was a Shut-in', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractNohohon(item):
	'''
	# 'Nohohon Translation'

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Monster Musume Harem wo Tsukurou!' in item['tags']:
		return buildReleaseMessage(item, 'Monster Musume Harem o Tsukurou!', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractNeetTranslations(item):
	'''
	# NEET Translations

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Marginal Operation' in item['tags']:
		return buildReleaseMessage(item, 'Marginal Operation', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractKyakka(item):
	'''
	# Kyakka

	'''
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
def extractNoviceTranslator(item):
	'''
	# 'NoviceTranslator'

	'''
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
def extractMahouKoukoku(item):
	'''
	# MahouKoukoku

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Shiro no Koukoku Monogatari ' in item['title']:
		return buildReleaseMessage(item, 'Shiro no Koukoku Monogatari', vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
# JawzTranslations
####################################################################################################################################################
def extractJawzTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Zectas' in item['tags'] and vol and chp:
		return buildReleaseMessage(item, 'Zectas', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'LMS' in item['tags'] and vol and chp:
		return buildReleaseMessage(item, 'Legendary Moonlight Sculptor', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractLunate(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if "chapter" in item['title'].lower() and (vol or chp):
		return buildReleaseMessage(item, 'World Customize Creator', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractMoonBunnyCafe(item):
	'''

	'''
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
def extractLonahora(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if "Earth's Core" in item['tags'] and (chp and vol):
		return buildReleaseMessage(item, "Earth's Core", vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractLostInTranslation(item):
	'''

	'''
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
def extractHoldX(item):
	'''

	'''
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
def extractLoiterous(item):
	'''

	'''
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
	'''

	'''
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
def extractNovelsNao(item):
	'''

	'''
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
	'''

	'''
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
def extractNutty(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'A Mistaken Marriage Match' in item['tags'] and 'a generation of military counselor' in item['tags']:
		return buildReleaseMessage(item, 'A mistaken marriage match: A generation of military counselor', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractManaTankMagus(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Mana Tank Magus' in item['tags']:
		return buildReleaseMessage(item, 'Mana Tank Magus', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractKamiTranslation(item):
	'''

	'''
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
def extractKobatoChanDaiSukiScan(item):
	'''

	'''
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
def extractKingJaahn(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	return buildReleaseMessage(item, 'Divine Progress', vol, chp, frag=frag, postfix=postfix, tl_type='oel')


####################################################################################################################################################
#
####################################################################################################################################################
def extractKoreanNovelTrans(item):
	'''

	'''
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
def extractKahoim(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Soshite Shoujo wa Akujo no Karada o Te ni Ireru' in item['tags'] :
		return buildReleaseMessage(item, 'Soshite Shoujo wa Akujo no Karada o Te ni Ireru', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractHoldXandClick(item):
	'''

	'''
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
	'''

	'''
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
def extractIsekaiTranslations(item):
	'''

	'''
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
def extractMakinaTranslations(item):
	'''

	'''
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
	'''

	'''
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
	'''

	'''
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
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Ryouriban' in item['title']:
		return buildReleaseMessage(item, 'The Cook of the Mercenary Corp', vol, chp, frag=frag, postfix=postfix)
	if 'UchiMusume' in item['title']:
		return buildReleaseMessage(item, 'For my daughter, I might even be able to defeat the demon king', vol, chp, frag=frag, postfix=postfix)

	return False

def extractLasciviousImouto(item):
	'''

	'''
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
def extractNanjamora(item):
	'''

	'''
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
def extractNooblate(item):
	'''

	'''
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
def extractMadaoTranslations(item):
	'''

	'''
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
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Battle Emperor' in item['tags']:
		return buildReleaseMessage(item, 'Battle Emperor', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractMorrighanSucks(item):
	'''

	'''
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
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'World of Hidden Phoenix' in item['tags']:
		return buildReleaseMessage(item, 'World of Hidden Phoenix', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractMike777ac(item):
	'''
	# Mike777ac

	'''
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












