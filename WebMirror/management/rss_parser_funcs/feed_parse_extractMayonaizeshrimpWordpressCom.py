def extractMayonaizeshrimpWordpressCom(item):
	'''
	Parser for 'mayonaizeshrimp.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Love Switch',                                                        'Love Switch',                                                                       'translated'), 
		('You Think It’s Fine to Just Summon Me to Another World? Huh?',       'You Think It’s Fine to Just Summon Me to Another World? Huh?',                      'translated'), 
		('Impregnable ≪Dreadnought≫',                                         'Impregnable ≪Dreadnought≫',                                                        'translated'), 
		('No Fatigue',                                                         'No Fatigue: 24-jikan Tatakaeru Otoko no Tenseitan',                                 'translated'), 
		('Isekai GM',                                                          'The GM Has Logged Into A Different World',                                          'translated'), 
		('Master\'s Smile',                                                    'Master\'s Smile',                                                                   'translated'), 
		('heibon',                                                             'E? Heibon Desu yo??',                                                               'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	titlemap = [
		('YTIF ',             'You Think It\'s Fine to Just Summon Me to Another World? Huh?',      'translated'),
		('ToK ',              'Tower of Karma',                                                     'translated'),
		('Isekai GM ',        'The GM Has Logged Into A Different World',                           'translated'), 
		('LHA chapter ',      'The Little Hero of Alcatar',                                         'oel'), 
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False