def extractLostInTranslation(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Third Prince Elmer' in item['tags']:
		return buildReleaseMessageWithType(item, 'Third Prince Elmer', vol, chp, frag=frag, postfix=postfix)
	if 'Otoko Aruji' in item['tags']:
		return buildReleaseMessageWithType(item, 'Otoko Aruji', vol, chp, frag=frag, postfix=postfix)
	if "Sword Saint's Disciple" in item['tags']:
		return buildReleaseMessageWithType(item, "Sword Saint's Disciple", vol, chp, frag=frag, postfix=postfix)
	if 'Doll Dungeon' in item['tags']:
		return buildReleaseMessageWithType(item, 'Doll Dungeon', vol, chp, frag=frag, postfix=postfix)
	return False
