def extractBeehugger(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Summary' in item['tags']:
		return None
		
		
	if 'Battle Emperor' in item['tags']:
		return buildReleaseMessageWithType(item, 'Battle Emperor', vol, chp, frag=frag, postfix=postfix)
	if 'Battle Emperor Chapter ' in item['title']:
		return buildReleaseMessageWithType(item, 'Battle Emperor', vol, chp, frag=frag, postfix=postfix)
	if 'Sword Spirit' in item['tags']:
		return buildReleaseMessageWithType(item, 'Sword Spirit', vol, chp, frag=frag, postfix=postfix)
	if 'Sword Spirit Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Sword Spirit', vol, chp, frag=frag, postfix=postfix)
	# if 'Forty Millenniums of Cultivation' in item['tags'] and (chp or vol):
	# 	return buildReleaseMessageWithType(item, 'Forty Millenniums of Cultivation', vol, chp, frag=frag, postfix=postfix)
	return False