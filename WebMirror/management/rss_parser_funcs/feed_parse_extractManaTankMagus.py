def extractManaTankMagus(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Mana Tank Magus' in item['tags']:
		return buildReleaseMessageWithType(item, 'Mana Tank Magus', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
