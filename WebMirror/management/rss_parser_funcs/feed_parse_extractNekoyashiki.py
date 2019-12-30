def extractNekoyashiki(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'rakudai kishi no eiyuutan' in item['tags']:
		return buildReleaseMessageWithType(item, 'Rakudai Kishi no Eiyuutan', vol, chp, frag=frag, postfix=postfix)
	if 'Ore no Pet was Seijo-sama' in item['tags'] or 'Ore no Pet wa Seijo-sama' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ore no Pet was Seijo-sama', vol, chp, frag=frag, postfix=postfix)
	if 'M-chan wars' in item['tags']:
		return buildReleaseMessageWithType(item, 'M-chan Wars: Rise and Fall of the Cat Tyrant', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Etranger of the Sky' in item['tags'] or 'Tenkyuu no Etranger' in item['tags']:
		return buildReleaseMessageWithType(item, 'Spear of Thunder – Etranger of the Sky', vol, chp, frag=frag, postfix=postfix)
	if 'Yamato Nadeshiko' in item['tags']:
		return buildReleaseMessageWithType(item, 'Yamato Nadeshiko, Koibana no Gotoku', vol, chp, frag=frag, postfix=postfix)
	if 'Youhei Monogatari' in item['tags']:
		return buildReleaseMessageWithType(item, 'Youhei Monogatari ~Junsuinaru Hangyakusha (Rebellion)~', vol, chp, frag=frag, postfix=postfix)
	if 'Qualidea Code' in item['tags']:
		return buildReleaseMessageWithType(item, 'Qualidea Code', vol, chp, frag=frag, postfix=postfix)
	if 'The Brander Female Fencer' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Brander Female Fencer', vol, chp, frag=frag, postfix=postfix)
	if 'The Elf is a Freeloader' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Elf is a Freeloader', vol, chp, frag=frag, postfix=postfix)
	return False
