def extractWwwWangmamareadCom(item):
	'''
	Parser for 'www.wangmamaread.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Returning from the Immortal World',                'Returning from the Immortal World',                               'translated'),
		('Master of Trading Star Card Game (Rebirth)',       'Master of Trading Star Card Game (Rebirth)',                      'translated'),
		('Long Live Summons!',                               'Long Live Summons!',                                              'translated'),
		('Release that Witch',                               'Release that Witch',                                              'translated'),
		('Eastern Palace',                                   'Eastern Palace',                                                  'translated'),
		('Good Morning, Mr. President!',                     'Good Morning, Mr. President!',                                    'translated'),
		('Star Martial God Technique',                       'Star Martial God Technique',                                      'translated'),
		('Douluo Dalu: Legend of the Divine Realm',          'Douluo Dalu: Legend of the Divine Realm',                         'translated'),
		('zhan long',                                        'Zhan Long',                                                       'translated'),
		('Chronicles of Primordial Wars',                    'Chronicles of Primordial Wars',                                   'translated'),
		('To Be a Power in the Shadows!',                    'To Be a Power in the Shadows!',                                   'translated'),
		('The Tutorial Is Too Hard',                         'The Tutorial Is Too Hard',                                        'translated'),
		('Legend of the Cultivation God',                    'Legend of the Cultivation God',                                   'translated'),
		('The Anarchic Consort of the Prince',               'The Anarchic Consort of the Prince',                              'translated'),
		('Dragon Blood Warrior',                             'Dragon Blood Warrior',                                            'translated'),
		('Otherworld Nation Founding Chronicles',            'Otherworld Nation Founding Chronicles',                           'translated'),
		('across the stunning beast princess: phoenix against the world',       'across the stunning beast princess: phoenix against the world',                      'translated'),
		('Rebirth of the Rich and Wealthy',       'Rebirth of the Rich and Wealthy',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False