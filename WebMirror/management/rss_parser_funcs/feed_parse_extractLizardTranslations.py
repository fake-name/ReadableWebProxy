def extractLizardTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'The Strongest Violent Soldier' in item['tags']:
		return buildReleaseMessageWithType(item, 'The Strongest Violent Soldier', vol, chp, frag=frag, postfix=postfix)
	return False
