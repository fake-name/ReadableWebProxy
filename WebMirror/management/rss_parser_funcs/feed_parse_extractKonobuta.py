def extractKonobuta(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'status' in item['tags']:
		return buildReleaseMessageWithType(item, 'Sir, I can’t actually read my Status', vol, chp, frag=frag, postfix=postfix)
	if 'uchimusume' in item['tags']:
		return buildReleaseMessageWithType(item, 'For my daughter, I might even be able to defeat the demon king', vol, chp, frag=frag, postfix=postfix)
		
		
	if 'Ryouriban' in item['title']:
		return buildReleaseMessageWithType(item, 'The Cook of the Mercenary Corp', vol, chp, frag=frag, postfix=postfix)
	if 'UchiMusume' in item['title']:
		return buildReleaseMessageWithType(item, 'For my daughter, I might even be able to defeat the demon king', vol, chp, frag=frag, postfix=postfix)
	return False