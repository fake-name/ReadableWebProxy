def extractWwwMystifiedtranslationCom(item):
	'''
	Parser for 'www.mystifiedtranslation.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('vrmmo: create a bug every ten hours',               'vrmmo: create a bug every ten hours',                              'translated'),
		('the ceo wants to marry me',                         'the ceo wants to marry me',                                        'translated'),
		('i do not want to inherit the family fortune',       'i do not want to inherit the family fortune',                      'translated'),
		('become a master from hokage',                       'become a master from hokage',                                      'translated'),
		('i am a magic sword',                               'i am a magic sword',                                              'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False