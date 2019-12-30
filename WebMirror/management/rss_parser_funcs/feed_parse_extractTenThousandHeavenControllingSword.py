def extractTenThousandHeavenControllingSword(item):
	"""
	# 'Ten Thousand Heaven Controlling Sword'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	return False
