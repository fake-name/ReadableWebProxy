def extractWeleTranslation(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if item['title'].lower().startswith('sin city'):
		return buildReleaseMessageWithType(item, 'Sin City', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('zhan xian'):
		return buildReleaseMessageWithType(item, 'Zhan Xian', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('heaven awakening path'):
		return buildReleaseMessageWithType(item, 'Heaven Awakening Path', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('immortal executioner'):
		return buildReleaseMessageWithType(item, 'Immortal Executioner', vol, chp, frag=frag, postfix=postfix)
	return False
