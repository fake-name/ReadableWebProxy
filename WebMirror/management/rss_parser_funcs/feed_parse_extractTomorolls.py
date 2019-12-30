def extractTomorolls(item):
	"""
	# Tomorolls

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Cicada as Dragon' in item['tags'] or 'Semi Datte Tensei Sureba Ryuu Ni Naru' in item['title']:
		return buildReleaseMessageWithType(item, 'Cicada as Dragon', vol, chp, frag=frag, postfix=postfix)
	return False
