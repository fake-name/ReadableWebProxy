def extractBersekerTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if 'Because the world has changed into a death game is funny' in item['tags'] and (chp or vol or 'Prologue' in postfix):
		return buildReleaseMessageWithType(item, 'Sekai ga death game ni natta no de tanoshii desu', vol, chp, frag=frag, postfix=postfix)
	return False
