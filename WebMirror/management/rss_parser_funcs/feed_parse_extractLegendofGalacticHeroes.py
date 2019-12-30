def extractLegendofGalacticHeroes(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Part 1 - Dawn' in item['tags']:
		if not vol:
			vol = 1
		return buildReleaseMessageWithType(item, 'Legend of Galactic Heroes', vol, chp, frag=frag, postfix=postfix)
	if 'Part 2 - Ambition' in item['tags']:
		if not vol:
			vol = 2
		return buildReleaseMessageWithType(item, 'Legend of Galactic Heroes', vol, chp, frag=frag, postfix=postfix)
	return False
