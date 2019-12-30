def extractKyOptionsLibrary(item):
	"""
	# 'kyoptionslibrary.blogspot.com'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Death March' in item['tags']:
		return buildReleaseMessageWithType(item, 'Death March kara Hajimaru Isekai Kyusoukyoku (LN)', vol, chp, frag=frag, postfix=postfix)
	return False
