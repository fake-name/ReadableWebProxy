def extractSteambunlightnovelCom(item):
	'''
	Parser for 'steambunlightnovel.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('tang yin\'s adventure in another world',       'Tang Yin\'s Adventure In Another World',                      'translated'),
		('devil\'s son-in-law',                          'Devil\'s Son-in-Law',                                         'translated'),
		('the cold reagent keeps a fox as a consort',    'the cold reagent keeps a fox as a consort',                   'translated'),
		('Martial God Space',                            'Martial God Space',                                           'translated'),
		('Demon\'s Diary',                               'Demon\'s Diary',                                              'translated'),
		('the king of hell\'s genius pampered wife',     'the king of hell\'s genius pampered wife',                    'translated'),
		('History’s Strongest Senior Brother',           'History’s Strongest Senior Brother',                          'translated'),
		('traveler',                                     'traveler',                                                    'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False