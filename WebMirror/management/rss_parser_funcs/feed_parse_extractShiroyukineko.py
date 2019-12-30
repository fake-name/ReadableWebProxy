def extractShiroyukineko(item):
	"""
	# 'Shiroyukineko Translations'

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'Announcements' in item['tags']:
		return None
		
	tagmap = [
		('DOP',                                                    'Descent of the Phoenix: 13 Year Old Princess Consort',    'translated'),
		('Descent of the Phoenix: 13 Year Old Princess Consort',   'Descent of the Phoenix: 13 Year Old Princess Consort',    'translated'),
		('LLS',                                                    'Long Live Summons!',                                      'translated'),
		('Long Live Summons!',                                     'Long Live Summons!',                                      'translated'),
		('Virtual World: Unparalled Under The Sky',                'Virtual World: Unparalleled under the Sky',               'translated'),
		('VW:UUTS',                                                'Virtual World: Unparalleled under the Sky',               'translated'),
		('Ze Tian Ji',                                             'Ze Tian Ji',                                              'translated'),
		('The Strongest Dan God',                                  'The Strongest Dan God',                                   'translated'),
		('Scriptures of the Great Emperor',                        'Scriptures of the Great Emperor',                         'translated'),
		('Dragon-Blooded War God',                                 'Dragon-Blooded War God',                                  'translated'),
		('Godly Model Creator',                                    'Godly Model Creator',                                     'translated'),
		('Super Brain Telekinesis',                                'Super Brain Telekinesis',                                 'translated'),
		('Shadow Rogue',                                           'Shadow Rogue',                                            'translated'),
		('hacker',                                                 'HacKer',                                                  'translated'),
		('Return of the Net Gaming Monarch',                       'Return of the Net Gaming Monarch',                        'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	if 'ZTJ Chapter' in item['title']:
		return buildReleaseMessageWithType(item, 'Ze Tian Ji', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('DOP Chapter'):
		return buildReleaseMessageWithType(item, 'Descent of the Phoenix: 13 Year Old Princess Consort', vol, chp, frag=frag, postfix=postfix)
		
		
	return False