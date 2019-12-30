def extractArkMachineTranslations(item):
	"""
	# Ark Machine Translations

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'ark volume' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Ark', vol, chp, frag=frag, postfix=postfix)
	if 'ark the legend volume' in item['title'].lower() or 'ATL' in item['tags']:
		return buildReleaseMessageWithType(item, 'Ark The Legend', vol, chp, frag=frag, postfix=postfix)
	if 'lms volume' in item['title'].lower():
		return buildReleaseMessageWithType(item, 'Legendary Moonlight Sculptor', vol, chp, frag=frag, postfix=postfix)
	return False
