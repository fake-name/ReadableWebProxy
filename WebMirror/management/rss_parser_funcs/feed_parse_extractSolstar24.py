def extractSolstar24(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'jin xiu wei yang' in item['tags']:
		return buildReleaseMessageWithType(item, 'Jin Xiu Wei Yang', vol, chp, frag=frag, postfix=postfix)
	if 'dao qing' in item['tags']:
		return buildReleaseMessageWithType(item, 'Dao Qing', vol, chp, frag=frag, postfix=postfix)
	return False
