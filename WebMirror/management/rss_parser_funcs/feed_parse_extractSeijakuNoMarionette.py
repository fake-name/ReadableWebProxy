def extractSeijakuNoMarionette(item):
	'''
	Parser for 'Seijaku no Marionette'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	tagmap = [
		('Koushirou Kujou the Detective Butler',       'Koushirou Kujou the Detective Butler', 'translated'),
		('The Impostor Luca and a Black Monster',       'The Impostor Luca and a Black Monster', 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False