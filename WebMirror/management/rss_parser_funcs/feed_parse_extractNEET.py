def extractNEET(item):
	"""
	# Lazy NEET Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'NEET dakedo Hello Work ni Ittara Isekai ni Tsuretekareta' in item['tags']:
		return buildReleaseMessageWithType(item, 'NEET dakedo Hello Work ni Ittara Isekai ni Tsuretekareta', vol, chp, frag=frag, postfix=postfix)
	return False
