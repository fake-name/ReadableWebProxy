def extractMakinaTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if "I aim to be an adventurer with the jobclass of 'Jobless'" in item['tags']:
		return buildReleaseMessageWithType(item, 'I Aim to Be an Adventurer with the Jobclass of "Jobless"', vol, chp, frag=frag, postfix=postfix)
	return False
