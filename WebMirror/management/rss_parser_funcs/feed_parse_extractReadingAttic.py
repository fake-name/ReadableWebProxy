def extractReadingAttic(item):
	"""
	Reading Attic
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'A Tale of Two Phoenixes （凤囚凰）' in item['tags']:
		return buildReleaseMessageWithType(item, 'A Tale of Two Phoenixes', vol, chp, frag=frag, postfix=postfix)
	if 'Ghost Invasion （有鬼来袭）' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ghost Invasion', vol, chp, frag=frag, postfix=postfix)
	if 'Stunning Edge （绝色锋芒）' in item['tags']:
		return buildReleaseMessageWithType(item, 'Stunning Edge', vol, chp, frag=frag, postfix=postfix)
	return False
