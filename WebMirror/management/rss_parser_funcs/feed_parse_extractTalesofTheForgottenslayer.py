def extractTalesofTheForgottenslayer(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'the botched summoning' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Botched Summoning', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
