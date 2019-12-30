def extractMikazuki2017WordpressCom(item):
	'''
	Parser for 'mikazuki2017.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('CL : ',        'Crescent Love',                          'oel'),
		('CL: Chapter',  'Crescent Love',                          'oel'),
		('HIHEZL : ',    'He is His Excellency Zhi Li',            'translated'),
		('HIHEZL: ',     'He is His Excellency Zhi Li',            'translated'),
		('TUMBT: ',      'The Ugly Man’s Big Transformation',      'translated'),
		('TUMBT : ',     'The Ugly Man’s Big Transformation',      'translated'),
		('BTM : ',       'Beyond the Moon',                        'translated'),
		('BTM: ',        'Beyond the Moon',                        'translated'),
		('BMHS : ',      'Beloved Marriage in High Society',       'translated'),
		('BHMS: ',       'Beloved Marriage in High Society',       'translated'),
		('BHMS : ',      'Beloved Marriage in High Society',       'translated'),
		('Jubo : ',      'Jubo',                                   'translated'),
		('S&OP : ',      'Superstar and Ordinary People',          'translated'),
		('SP: ',         'Special Property',                       'translated'),
		('19Y: ',        '19 Years',                               'translated'),
		('LMTW : ',      'Love is More Than a Word',               'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent in item['title']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False