def extractFriendshipIsPower(item):
	"""
	'Friendship Is Power'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Forty Millenniums of Cultivation Chapters' in item['tags']:
		return buildReleaseMessageWithType(item, 'Forty Millenniums of Cultivation Chapters', vol, chp, frag=frag, postfix=postfix)
	return False
