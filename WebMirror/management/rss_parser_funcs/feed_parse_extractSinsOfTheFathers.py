def extractSinsOfTheFathers(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	return buildReleaseMessageWithType(item, 'Sins of the Fathers '.lower(), vol, chp, frag=frag, postfix=postfix, tl_type='oel')
