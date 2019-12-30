def extractWhiteNightSite(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'What Came to Mind During My Third Time in Another World Was to for Now, Get Naked.' in item['tags']:
		return buildReleaseMessageWithType(item, 'What Came to Mind During My Third Time in Another World Was to for Now, Get Naked.', vol, chp, frag=frag, postfix=postfix)
	return False
