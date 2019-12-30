def extractNooblate(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Kujibiki Tokushou : Musou Harem Ken' in item['title'] or 'Kujibiku Tokushou : Musou Harem Ken' in item['title'] or 'Kujibiki Tokushou: Musou Hāremu ken' in item[
	    'title'] or 'Kujibiki Tokushou: Musou Harem Ken' in item['title'] or 'Kujibiji Tokushou : Musou Harem Ken' in item['title']:
		return buildReleaseMessageWithType(item, 'Kujibiki Tokushou : Musou Harem Ken', vol, chp, frag=frag, postfix=postfix)
	return False
