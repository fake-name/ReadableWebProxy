def extractAzureSky(item):
	"""
	# extractAzureSky

	"""
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Shinde Hajimaru'.lower() in item['title'].lower():
		postfix = ''
		if 'prologue' in item['title'].lower():
			postfix = 'Prologue'
		return buildReleaseMessageWithType(item, 'Shinde Hajimaru Isekai Tensei', vol, chp, frag=frag, postfix=postfix)
	return False
