def extractBlancabloggingblockWordpressCom(item):
	'''
	Parser for 'blancabloggingblock.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Mahousekai',                            'Mahousekai no Uketsukejou ni Naritaidesu',                      'translated'),
		('Matsurikaden',                          'The Legend of Bureaucrat Matsurika',                            'translated'),
		('Matsurika Kanriden',                    'The Legend of Bureaucrat Matsurika',                            'translated'),
		('Tsurugi no Joou to Rakuin no Ko',       'Tsurugi no Joou to Rakuin no Ko',                               'translated'),
		('shounen onmyouji',                      'Shounen Onmyouji',                                              'translated'),
		('Kyoto Holmes',                          'Kyoto Teramachi Sanjou no Holmes',                              'translated'),
		('Kyoholmes',                             'Kyoto Teramachi Sanjou no Holmes',                              'translated'),
		('Kaminai',                               'Kamisama no Inai Nichiyoubi',                                   'translated'),
		('Jungfrau',                              'Kenkoku no Jungfrau',                                           'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False