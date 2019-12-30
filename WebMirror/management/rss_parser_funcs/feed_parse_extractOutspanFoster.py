def extractOutspanFoster(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Chapter' in item['tags'] and 'ascension' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Ascension Chronicle', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
