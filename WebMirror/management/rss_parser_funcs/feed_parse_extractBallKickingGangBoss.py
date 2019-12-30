def extractBallKickingGangBoss(item):
	"""
	# "'Ball'-Kicking Gang Boss"
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'jinsei' in item['tags']:
		return buildReleaseMessageWithType(item, "I'll Live My Second Life!", vol, chp, frag=frag, postfix=postfix)
	return False
