def extractThyaeria(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Tales of Demons and Gods' in item['tags']:
		return buildReleaseMessageWithType(item, 'Tales of Demons and Gods', vol, chp, frag=frag, postfix=postfix)
	if 'Warlock of the Magus World' in item['tags']:
		return buildReleaseMessageWithType(item, 'Warlock of the Magus World', vol, chp, frag=frag, postfix=postfix)
	return False
