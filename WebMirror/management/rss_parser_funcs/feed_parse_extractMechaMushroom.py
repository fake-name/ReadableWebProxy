def extractMechaMushroom(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'YaoNie Bing Wang (WSK)' in item['title'] or 'Yao Nie Bing Wang (WSK)' in item['title'] or 'YNBW (WSK)' in item['title']:
		return buildReleaseMessageWithType(item, 'Yao Nie Bing Wang', vol, chp, frag=frag, postfix=postfix)
	if 'Jiang Ye Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Jiang Ye Chapter', vol, chp, frag=frag, postfix=postfix)
	return False
