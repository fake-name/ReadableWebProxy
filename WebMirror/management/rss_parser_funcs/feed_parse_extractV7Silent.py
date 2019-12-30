def extractV7Silent(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'The Demon Queen is My Fiancée!' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Demon Queen is My Fiancée!', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Getcha Skills' in item['tags']:
		return buildReleaseMessageWithType(item, 'Getcha Skills', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
