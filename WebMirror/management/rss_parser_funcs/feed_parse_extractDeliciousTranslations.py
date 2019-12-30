def extractDeliciousTranslations(item):
	"""
	# 'Delicious Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('Pet Charm'):
		return buildReleaseMessageWithType(item, 'Pet Charm', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('School Beauty Personal Bodyguard'):
		return buildReleaseMessageWithType(item, 'School Beauty Personal Bodyguard', vol, chp, frag=frag, postfix=postfix)
	return False
