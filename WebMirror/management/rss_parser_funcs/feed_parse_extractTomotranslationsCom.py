def extractTomotranslationsCom(item):
	'''
	Parser for 'tomotranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('A Wish To Grab Happiness',                       'Negawakuba no Konote ni Koufuku wo',                      'translated'),
		('Negawakuba no Konote ni Koufuku wo',             'Negawakuba no Konote ni Koufuku wo',                      'translated'),
		('This Hero is invincible but too cautious',       'This Hero is invincible but too cautious',                      'translated'),
		('IT IS A DIFFERENT WORLD AND YET I AM CULTIVATING MONSTERS',       'IT IS A DIFFERENT WORLD AND YET I AM CULTIVATING MONSTERS',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False