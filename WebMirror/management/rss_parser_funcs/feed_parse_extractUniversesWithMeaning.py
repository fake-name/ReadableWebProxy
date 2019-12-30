def extractUniversesWithMeaning(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Angel of Death' in item['title']:
		return buildReleaseMessageWithType(item, 'Angel of Death', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'In The Name Of God' in item['title']:
		return buildReleaseMessageWithType(item, 'In The Name Of God', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
