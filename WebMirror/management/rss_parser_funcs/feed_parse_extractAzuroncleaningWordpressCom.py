def extractAzuroncleaningWordpressCom(item):
	'''
	Parser for 'azuroncleaning.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	if item['tags'] == ['Uncategorized']:
		titlemap = [
			('Qinglian Chronicles Chapter ',               'Qinglian Chronicles',                   'translated'),
			('How To Die As Heavy As Mount Tai Chapter ',  'How To Die As Heavy As Mount Tai',      'translated'),
		]
	
		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	tagmap = [
		('HTDASAMT',                               'How To Die As Heavy As Mount Tai',                      'translated'),
		('How to die as heavy as mount tai',       'How To Die As Heavy As Mount Tai',                      'translated'),
		('PRC',                                    'PRC',                                                   'translated'),
		('Loiterous',                              'Loiterous',                                             'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False