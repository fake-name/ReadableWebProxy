def extractDragomirCM(item):
	"""
	# DragomirCM

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if not postfix and ':' in item['title']:
		postfix = item['title'].split(':')[-1]
	if 'Magic Academy' in item['tags']:
		return buildReleaseMessageWithType(item, 'I was reincarnated as a Magic Academy!', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if '100 Luck' in item['tags']:
		return buildReleaseMessageWithType(item, '100 Luck and the Dragon Tamer Skill!', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False
