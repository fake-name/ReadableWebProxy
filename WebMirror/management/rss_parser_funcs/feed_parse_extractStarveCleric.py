def extractStarveCleric(item):
	"""
	StarveCleric
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'protected' in item['title'].lower():
		return None
	if "Library of Heaven's Path" in item['tags']:
		return buildReleaseMessageWithType(item, "Library of Heaven's Path", vol, chp, frag=frag, postfix=postfix)
	if 'The Experimental Diaries of A Crazy Lich' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Experimental Diaries of A Crazy Lich', vol, chp, frag=frag, postfix=postfix)
	if 'Tian Ying' in item['tags']:
		return buildReleaseMessageWithType(item, 'Tian Ying', vol, chp, frag=frag, postfix=postfix)
	if 'The Adonis Next Door' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Adonis Next Door', vol, chp, frag=frag, postfix=postfix)
	if 'The Diary of the Truant Death God' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Diary of the Truant Death God', vol, chp, frag=frag, postfix=postfix)
	if 'Dao Tian Xian Tu' in item['tags']:
		return buildReleaseMessageWithType(item, 'Dao Tian Xian Tu', vol, chp, frag=frag, postfix=postfix)
	if 'Rebirth - First Class Magician' in item['tags']:
		return buildReleaseMessageWithType(item, 'Rebirth - First Class Magician', vol, chp, frag=frag, postfix=postfix)
	if 'The Records of the Human Emperor' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Records of the Human Emperor', vol, chp, frag=frag, postfix=postfix)
	return False