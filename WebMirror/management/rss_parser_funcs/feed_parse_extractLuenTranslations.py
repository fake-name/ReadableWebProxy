def extractLuenTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Journey to Seek Past Reincarnations' in item['tags'] or item['title'].startswith('JTSPR'):
		return buildReleaseMessageWithType(item, 'Journey to Seek Past Reincarnations', vol, chp, frag=frag, postfix=postfix)
	if 'Little Phoenix Is Not An Immortal' in item['tags']:
		return buildReleaseMessageWithType(item, 'Little Phoenix Is Not An Immortal', vol, chp, frag=frag, postfix=postfix)
	if 'Hard to Escape' in item['tags']:
		return buildReleaseMessageWithType(item, 'Hard to Escape', vol, chp, frag=frag, postfix=postfix)
	return False
