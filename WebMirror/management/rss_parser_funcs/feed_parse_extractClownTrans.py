def extractClownTrans(item):
	"""
	# 'Translated by a Clown'

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Tensei Shitara Slime datta ken' in item['tags'] and chp:
		return buildReleaseMessageWithType(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)
	return False
