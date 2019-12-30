def extract7DaysTrial(item):
	"""
	#'7 Days Trial'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'content' in item['tags']:
		return buildReleaseMessageWithType(item, 'War of the Supreme', vol, chp, frag=frag, postfix=postfix)
	return False
