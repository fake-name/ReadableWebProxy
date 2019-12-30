def extractDailyDoseNovels(item):
	"""
	'Daily Dose Novels'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Castle of Black Iron' in item['tags']:
		return buildReleaseMessageWithType(item, 'Castle of Black Iron', vol, chp, frag=frag, postfix=postfix)
	return False
