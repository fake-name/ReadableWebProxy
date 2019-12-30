def extractMahouKoukoku(item):
	"""
	# MahouKoukoku

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Shiro no Koukoku Monogatari ' in item['title']:
		return buildReleaseMessageWithType(item, 'Shiro no Koukoku Monogatari', vol, chp, frag=frag, postfix=postfix)
	return False
