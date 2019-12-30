def extractLickymeeTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Medusa' in item['tags']:
		return buildReleaseMessageWithType(item, 'Regarding the Story of My Wife, Medusa', vol, chp, frag=frag, postfix=postfix)
	if 'OreOjou' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ore ga Ojousama Gakkou ni "Shomin Sample" Toshite Rachirareta Ken', vol, chp, frag=frag, postfix=postfix)
	return False
