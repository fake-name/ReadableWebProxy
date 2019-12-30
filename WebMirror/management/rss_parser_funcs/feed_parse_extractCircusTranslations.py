def extractCircusTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'German Translation' in item['tags']:
		return None
	if 'Turkish Translation' in item['tags']:
		return None
	if 'Spanish translation' in item['tags']:
		return None
	if chp or vol:
		return buildReleaseMessageWithType(item, 'Tensei Shitara Slime Datta Ken', vol, chp, frag=frag, postfix=postfix)
	return False
