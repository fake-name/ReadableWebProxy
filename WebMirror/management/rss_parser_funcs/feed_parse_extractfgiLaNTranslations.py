def extractfgiLaNTranslations(item):
	"""
	# 'fgiLaN translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'kimi no na wa' in item['tags']:
		return buildReleaseMessageWithType(item, 'kimi no na wa', vol, chp, frag=frag, postfix=postfix)
	if 'shuumatsu nani shitemasu ka? isogashii desu ka? sukutte moratte ii desu ka?' in item['tags']:
		return buildReleaseMessageWithType(item, 'shuumatsu nani shitemasu ka? isogashii desu ka? sukutte moratte ii desu ka?', vol, chp, frag=frag, postfix=postfix)
	return False
