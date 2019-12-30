def extractCrystalRainDescends(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Honey Stewed Squid' in item['tags']:
		return buildReleaseMessageWithType(item, 'Honey Stewed Squid', vol, chp, frag=frag, postfix=postfix)
	if 'Bloom' in item['tags']:
		return buildReleaseMessageWithType(item, 'Bloom', vol, chp, frag=frag, postfix=postfix)
	return False
