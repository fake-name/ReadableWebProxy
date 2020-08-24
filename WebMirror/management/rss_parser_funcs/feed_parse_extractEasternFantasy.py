def extractEasternFantasy(item):
	"""
	Parser for 'Eastern Fantasy'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('The Alma Chronicles',                     'The Alma Chronicles',                                    'translated'),
		('fluffy cultivation',                      'A Martial Odyssey 2',                                    'translated'),
		('A Martial Odyssey 2',                     'A Martial Odyssey 2',                                    'translated'),
		('A Martial Odyssey',                       'A Martial Odyssey',                                      'translated'),
		('the good-for-nothing cultivator',         'the good-for-nothing cultivator',                        'translated'),
		('the romantic cultivator',                 'the romantic cultivator',                                'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False