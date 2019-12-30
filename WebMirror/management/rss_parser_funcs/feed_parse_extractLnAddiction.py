def extractLnAddiction(item):
	"""
	# Ln Addiction

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if ('Hissou Dungeon Unei Houhou' in item['tags'] or 'Hisshou Dungeon Unei Houhou' in item['tags']) and (chp or frag):
		return buildReleaseMessageWithType(item, 'Hisshou Dungeon Unei Houhou', vol, chp, frag=frag, postfix=postfix)
	return False
