def extractTseirpTranslations(item):
	"""
	# 'Tseirp Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'IS SS' in item['title'] and not postfix:
		postfix = 'Side Story'
	if item['title'].startswith('IS '):
		return buildReleaseMessageWithType(item, 'Invincible Saint ~Salaryman, the Path I Walk to Survive in This Other World~', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('GC '):
		return buildReleaseMessageWithType(item, "I've Became Able to Do Anything With My Growth Cheat, but I Can't Seem to Get Out of Being Jobless", vol, chp, frag=frag, postfix=postfix)
	if 'Growth Cheat' in item['tags']:
		return buildReleaseMessageWithType(item, "I've Became Able to Do Anything With My Growth Cheat, but I Can't Seem to Get Out of Being Jobless", vol, chp, frag=frag, postfix=postfix)
	if 'Live Dungeon' in item['tags']:
		return buildReleaseMessageWithType(item, 'Live Dungeon', vol, chp, frag=frag, postfix=postfix)
	if 'Slow Life Frontier' in item['tags']:
		return buildReleaseMessageWithType(item, 'I was kicked out of the Hero’s party because I wasn’t a true companion so I decided to have a slow life at the frontier.', vol, chp, frag=frag, postfix=postfix)
	return False