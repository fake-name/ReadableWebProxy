def extractJingletranslationsWordpressCom(item):
	'''
	Parser for 'jingletranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Breaking Off the Engagement… Bring it on!',       'Breaking Off the Engagement… Bring it on!',                      'translated'),
		('I Favor the Villainess',                          'I Favor the Villainess',                                         'translated'),
		('City of Slumber',                                 'City of Slumber',                                                'translated'),
		('Villainess’s Sweet Everyday',                     'Villainess\'s Sweet Everyday',                                   'translated'),
		('Outaishihi ni Nante Naritakunai!!',               'Outaishihi ni Nante Naritakunai!!',                              'translated'),
		('First Love × First Love',                         'First Love × First Love',                                        'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False