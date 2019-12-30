def extractTotokk(item):
	"""
	# Totokk's Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	if 'Shen Yin Wang Zuo Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Shen Yin Wang Zuo', vol, chp, frag=frag, postfix=postfix)
	if '[SWYZ] Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Shen Yin Wang Zuo', vol, chp, frag=frag, postfix=postfix)
	if '[SYWZ]' in item['title']:
		return buildReleaseMessageWithType(item, 'Shen Yin Wang Zuo', vol, chp, frag=frag, postfix=postfix)
	if 'Shen Yin Wang Zuo, Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Shen Yin Wang Zuo', vol, chp, frag=frag, postfix=postfix)
	if 'SYWZ' in item['tags']:
		return buildReleaseMessageWithType(item, 'Shen Yin Wang Zuo', vol, chp, frag=frag, postfix=postfix)
		
	return False