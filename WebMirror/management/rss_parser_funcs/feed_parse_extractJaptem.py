def extractJaptem(item):
	"""
	# Japtem

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if '[Chinese] Shadow Rogue' in item['tags']:
		return buildReleaseMessageWithType(item, 'Shadow Rogue', vol, chp, frag=frag, postfix=postfix)
	if '[Chinese] Unique Legend' in item['tags'] or 'Unique Legend' in item['tags']:
		return buildReleaseMessageWithType(item, 'Unique Legend', vol, chp, frag=frag, postfix=postfix)
	if "[Japanese] Magi's Grandson" in item['tags'] or "[JP] Magi's Grandson" in item['tags']:
		return buildReleaseMessageWithType(item, "Magi's Grandson", vol, chp, frag=frag, postfix=postfix)
	if '[Japanese / Hosted] Arifureta' in item['tags']:
		return buildReleaseMessageWithType(item, 'Arifureta', vol, chp, frag=frag, postfix=postfix)
	if '[Korean] 21st Century Archmage' in item['tags']:
		return buildReleaseMessageWithType(item, '21st Century Archmage', vol, chp, frag=frag, postfix=postfix)
	if '[Chinese] Kill No More' in item['tags']:
		return buildReleaseMessageWithType(item, 'Kill No More', vol, chp, frag=frag, postfix=postfix)
	if "[JP] Duke's Daughter" in item['tags']:
		return buildReleaseMessageWithType(item, "Good Sense of a Duke's Daughter", vol, chp, frag=frag, postfix=postfix)
	return False
