def extractStarveCleric(item):
	"""
	StarveCleric
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	if 'protected' in item['title'].lower():
		return None
		
	tagmap = [

		("Library of Heaven's Path",                 "Library of Heaven's Path",                 'translated'),
		('The Experimental Diaries of A Crazy Lich', 'The Experimental Diaries of A Crazy Lich', 'translated'),
		('ninth special district',                   'ninth special district',                   'translated'),
		('Tian Ying',                                'Tian Ying',                                'translated'),
		('The Adonis Next Door',                     'The Adonis Next Door',                     'translated'),
		('The Diary of the Truant Death God',        'The Diary of the Truant Death God',        'translated'),
		('Dao Tian Xian Tu',                         'Dao Tian Xian Tu',                         'translated'),
		('Rebirth - First Class Magician',           'Rebirth - First Class Magician',           'translated'),
		('The Records of the Human Emperor',         'The Records of the Human Emperor',         'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
		
	return False