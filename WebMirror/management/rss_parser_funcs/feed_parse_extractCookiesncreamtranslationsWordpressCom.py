def extractCookiesncreamtranslationsWordpressCom(item):
	'''
	Parser for 'cookiesncreamtranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('Phoenix Against the World Chapter ',                                           'Across the Stunning Beast Princess: Phoenix Against the World',      'translated'),
		('Descent of the Phoenix Chapter ',                                              'Descent of the Phoenix – 13 Years Old Princess Consort',             'translated'),
		('Modern Cinderella Chapter ',                                                   'Modern Cinderella',                                                  'translated'),
		('Pampered Fei: Brimming with Cuteness Chapter ',                                'Pampered Fei: Brimming with Cuteness',                               'translated'),
		('Pampered Fei Brimming with Cuteness Chapter ',                                 'Pampered Fei: Brimming with Cuteness',                               'translated'),
		('Raising a Fox Consort: The Cold Demonic Wang’s Sweet Love Chapter ',           'Raising a Fox Consort: The Cold Demonic Wang\'s Sweet Love',         'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False