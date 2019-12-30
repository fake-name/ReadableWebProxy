def extractDisappointingTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'GSB' in item['tags']:
		return buildReleaseMessageWithType(item, 'Galaxy Shattering Blade', vol, chp, frag=frag, postfix=postfix)
	return False
