def extractDekinaiDiary(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	if 'Konjiki no Moji Tsukai' in item['tags']:
		return buildReleaseMessageWithType(item, 'Konjiki no Word Master', vol, chp, frag=frag, postfix=postfix)
	if 'Konjiki no Word Master' in item['tags']:
		return buildReleaseMessageWithType(item, 'Konjiki no Word Master', vol, chp, frag=frag, postfix=postfix)
		
	return False