def extractVesperlxd(item):
	"""
	Parser for 'VesperLxD'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
		
	tagmap = [
		('Invincible Level Up',                                   'Invincible Level Up',                                'translated'),
		('Rebirth of an Abandoned Woman',                         'Rebirth of an Abandoned Woman',                      'translated'),
		("Great Han's Female General Wei Qiqi",                   "Great Han's Female General Wei Qiqi",                'translated'),
		('The Woman Who Accepts Her Fate',                        'The Woman Who Accepts Her Fate',                     'translated'),
		('Miracle Doctor, Wild Empress: Genius Summoner',         'Miracle Doctor, Wild Empress: Genius Summoner',      'translated'),
		('The General’s Little Peasant Wife',                     'The General’s Little Peasant Wife',                  'translated'),
		('Midnight Offering: Hades\'s Little Pet',                'Midnight Offering: Hades\'s Little Pet',             'translated'),
		('The Man Who Met God',                                   'The Man Who Met God',                                'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False