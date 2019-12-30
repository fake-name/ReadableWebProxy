def extractMichilunWordpressCom(item):
	'''
	Parser for 'michilun.wordpress.com'
	'''
	bad = [
		'Recommendations and Reviews',
		]
	
	if any([tmp in item['tags'] for tmp in bad]):
		return None
	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Side Projects - Scheme of the Official Descendant',                  'Scheme of the Official Descendant',                      'translated'),
		('Song in the Peach Blossoms',                                         'Song in the Peach Blossoms',                             'translated'),
		('Onrain (Online - The Novel)',                                        'Onrain (Online - The Novel)',                            'translated'),
		('At the End of the Wish',                                             'At the End of the Wish',                                 'translated'),
		('Bringing Calamity to the Nation',                                    'Bringing Calamity to the Nation',                        'translated'),
		('Side Projects - The Flame\'s Daughter',                              'The Flame\'s Daughter',                                  'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False