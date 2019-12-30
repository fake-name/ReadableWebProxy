def extractAquarilasScenario(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'In That Moment of Suffering' in item['tags']:
		return buildReleaseMessageWithType(item, 'In That Moment of Suffering', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
