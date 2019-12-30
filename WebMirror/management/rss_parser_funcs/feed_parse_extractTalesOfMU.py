def extractTalesOfMU(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if any('volume' in tag.lower() for tag in item['tags']) and (chp or vol):
		return buildReleaseMessageWithType(item, 'Tales of MU', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
