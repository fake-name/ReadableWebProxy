def extractGiraffe(item):
	"""
	# Giraffe Corps

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Ti Shen' in item['tags']:
		return buildReleaseMessageWithType(item, 'Tishen', vol, chp, frag=frag, postfix=postfix)
	if 'True Star' in item['tags']:
		return buildReleaseMessageWithType(item, 'Juxing', vol, chp, frag=frag, postfix=postfix)
	if 'Gong Hua' in item['tags']:
		return buildReleaseMessageWithType(item, 'Gong Hua', vol, chp, frag=frag, postfix=postfix)
	if 'Chen Yue Zhi Yao' in item['tags']:
		return buildReleaseMessageWithType(item, 'Chen Yue Zhi Yao', vol, chp, frag=frag, postfix=postfix)
	return False
