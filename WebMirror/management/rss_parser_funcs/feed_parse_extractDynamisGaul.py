def extractDynamisGaul(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Reincarnated by the God of Creation' in item['tags']:
		return buildReleaseMessageWithType(item, 'Reincarnated by the God of Creation', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Status Meister' in item['tags']:
		return buildReleaseMessageWithType(item, 'Status Meister', vol, chp, frag=frag, postfix=postfix)
	return False
