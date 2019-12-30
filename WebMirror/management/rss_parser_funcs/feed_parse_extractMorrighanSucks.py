def extractMorrighanSucks(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Unlimited Anime Works' in item['title']:
		return buildReleaseMessageWithType(item, 'Unlimited Anime Works', vol, chp, frag=frag, postfix=postfix)
	return False
