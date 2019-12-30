def extractTomotranslationsWordpressCom(item):
	'''
	Parser for 'tomotranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('This Hero is invincible but too cautious',                       'This Hero is invincible but too cautious',                                     'translated'),
		('A Wish To Grab Happiness',                                       'A Wish To Grab Happiness',                                                     'translated'),
		('IT IS A DIFFERENT WORLD AND YET I AM CULTIVATING MONSTERS',      'It Is A Different World And Yet I Am Cultivating Monsters (LN)',               'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False