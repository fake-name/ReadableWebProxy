def extractFamilyfiendlyWordpressCom(item):
	'''
	Parser for 'familyfiendly.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Nanashi no Satsujinki wa Isekai de Kyou mo Warau',       'Nanashi no Satsujinki wa Isekai de Kyou mo Warau',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False