def extractTranslationNations(item):
	"""
	# Translation Nations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Stellar Transformation' in item['tags']:
		return buildReleaseMessageWithType(item, 'Stellar Transformations', vol, chp, frag=frag, postfix=postfix)
	if 'The Legendary Thief' in item['tags']:
		return buildReleaseMessageWithType(item, 'Virtual World - The Legendary Thief', vol, chp, frag=frag, postfix=postfix)
	if 'SwallowedStar' in item['tags']:
		return buildReleaseMessageWithType(item, 'Swallowed Star', vol, chp, frag=frag, postfix=postfix)
	if 'Transcending The Nine Heavens' in item['tags']:
		return buildReleaseMessageWithType(item, 'Transcending The Nine Heavens', vol, chp, frag=frag, postfix=postfix)
	if 'God and Devil World' in item['tags']:
		return buildReleaseMessageWithType(item, 'God and Devil World', vol, chp, frag=frag, postfix=postfix)
	if 'Limitless Sword God' in item['tags']:
		return buildReleaseMessageWithType(item, 'Limitless Sword God', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('undefeated god of war') and 'Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Undefeated God of War', vol, chp, frag=frag, postfix=postfix)
	if 'Undefeated God of War' in item['tags']:
		return buildReleaseMessageWithType(item, 'Undefeated God of War', vol, chp, frag=frag, postfix=postfix)
	if 'Path to Heaven' in item['tags']:
		return buildReleaseMessageWithType(item, 'Path to Heaven', vol, chp, frag=frag, postfix=postfix)
	if 'The Ultimate Evolution' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Ultimate Evolution', vol, chp, frag=frag, postfix=postfix)
	if 'Plundering the Dao of the Immortal Path' in item['tags']:
		return buildReleaseMessageWithType(item, 'Plundering the Dao of the Immortal Path', vol, chp, frag=frag, postfix=postfix)
	if 'Only I Shall Be Immortal' in item['tags']:
		return buildReleaseMessageWithType(item, 'Only I Shall Be Immortal', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('the ultimate evolution volume') and 'Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'The Ultimate Evolution', vol, chp, frag=frag, postfix=postfix)
	return False