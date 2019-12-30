def extractCloudManor(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Book of Sun & Moon Swordplay' in item['tags']:
		return buildReleaseMessageWithType(item, 'Book of Sun & Moon Swordplay', vol, chp, frag=frag, postfix=postfix)
	if 'It is a Straight Road' in item['tags']:
		return buildReleaseMessageWithType(item, 'It is a Straight Road', vol, chp, frag=frag, postfix=postfix)
	if 'Pursuit of Liao Yue Murderer' in item['tags']:
		return buildReleaseMessageWithType(item, 'Pursuit of Liao Yue Murderer', vol, chp, frag=frag, postfix=postfix)
	if 'Rice Pot Next Door' in item['tags']:
		return buildReleaseMessageWithType(item, 'Rice Pot Next Door', vol, chp, frag=frag, postfix=postfix)
	if 'Man from Wild South' in item['tags']:
		return buildReleaseMessageWithType(item, 'Man from the Wild South', vol, chp, frag=frag, postfix=postfix)
	return False