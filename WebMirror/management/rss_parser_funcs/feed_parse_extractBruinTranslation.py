def extractBruinTranslation(item):
	"""
	# 'Bruin Translation'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if not item['title']:
		return False
	if item['tags'] == ['Uncategorized'] and item['title'].startswith('Volume'):
		return buildReleaseMessageWithType(item, 'Otherworldly Evil Monarch', vol, chp, frag=frag, postfix=postfix)
	return False
