def extractWitchLife(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Witch Life' in item['tags']:
		return buildReleaseMessageWithType(item, 'Witch Life', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
