def extractRumanshisLair(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('Jobless'):
		return buildReleaseMessageWithType(item, 'I Aim to Be an Adventurer with the Jobclass of "Jobless"', vol, chp, frag=frag, postfix=postfix)
	if 'The Harem Was a Forced Goal' in item['tags'] or 'THWAFG' in item['title']:
		if 'SS' in item['title'] and not postfix:
			postfix = 'Side Story'
		return buildReleaseMessageWithType(item, 'The Harem Was a Forced Goal', vol, chp, frag=frag, postfix=postfix)
	if 'Isekai Cheat' in item['tags'] or 'Isekai Cheat' in item['title']:
		return buildReleaseMessageWithType(item, 'Different World Reincarnation ~ Enjoying the new world as a cheat ~', vol, chp, frag=frag, postfix=postfix)
	if 'Other Worlds Monster Breeder' in item['tags'] or 'Other World’s Monster Breeder (PokeGod)'.lower() in item['title'].lower():
		return buildReleaseMessageWithType(item, "Other World's Monster Breeder", vol, chp, frag=frag, postfix=postfix)
	if 'When I returned home, what I found was fantasy!?'.lower() in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Kaettekite mo Fantasy!?', vol, chp, frag=frag, postfix=postfix)
	return False
