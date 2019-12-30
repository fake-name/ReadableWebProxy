def extractZombieKnight(item):
	"""

	"""
	titleconcat = ' '.join(item['tags']) + item['title']
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(titleconcat)
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	return buildReleaseMessageWithType(item, 'The Zombie Knight', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
