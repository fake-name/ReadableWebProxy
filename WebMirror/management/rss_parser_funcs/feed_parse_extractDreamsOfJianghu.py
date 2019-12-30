def extractDreamsOfJianghu(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	bad = ['pictures']
	if any([(tmp in item['tags']) for tmp in bad]):
		return None
		
	tagmap = [
		('TBVW',    'To Be A Virtuous Wife',                    'translated'),
		('WC',      'World of Cultivation',                     'translated'),
		('8TT',     'Eight Treasure Trousseau',                 'translated'),
		('4.6',     '4.6 Billion Years Symphony of Evolution',  'translated'),
		('Zuo Mo',  'World of Cultivation',                     'translated'),
		('ZX',      'Zhui Xu',                                  'translated'),
		('AUW',     'An Unyielding Wind',                       'translated'),
		('ADND',    'Ascending, Do Not Disturb',                'translated'),
		('sd',      'Sword Dynasty',                            'translated'),
		
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False