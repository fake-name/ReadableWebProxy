def extractOniichancornerWordpressCom(item):
	'''
	Parser for 'oniichancorner.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Isekai Tensei Shodouki',                                     'Isekai Tensei Shodouki',                                                    'translated'),
		('Supreme God',                                                'Supreme God',                                                               'translated'),
		('when i woke up i became a silver haired loli vampire',       'when i woke up i became a silver haired loli vampire',                      'translated'),
		('takarakuji',                                                 'Takarakuji de 40-oku Atattandakedo',                                        'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False