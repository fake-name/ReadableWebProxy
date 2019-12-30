def extractReddyCreations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'rigel' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Rigel', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	else:
		return buildReleaseMessageWithType(item, 'Riddick/ Against the Heavens', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
