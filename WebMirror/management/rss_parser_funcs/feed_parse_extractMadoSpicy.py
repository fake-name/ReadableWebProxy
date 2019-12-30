def extractMadoSpicy(item):
	"""
	# MadoSpicy TL

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Kyuuketsu Hime' in item['title']:
		postfix = ''
		if 'interlude' in postfix.lower():
			postfix = 'Interlude {num}'.format(num=chp)
			chp = None
		if 'prologue' in postfix.lower():
			postfix = 'Prologue {num}'.format(num=chp)
			chp = None
		return buildReleaseMessageWithType(item, 'Kyuuketsu Hime wa Barairo no Yume o Miru', vol, chp, frag=frag, postfix=postfix)
	return False
