def extractSubudai11(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Mai Kitsune Waifu Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'My Fox Immortal Wife', vol, chp, frag=frag, postfix=postfix)
	if 'My Beautiful Teacher Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'My Beautiful Teacher', vol, chp, frag=frag, postfix=postfix)
	if 'Awakening – 仿如昨日' in item['title']:
		return buildReleaseMessageWithType(item, 'Awakening – 仿如昨日', vol, chp, frag=frag, postfix=postfix)
	if 'Awakening' in item['title']:
		return buildReleaseMessageWithType(item, 'Awakening – 仿如昨日', vol, chp, frag=frag, postfix=postfix)
	return False
