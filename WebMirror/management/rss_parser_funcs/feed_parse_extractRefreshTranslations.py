def extractRefreshTranslations(item):
	"""
	'Refresh Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Aspiration for Nation and Beauty' in item['tags']:
		return buildReleaseMessageWithType(item, 'Aspiration for Nation and Beauty', vol, chp, frag=frag, postfix=postfix)
	return False
