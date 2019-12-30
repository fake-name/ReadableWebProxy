def extractElementalCobalt(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].lower().startswith('arifureta chapter') or 'Arifureta Translation' in item['tags']:
		return buildReleaseMessageWithType(item, 'Arifureta Shokugyou de Sekai Saikyou', vol, chp, frag=frag, postfix=postfix)
		
	if item['title'].lower().startswith('reincarnated as a villager – strongest slow-life'):
		return buildReleaseMessageWithType(item, 'Reincarnated as a Villager ~ Strongest Slow-life', vol, chp, frag=frag, postfix=postfix)
		
	if item['title'].lower().startswith('requiem to the stars'):
		return buildReleaseMessageWithType(item, 'Requiem to the Stars', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Hawtness' in item['tags']:
		return buildReleaseMessageWithType(item, 'Hawtness', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Time and Place' in item['tags']:
		return buildReleaseMessageWithType(item, 'Time and Place', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Tales of an Enchantress' in item['tags']:
		return buildReleaseMessageWithType(item, 'Tales of an Enchantress', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
		
	return False