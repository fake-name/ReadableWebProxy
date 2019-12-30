def extractTrungtNguyen(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Underdog Versus Boss' in item['tags']:
		return buildReleaseMessageWithType(item, 'Underdog Versus Boss', vol, chp, frag=frag, postfix=postfix)
	if 'Xiao Qi Wait' in item['tags']:
		return buildReleaseMessageWithType(item, 'Xiao Qi Wait', vol, chp, frag=frag, postfix=postfix)
	if 'Beloved Little Treasure' in item['tags']:
		return buildReleaseMessageWithType(item, 'Beloved Little Treasure', vol, chp, frag=frag, postfix=postfix)
	if 'Real Fake Fiance' in item['tags']:
		return buildReleaseMessageWithType(item, 'Real Fake Fiance', vol, chp, frag=frag, postfix=postfix)
	if 'Demoness Go See The Emperor' in item['tags']:
		return buildReleaseMessageWithType(item, 'Demoness Go See The Emperor', vol, chp, frag=frag, postfix=postfix)
	if 'The Reluctant Bride Book I' in item['tags']:
		if not vol:
			vol = 1
		return buildReleaseMessageWithType(item, 'The Reluctant Bride Book I', vol, chp, frag=frag, postfix=postfix)
	return False
