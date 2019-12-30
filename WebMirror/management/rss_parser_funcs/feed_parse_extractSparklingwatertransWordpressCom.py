def extractSparklingwatertransWordpressCom(item):
	'''
	Parser for 'sparklingwatertrans.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Faraway Wanderers',                                'Faraway Wanderers',                                               'translated'),
		('Han Shan\'s Sword Unsheathed',                     'Han Shan\'s Sword Unsheathed',                                    'translated'),
		('Lord Seventh',                                     'Lord Seventh',                                                    'translated'),
		('The Actor Extraordinaire',                         'The Actor Extraordinaire',                                        'translated'),
		('PRC',                                              'PRC',                                                             'translated'),
		('Loiterous',                                        'Loiterous',                                                       'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False