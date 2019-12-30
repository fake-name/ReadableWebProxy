def extractWuxiaLovers(item):
	"""
	Wuxia Lovers
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('CGA Chapter') or item['title'].startswith('CGA: Chapter'):
		return buildReleaseMessageWithType(item, 'Conquer God, Asura, and 1000 Beauties', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Etranger Chapter'):
		return buildReleaseMessageWithType(item, 'Etranger', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Q11 Chapter'):
		return buildReleaseMessageWithType(item, 'Queen of No.11 Agent 11', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('STS Chapter'):
		return buildReleaseMessageWithType(item, 'Sky Traversing Sword Master', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('DGM Chapter'):
		return buildReleaseMessageWithType(item, 'Descent of the God of Magic', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('The First Hunter Chapter'):
		return buildReleaseMessageWithType(item, 'The First Hunter', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Slaughter System – '):
		return buildReleaseMessageWithType(item, 'Slaughter System', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if item['title'].startswith('Getcha Skills Chapter '):
		return buildReleaseMessageWithType(item, 'Getcha Skills', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if item['title'].startswith('Empyrean Ascent Chapter'):
		return buildReleaseMessageWithType(item, 'Empyrean Ascent', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if item['title'].startswith('[Guardian] Chapter'):
		return buildReleaseMessageWithType(item, '[Guardian]', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
