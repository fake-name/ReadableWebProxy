def extractKitchennovelCom(item):
	'''
	Parser for 'kitchennovel.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Strange World Alchemist Chef',                  'Strange World Alchemist Chef',                                 'translated'),
		('Imperial Chef Rookie',                          'Imperial Chef Rookie',                                         'translated'),
		('Daddy Fantasy World',                           'Daddy Fantasy World',                                          'translated'),
		('Here Comes the Lady Chef',                      'Here Comes the Lady Chef',                                     'translated'),
		('Different World Okonomiyaki Chain Store',       'Different World Okonomiyaki Chain Store',                      'translated'),
		('Strange World Little Cooking Saint',            'Strange World Little Cooking Saint',                           'translated'),
		('Fine Food Broadcastor',                         'Fine Food Broadcaster',                                        'translated'),
		('Kitchen Xiuzhen',                               'Kitchen Xiuzhen',                                              'translated'),
		('Reborn - Super Chef',                           'Reborn - Super Chef',                                          'translated'),
		('The Taming of the Black Bellied Scholar',       'The Taming of the Black Bellied Scholar',                      'translated'),
		('The Feast',                                     'The Feast',                                                    'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False