def extractSystemtranslationHomeBlog(item):
	'''
	Parser for 'systemtranslation.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Summoner of Miracles',                'Summoner of Miracles',                               'translated'),
		('inadvertently invincible',            'inadvertently invincible',                           'translated'),
		('stand user in marvel universe',       'stand user in marvel universe',                      'translated'),
		('crazy leveling system',               'crazy leveling system',                              'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
	
	if item['tags'] == ['Uncategorized'] or item['tags'] == ['Novel']:
		titlemap = [
			('Stand User in Marvel Universe Chapter ',                   'Stand User in Marvel Universe',                  'translated'),
			('S.U.M.U Chapter ',                                         'Stand User in Marvel Universe',                  'translated'),
			('Jorge Joestar Chapter',                                    'Jorge Joestar',                                  'translated'),
			('C.L.S Chapter ',                                           'Crazy Leveling System',                          'translated'),
			('Crazy Leveling System Chapter',                            'Crazy Leveling System',                          'translated'),
			('I.D.W.A.T.S Chapter ',                                     'I Don\'t Want To Go Against The Sky',            'translated'),
			('S.S Chapter ',                                             'System Supplier',                                'translated'),
			('S.O.M Chapter ',                                           'Summoner of Miracles',                           'translated'),
			('Summoner of Miracles Chapter ',                            'Summoner of Miracles',                           'translated'),
			('Inadvertently Invincible Chapter ',                        'Inadvertently Invincible',                       'translated'),
		]
	
		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False