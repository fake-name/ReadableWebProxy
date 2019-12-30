def extractRuisTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'A Mismatched Marriage: Records of Washed Away Injustices' in item['tags']:
		return buildReleaseMessageWithType(item, 'A Mismatched Marriage: Records of Washed Away Injustices', vol, chp, frag=frag, postfix=postfix)
	return False
