def extractPlaceOfLegends(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'The Fragile Monster Lord' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Fragile Monster Lord', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'The New Start' in item['tags']:
		return buildReleaseMessageWithType(item, 'The New Start', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'The Rude Time Stopper' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Rude Time Stopper', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
