def extractYumeabyss(item):
	"""
	Yumeabyss
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if "Black Bellied Prince's Stunning Abandoned Consort" in item['tags']:
		return buildReleaseMessageWithType(item, "Black Bellied Prince's Stunning Abandoned Consort", vol, chp, frag=frag, postfix=postfix)
	if 'The Cry of the Phoenix Which Reached the Ninth Heaven' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Cry of the Phoenix Which Reached the Ninth Heaven', vol, chp, frag=frag, postfix=postfix)
	if 'Island: End of Nightmare' in item['tags']:
		return buildReleaseMessageWithType(item, 'Island: End of Nightmare', vol, chp, frag=frag, postfix=postfix)
	if 'Xiao Qi, Wait' in item['tags']:
		return buildReleaseMessageWithType(item, 'Xiao Qi, Wait', vol, chp, frag=frag, postfix=postfix)
	return False
