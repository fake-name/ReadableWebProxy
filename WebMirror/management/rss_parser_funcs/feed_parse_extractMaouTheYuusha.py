def extractMaouTheYuusha(item):
	"""
	# Maou the Yuusha

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if ':' in item['title']:
		postfix = item['title'].split(':', 1)[-1]
	if 'Maou the Yuusha' in item['tags'] and 'chapter' in [tmp.lower() for tmp in item['tags']]:
		return buildReleaseMessageWithType(item, 'Maou the Yuusha', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
