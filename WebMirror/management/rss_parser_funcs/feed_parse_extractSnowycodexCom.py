def extractSnowycodexCom(item):
	'''
	Parser for 'snowycodex.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	blocked_manhua = [
		'The Legendary Master\'s Wife',
		'World of Cultivation Manhua',
		'Xue Yue Hua (Snow, Moon and Flowers)',
		'Mao Zhi Ming (Cat of Tea)',
		]
	if any([tag in item['tags'] for tag in blocked_manhua]):
		return None

	tagmap = [
		('The Daily Task of Preventing My Disciple from Turning to the Dark Side',         'The Daily Task of Preventing My Disciple from Turning to the Dark Side',                    'translated'),
		('Everyday Life of a Dom Boyfriend',                                               'Everyday Life of a Dom Boyfriend',                                                          'translated'),
		('Wangye, Wangfei is a Cat',                                                       'Wangye, Wangfei is a Cat',                                                                  'translated'),
		('After Exchanging Shadows',                                                       'After Exchanging Shadows',                                                                  'translated'),
		('My Husband Is An Undead',                                                        'My Husband Is An Undead',                                                                   'translated'),
		('Happy Little Mayor',                                                             'Happy Little Mayor',                                                                        'translated'),
		('Heroic Death System',                                                            'Heroic Death System',                                                                       'translated'),
		('Death Notice',                                                                   'Death Notice',                                                                              'translated'),
		('Intense Radical Behavior',                                                       'Intense Radical Behaviors',                                                                 'translated'),
		('The Ultimate Past',                                                              'The Ultimate Past',                                                                         'translated'),
		('Thriller Paradise',                                                              'Thriller Paradise',                                                                         'translated'),
		('Hero? I’ve Long Stopped Being One',                                              'Hero? I’ve Long Stopped Being One',                                                         'translated'),
		('Reborn As My Love Rival’s Wife',                                                 'Reborn As My Love Rival’s Wife',                                                            'translated'),
		('Once We Come Across Love',                                                       'Once We Come Across Love',                                                                  'translated'),
		('Strange Life of a Cat',                                                          'Strange Life of a Cat',                                                                     'translated'),
		('Hollywood Secret Garden',                                                        'Hollywood Secret Garden',                                                                   'translated'),
		('The Path of the Cannon Folder\'s Counterattack',                                 'The Path of the Cannon Folder\'s Counterattack',                                            'translated'),
		('The Overflowing Fragrance of the Fish',                                          'The Overflowing Fragrance of the Fish',                                                     'translated'),
		('Vanguard of the Eternal Night',                                                  'Vanguard of the Eternal Night',                                                             'translated'),
		('Friends With Benefits',                                                          'Friends With Benefits',                                                                     'translated'),
		('Daily Life of an Immortal Cat in the Human World',                               'Daily Life of an Immortal Cat in the Human World',                                          'translated'),
		('Guardian Plot Armor',                                                            'Guardian Plot Armor',                                                                       'oel'),
		('Please Emperor, This Is All A Ploy From My Sister!',                             'Please Emperor, This Is All A Ploy From My Sister!',                                        'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False