def extractAdamantineDragonintheCrystalWorld(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Crystal World' in item['tags']:
		return buildReleaseMessageWithType(item, 'Adamantine Dragon in the Crystal World', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
