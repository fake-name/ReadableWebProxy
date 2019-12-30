def extractBathrobeKnight(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if not postfix and '-' in item['title']:
		postfix = item['title'].split('-')[-1]
	return buildReleaseMessageWithType(item, 'The Bathrobe Knight', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
