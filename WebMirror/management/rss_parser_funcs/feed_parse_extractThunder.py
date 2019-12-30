def extractThunder(item):
	"""
	# Thunder Translations:

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Stellar Transformations' in item['tags'] and (vol or chp):
		return buildReleaseMessageWithType(item, 'Stellar Transformations', vol, chp, frag=frag, postfix=postfix)
	return False
