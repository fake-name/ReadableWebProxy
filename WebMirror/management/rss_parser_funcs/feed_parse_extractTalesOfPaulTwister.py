def extractTalesOfPaulTwister(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'The Fate of Paul Twister' in item['tags']:
		assert not vol
		vol = 2
		return buildReleaseMessageWithType(item, 'The Tales of Paul Twister', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'The Return of Paul Twister' in item['tags']:
		assert not vol
		vol = 3
		return buildReleaseMessageWithType(item, 'The Tales of Paul Twister', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
