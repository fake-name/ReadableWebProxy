def extractGuroTranslation(item):
	"""
	# 'GuroTranslation'

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	ltags = [tmp.lower() for tmp in item['tags']]
	if 'tensei shitara slime datta ken' in ltags:
		return buildReleaseMessageWithType(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)
	if '1000 nin no homunkurusu no shoujo tachi ni kakomarete isekai kenkoku' in ltags:
		return buildReleaseMessageWithType(item, '1000 nin no Homunkurusu no Shoujo tachi ni Kakomarete Isekai Kenkoku', vol, chp, frag=frag, postfix=postfix)
	return False
