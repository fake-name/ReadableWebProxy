def extractUltimateArcane(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Isekai ni kanaderu densetsu ~toki wo tomeru mono~' in item['tags']:
		return buildReleaseMessageWithType(item, 'Isekai ni kanaderu densetsu ~toki wo tomeru mono~', vol, chp, frag=frag, postfix=postfix)
	if 'JIKUU MAHOU DE ISEKAI TO CHIKYUU WO ITTARIKITARI' in item['tags']:
		return buildReleaseMessageWithType(item, 'Jikuu Mahou de Isekai to Chikyuu wo ittarikitari', vol, chp, frag=frag, postfix=postfix)
	return False
