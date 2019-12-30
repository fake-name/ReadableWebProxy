def extractWwwDdiversionXyz(item):
	'''
	Parser for 'www.ddiversion.xyz'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('If You Don\'t Go To Hell Who Will',       'If You Don\'t Go To Hell Who Will',                      'translated'),
		('Deadly Delivery',                         'Deadly Delivery',                                        'translated'),
		('Strongest Counterattack',                 'Strongest Counterattack',                                'translated'),
		('Slowly Falling For Changkong',            'Slowly Falling For Changkong',                           'translated'),
		('Ring The Chime Of Grievance',             'Ring The Chime Of Grievance',                            'translated'),
		('PRC',                                     'PRC',                                                    'translated'),
		('Loiterous',                               'Loiterous',                                              'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False