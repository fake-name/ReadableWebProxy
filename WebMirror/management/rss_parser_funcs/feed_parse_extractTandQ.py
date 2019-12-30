def extractTandQ(item):
	"""
	T&Q
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	bad = [
			'#K-drama', 
			'fashion', 
			'C-Drama', 
			'#Trending', 
			'Feature', 
			'#Trailer', 
			'#Eng Sub', 
			'Movies', 
			'Status Updates/Post Tallies', 
			'Learn Chinese',
			'Short Stories',
		]
	if any([(tmp in item['tags']) for tmp in bad]):
		return None
		
		
	tagmap = [
		('Three Kingdoms Online Overlord',                                      'Three Kingdoms Online Overlord',                                                'translated'),
		('Three Kingdoms Online Overlord | 网游之三国超级领主',                 'Three Kingdoms Online Overlord',                                                'translated'),
		('Perfect Fiance',                                                      'Perfect Fiancé',                                                                'translated'),
		('Perfect Fiancé | 完美未婚夫',                                         'Perfect Fiancé',                                                                'translated'),
		('Ten Years are not that Far',                                          'Ten Years are not that Far',                                                    'translated'),
		('#Les Interpretes',                                                    'Les Interpretes',                                                               'translated'),
		('致我们终将逝去的青春',                                                'To Our Youth That is Fading Away',                                              'translated'),
		('So Young | 致我们终将逝去的青春',                                     'To Our Youth That is Fading Away',                                              'translated'),
		("Fleeting Midsummer (Beijing University's Weakest Student)",           "Fleeting Midsummer (Beijing University's Weakest Student)",                     'translated'),
		("Fleeting Midsummer (Peking University's Weakest Student)",            "Fleeting Midsummer (Peking University's Weakest Student)",                      'translated'),
		("Fleeting Midsummer (Peking University's Weakest Student)| 北大差生·", "Fleeting Midsummer (Peking University's Weakest Student)",                      'translated'),
		("Fleeting Midsummer (Peking University's Weakest Student)| 北大差生",  "Fleeting Midsummer (Peking University's Weakest Student)",                      'translated'),
		('When A Snail Falls in Love| 如果蜗牛有爱情',                          'When A Snail Falls in Love',                                                    'translated'),
		('The Rebirth of an Ill-Fated Consort | 重生之嫡女祸妃',                'The Rebirth of an Ill-Fated Consort',                                           'translated'),
		('Siege in Fog | 迷雾围城',                                             'Siege in Fog',                                                                  'translated'),
		('Pristine Darkness | 他来了请闭眼之暗粼',                              'Pristine Darkness',                                                             'translated'),
		('Les Interpretes | 亲爱的翻译官',                                      'Les Interpretes',                                                               'translated'),
		('Les Interpretes | 情爱的翻译官',                                      'Les Interpretes',                                                               'translated'),
		('The Daily Record of Secretly Loving the Male Idol|男神暗恋日记',      'The Daily Record of Secretly Loving the Male Idol',                             'translated'),
		('Master Devil Don\'t Kiss Me',                                         'Master Devil Don\'t Kiss Me',                                                   'translated'),
		('Master Devil Don\'t Kiss Me! | 恶魔少爷别吻我',                       'Master Devil Don\'t Kiss Me',                                                   'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False