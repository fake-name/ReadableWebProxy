def extractLylisTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'The Unicorn Legion:' in item['title']:
		postfix = item['title'].split(':', 1)[-1]
		return buildReleaseMessageWithType(item, 'The Unicorn Legion', vol, chp, frag=frag, postfix=postfix)
	return False
