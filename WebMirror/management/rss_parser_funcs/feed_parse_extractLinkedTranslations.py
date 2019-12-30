def extractLinkedTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('A Record of a Mortal’s Journey to Immortality:'):
		if not postfix and ':' in item['title']:
			postfix = item['title'].split(':')[-1]
		return buildReleaseMessageWithType(item, 'A Record of a Mortal’s Journey to Immortality', vol, chp, frag=frag, postfix=postfix)
	return False
