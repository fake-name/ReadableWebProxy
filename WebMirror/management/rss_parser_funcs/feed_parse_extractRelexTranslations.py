def extractRelexTranslations(item):
	'''
	Parser for 'Relex Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	tagmap = [
		('Journey to the West',              'Journey to the West',           'translated'),
		('Legend of Galactic Heroes',        'Legend of Galactic Heroes',     'translated'),
		('Winds Against Progress',           'Winds Against Progress',        'translated'),
		('All you need is kill',             'All you need is kill',          'translated'),
		('Empire in Progress',               'Empire in Progress',            'translated'),
		('Romance of The Three Kingdoms',    'Romance of The Three Kingdoms', 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False