def extractPenjournalhappyWordpressCom(item):
	'''
	Parser for 'penjournalhappy.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Villain Reformation System',              'Pulling Together a Villain Reformation Strategy',                      'translated'),
		('Villain Reformation Strategy',            'Pulling Together a Villain Reformation Strategy',                      'translated'),
		('Want to Ascend? Then Fall in Love',       'Want to Ascend? Then Fall in Love',                      'translated'),
		('Golden Stage',                            'Golden Stage',                                           'translated'),
		('a tale of strategies for the throne',     'a tale of strategies for the throne',                    'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False