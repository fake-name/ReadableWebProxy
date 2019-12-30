def extractAsherahBlue(item):
	"""
	# 'AsherahBlue's Notebook'

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Juvenile Medical God' in item['tags']:
		return buildReleaseMessageWithType(item, 'Shaonian Yixian', vol, chp, frag=frag, postfix=postfix)
	return False
