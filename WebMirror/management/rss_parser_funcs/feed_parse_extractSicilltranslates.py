def extractSicilltranslates(item):
	'''
	Parser for 'SicillTranslates'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
		
	tagmap = [
		('So What if It\'s an RPG World!?',       'So What if It\'s an RPG World!?', 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False