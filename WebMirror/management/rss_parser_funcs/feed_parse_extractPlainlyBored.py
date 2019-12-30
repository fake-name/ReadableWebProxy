def extractPlainlyBored(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Empress with no Virtue'.lower() in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Empress with no Virtue', vol, chp, frag=frag, postfix=postfix)
	return False
