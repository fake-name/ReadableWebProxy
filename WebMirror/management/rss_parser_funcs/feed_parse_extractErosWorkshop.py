def extractErosWorkshop(item):
	"""
	# Eros Workshop

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Young God Divine Armaments' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'Young God Divine Armaments', vol, chp, frag=frag, postfix=postfix)
	if 'Communicationally Challenged' in item['tags'] and (chp or vol):
		return buildReleaseMessageWithType(item, 'Komyunan no Ore ga, Koushou Skill ni Zenfuri Shite Tensei Shita Kekka', vol, chp, frag=frag, postfix=postfix)
	return False