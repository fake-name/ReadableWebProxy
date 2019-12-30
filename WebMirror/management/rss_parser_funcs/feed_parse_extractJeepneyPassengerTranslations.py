def extractJeepneyPassengerTranslations(item):
	'''
	Parser for 'Jeepney Passenger Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "Wizard's Tale" in item['tags']:
		return buildReleaseMessageWithType(item, "Wizard's Tale", vol, chp, frag=frag, postfix=postfix)

	return False