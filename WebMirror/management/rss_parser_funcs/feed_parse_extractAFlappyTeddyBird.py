def extractAFlappyTeddyBird(item):
	"""
	# A Flappy Teddy Bird

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'The Black Knight who was stronger than even the Hero' in item['title']:
		return buildReleaseMessageWithType(item, 'The Black Knight Who Was Stronger than Even the Hero', vol, chp, frag=frag, postfix=postfix)
	return False
