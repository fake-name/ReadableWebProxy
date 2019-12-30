def extractSwordAndGame(item):
	"""
	# Sword And Game

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'The Rising of the Shield Hero' in item['tags'] and 'chapter' in [tmp.lower() for tmp in item['tags']]:
		return buildReleaseMessageWithType(item, 'The Rise of the Shield Hero', vol, chp, frag=frag, postfix=postfix)
	if 'Ark' in item['tags'] and (vol or chp or postfix):
		return buildReleaseMessageWithType(item, 'Ark', vol, chp, frag=frag, postfix=postfix)
	return False
