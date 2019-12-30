def extractForKalimdor(item):
	"""
	For Kalimdor
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('Bringing The Farm To Live In Another World'):
		return buildReleaseMessageWithType(item, 'Bringing The Farm To Live In Another World', vol, chp, frag=frag, postfix=postfix)
	if 'BTFTLIAW' in item['tags']:
		return buildReleaseMessageWithType(item, 'Bringing The Farm To Live In Another World', vol, chp, frag=frag, postfix=postfix)
	return False
