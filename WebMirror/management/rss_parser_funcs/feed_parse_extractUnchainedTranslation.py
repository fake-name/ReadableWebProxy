def extractUnchainedTranslation(item):
	"""
	# Unchained Translation

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'The Alchemist God' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'Ascension of the Alchemist God', vol, chp, frag=frag, postfix=postfix)
	return False
