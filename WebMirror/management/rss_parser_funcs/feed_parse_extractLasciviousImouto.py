def extractLasciviousImouto(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'].replace('-', '.'))
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'The Beast of the 17th District' in item['tags'] or 'the beast of the 17th district' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'The Beast of the 17th District', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Le Festin de Vampire' in item['tags']:
		return buildReleaseMessageWithType(item, 'Le Festin de Vampire', vol, chp, frag=frag, postfix=postfix)
	return False
