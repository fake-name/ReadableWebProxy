def extractShineTranslation(item):
	"""
	Shine Translation
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('Invincible Level up '):
		return buildReleaseMessageWithType(item, 'Invincible Level Up', vol, chp, frag=frag, postfix=postfix)
	return False
