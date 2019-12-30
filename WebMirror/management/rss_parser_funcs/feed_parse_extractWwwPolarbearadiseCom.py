def extractWwwPolarbearadiseCom(item):
	'''
	Parser for 'www.polarbearadise.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The World Is A Bit Sweet',               'The World Is A Bit Sweet',                      'translated'),
		('Feng Mang',                              'Feng Mang',                                     'translated'),
		('Number One Zombie Wife (第一尸妻)',      'Number One Zombie Wife',                        'translated'),
		('goldenassistant',                        'Golden Assistant',                              'translated'),
		('Oh, My Dear!',                           'Oh, My Dear!',                                  'translated'),
		('Blood Contract',                         'Blood Contract',                                        'translated'),
		('Liu Li Loves Jun',                       'Liu Li Loves Jun',                                      'translated'),
		('Idiot I Love You!',                      'Idiot I Love You!',                                     'translated'),
		('Number One Zombie Wife',                 'Number One Zombie Wife',                                'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False