def extractAranTranslations(item):
	"""

	# 'Aran Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None

	tagmap = [
		('IDS',       'Imperial God Emperor',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	if item['title'].startswith('IGE – '):
		return buildReleaseMessageWithType(item, 'Imperial God Emperor', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('IDS – '):
		return buildReleaseMessageWithType(item, "Inverted Dragon's Scale", vol, chp, frag=frag, postfix=postfix)
	return False