def extractWLTranslations(item):
	"""
	# 'WL Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Chapter Releases' in item['tags'] and ('OSI' in item['tags'] or item['title'].startswith('OSI Chapter')):
		return buildReleaseMessageWithType(item, 'One Sword to Immortality', vol, chp, frag=frag, postfix=postfix)
	return False
