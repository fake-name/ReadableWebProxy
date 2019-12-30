def extractTheMustangTranslator(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'The Six Immortals' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Six Immortals', vol, chp, frag=frag, postfix=postfix)
	return False
