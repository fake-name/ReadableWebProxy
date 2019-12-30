def extractWolfieTranslation(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'The amber sword' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Amber Sword', vol, chp, frag=frag, postfix=postfix)
	if 'The latest game is too amazing' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Latest Game is too Amazing', vol, chp, frag=frag, postfix=postfix)
	if 'The strategy to become good at magic' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Strategy to Become Good at Magic', vol, chp, frag=frag, postfix=postfix)
	if 'The Wolf Prince and The Ice Princess' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Wolf Prince and The Ice Princess', vol, chp, frag=frag, postfix=postfix)
		
		
	return False