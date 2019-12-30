def extractIzra709(item):
	"""
	# izra709 | B Group no Shounen Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if not postfix and '–' in item['title']:
		postfix = item['title'].split('–')[-1]
	if 'monohito chapter' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Monogatari no Naka no Hito', vol, chp, frag=frag, postfix=postfix)
	if 'b group chapter' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'B Group no Shounen', vol, chp, frag=frag, postfix=postfix)
	if 'assassin chapter' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Other World Assassin Life of a Man who was a Shut-in', vol, chp, frag=frag, postfix=postfix)
	return False
