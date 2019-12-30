def extractTrinityArchive(item):
	"""
	# 'Trinity Archive'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Summoned Slaughterer' in item['tags']:
		return buildReleaseMessageWithType(item, 'Summoned Slaughterer', vol, chp, frag=frag, postfix=postfix)
	return False
