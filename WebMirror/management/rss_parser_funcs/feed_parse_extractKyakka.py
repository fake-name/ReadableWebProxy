def extractKyakka(item):
	"""
	# Kyakka

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Yahari Ore no Seishun Love Come wa Machigatteiru' in item['tags'] and 'Translation' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'Yahari Ore no Seishun Rabukome wa Machigatte Iru.', vol, chp, frag=frag, postfix=postfix)
	if 'Yahari Ore no Seishun Love Come wa Machigatteiru' in item['tags'] and 'Light Novel' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'Yahari Ore no Seishun Rabukome wa Machigatte Iru.', vol, chp, frag=frag, postfix=postfix)
	return False
