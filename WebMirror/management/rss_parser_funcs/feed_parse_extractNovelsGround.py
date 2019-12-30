def extractNovelsGround(item):
	"""
	# 'Novels Ground'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Legend of the Cultivation God' in item['tags'] or 'LOTCG' in item['tags']:
		return buildReleaseMessageWithType(item, 'Legend of the Cultivation God', vol, chp, frag=frag, postfix=postfix)
	if 'Miracle Throne' in item['tags'] or 'LOTCG' in item['tags']:
		return buildReleaseMessageWithType(item, 'Miracle Throne', vol, chp, frag=frag, postfix=postfix)
	return False
