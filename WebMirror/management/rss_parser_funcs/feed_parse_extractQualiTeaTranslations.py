def extractQualiTeaTranslations(item):
	"""
	# 'QualiTeaTranslations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Harry Potter and the Rise of the Ordinary Person' in item['tags']:
		return None
	if 'Romance of Dragons and Snakes' in item['tags']:
		return buildReleaseMessageWithType(item, 'Romance of Dragons and Snakes', vol, chp, frag=frag, postfix=postfix)
	return False
