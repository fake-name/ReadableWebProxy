def extractSoulPermutation(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Elf-San with Master' in item['tags']:
		return buildReleaseMessageWithType(item, 'Elf-San with Master', vol, chp, frag=frag, postfix=postfix)
	if 'Levelmaker' in item['tags']:
		return buildReleaseMessageWithType(item, 'Levelmaker', vol, chp, frag=frag, postfix=postfix)
	return False
