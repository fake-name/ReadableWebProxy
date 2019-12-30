def extractChrononTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	item['title'] = item['title'].replace('’', '')
	if 'Weapons cheat'.lower() in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Modern weapons cheat in another world', vol, chp, frag=frag, postfix=postfix)
	if 'Heavenly Tribulation'.lower() in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Heavenly Tribulation', vol, chp, frag=frag, postfix=postfix)
	if 'I can speak'.lower() in item['title'].lower():
		return buildReleaseMessageWithType(item, 'I Can Speak with Animals and Demons', vol, chp, frag=frag, postfix=postfix)
	if 'I Bought a Girl'.lower() in item['title'].lower():
		return buildReleaseMessageWithType(item, 'I Bought a Girl', vol, chp, frag=frag, postfix=postfix)
	if 'Girl Corps'.lower() in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Girl Corps', vol, chp, frag=frag, postfix=postfix)
	if 'Modern Weapons'.lower() in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Modern weapons cheat in another world', vol, chp, frag=frag, postfix=postfix)
	if 'Upper World'.lower() in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Reincarnation ~ From the lower world to the upper world', vol, chp, frag=frag, postfix=postfix)
	if 'I work as a healer'.lower() in item['title'].lower():
		return buildReleaseMessageWithType(item, "I Work As A Healer In Another World's Labyrinth City", vol, chp, frag=frag, postfix=postfix)
	return False
