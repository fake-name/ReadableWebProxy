def extractWwwVmnovelsCom(item):
	'''
	Parser for 'www.vmnovels.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Big Landlord',                         'The Big Landlord',                                        'translated'),
		('Let Me Shoulder This Blame',               'Let Me Shoulder This Blame',                              'translated'),
		('Quickly Wear The Face of The Devil',       'Quickly Wear The Face of The Devil',                      'translated'),
		('didn’t love you enough',                   'didn\'t love you enough',                                 'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False