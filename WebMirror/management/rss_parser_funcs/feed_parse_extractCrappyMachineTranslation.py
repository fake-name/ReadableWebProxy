def extractCrappyMachineTranslation(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'Blade Online' in item['tags']:
		return buildReleaseMessageWithType(item, 'Blade Online', vol, chp, frag=frag, postfix=postfix)
	if "Another World's Savior" in item['tags']:
		return buildReleaseMessageWithType(item, "Another World's Savior", vol, chp, frag=frag, postfix=postfix)
	return False
