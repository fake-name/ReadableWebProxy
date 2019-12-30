def extractKakkokari仮(item):
	"""
	Parser for 'Kakkokari (仮)'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Stunning Edge' in item['tags']:
		return buildReleaseMessageWithType(item, 'Stunning Edge', vol, chp, frag=frag, postfix=postfix)
	if 'Honey Rabbit!' in item['tags']:
		return buildReleaseMessageWithType(item, 'Honey Rabbit!', vol, chp, frag=frag, postfix=postfix)
	if 'Both are Foxes' in item['tags']:
		return buildReleaseMessageWithType(item, 'Both are Foxes', vol, chp, frag=frag, postfix=postfix)
	if 'Ancient One' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ancient One', vol, chp, frag=frag, postfix=postfix)
	if 'Koushirou Kujou the Detective Butler' in item['tags']:
		return buildReleaseMessageWithType(item, 'Koushirou Kujou the Detective Butler', vol, chp, frag=frag, postfix=postfix)
	return False