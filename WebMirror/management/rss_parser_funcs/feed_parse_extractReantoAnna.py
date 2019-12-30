def extractReantoAnna(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Only I am not attacked in a world over runned by zombies' in item['tags'] or 'Chapter' in item['title'] and len(item['tags']) == 1 and 'Uncategorized' in item['tags'
	    ]:
		return buildReleaseMessageWithType(item, 'Only I am not attacked in a world overflowing with zombies', vol, chp, frag=frag, postfix=postfix)
	return False
