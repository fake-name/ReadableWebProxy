def extractIsohungrytlsCom(item):
	'''
	Parser for 'isohungrytls.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Wangye\'s-Maid-Is-The-Sect-Leader',                                           'Wangye\'s Maid is the Sect Leader',                                           'translated'), 
		('RFSH',                                                                        'Raising a Fox Spirit in My Home',                                             'translated'), 
		('poisonous peasant concubine',                                                 'Poisonous Peasant Concubine',                                                 'translated'), 
		('Descent of the God of Magic',                                                 'Descent of the God of Magic',                                                 'translated'), 
		('Wild Malicious Consort',                                                      'Wild Malicious Consort: Good For Nothing Ninth Miss',                         'translated'), 
		('Quick Transmigration Cannon Fodder\'s Record of Counterattacks',              'Quick Transmigration Cannon Fodder\'s Record of Counterattacks',              'translated'), 
		('Wangye, Wangfei is a Cat',                                                    'Wangye, Wangfei is a Cat',                                                    'translated'), 
		('Back to the Apocalypse',                                                      'Back to the Apocalypse',                                                      'translated'), 
		('Life After Marrying my Sworn Enemy',                                          'Life After Marrying my Sworn Enemy',                                          'translated'), 
		('Run Over',                                                                    'Run Over',                                                                    'translated'), 
		('Sword Labyrinth Of The Sacred Sword',                                         'Sword Labyrinth Of The Sacred Sword',                                         'translated'), 
		('Raising a Fox into a Consort',                                                'Raising a Fox into a Consort',                                                'translated'), 
		('Phoenix Rising Over The World',                                               'Phoenix Rising Over The World',                                               'translated'), 
		('Expelled From Paradise',                                                      'Expelled From Paradise',                                                      'translated'), 
		('Black Bellied President Dotes on Wife',                                       'Black Bellied President Dotes on Wife',                                       'translated'), 
		('World of Chaos: Alluring Military Consort',                                   'World of Chaos: Alluring Military Consort',                                   'translated'), 
		('Demon God Pesters- The Ninth Lady of the Doctor',                             'The Demon God Pesters: The Ninth Lady of the Doctor',                         'translated'), 
		('Bewitching Prince Spoils His Wife: Genius Doctor Unscrupulous Consort',       'Bewitching Prince Spoils His Wife: Genius Doctor Unscrupulous Consort',       'translated'),  
		('Transmigration Routine',                                                      'The Transmigration Routine of Always Being Captured by the ML',               'translated'), 
		('World of Chaos',                                                              'World of Chaos: Alluring Military Consort',                                   'translated'), 
		('QT Cannon Fodder\'s Record of Counterattacks',                                'Quick Transmigration Cannon Fodder\'s Record of Counterattacks',              'translated'), 
		('Rebirth in a Perfect Era',                                                    'Rebirth in a Perfect Era',                                                    'translated'), 
		('Need to Propose to Seven Men What to Do',                                     'Need to Propose to Seven Men What to Do',                                     'translated'), 
		('Way of Transmigration',                                                       'Way of Transmigration',                                                       'translated'), 
		('The Cold Regent Keeps a Fox as a Consort',                                    'The Cold Regent Keeps a Fox as a Consort',                                    'translated'), 
		('The Captivating Crown Prince',                                                'The Captivating Crown Prince',                                                'translated'), 
		('Thunder Martial',                                                             'Thunder Martial',                                                             'translated'), 
		('Return of the Goddess',                                                       'Return of the Goddess',                                                       'translated'), 
		('Film Emperor\'s Beloved Wife',                                                'Film Emperor\'s Beloved Wife',                                                'translated'), 
		('Every Vicious Woman Needs a Loyal Man',                                       'Every Vicious Woman Needs a Loyal Man',                                       'translated'), 
		('Sinister Ex-Girlfriend',                                                      'Sinister Ex-Girlfriend',                                                      'translated'), 
		('Killed the White Lotus',                                                      'Killed the White Lotus',                                                      'translated'), 
		('The Lover\'s Prattle',                                                        'The Lover\'s Prattle',                                                        'translated'), 
		('How to die as heavy as mount tai',                                            'How to die as heavy as mount tai',                                            'translated'), 
		('You Look Like You\'re Made of Money',                                         'You Look Like You\'re Made of Money',                                         'translated'), 
		('Subduing a Gentleman\'s Heart',                                               'Hundred Flowers Slaughter: Confusing a Gentleman\'s Heart',                   'translated'), 
		('There\'s A Beauty',                                                           'There\'s A Beauty',                                                           'translated'), 
		('Midnight Cinderella',                                                         'Midnight Cinderella',                                                         'translated'), 
		('Wealthy Woof',                                                                'Daily Life of a Wealthy Woof',                                                'translated'), 
		('Banished to Another World',                                                   'Banished to Another World',                                                   'translated'), 
		('quick transmigration female lead male god never stopping',                    'Quick Transmigration Female Lead: Male God, Never Stopping',                  'translated'), 
		('Young Master Quan',                                                           'Young Master Quan',                                                           'translated'), 
		('Wife is Outrageous',                                                          'Wife is Outrageous',                                                          'translated'), 
		('Goddess Medical Doctor',                                                      'Goddess Medical Doctor',                                                      'translated'), 
		('the travelling hero won\'t let the innkeeper\'s son escape',                  'The Traveling Hero Won\'t Let the Innkeeper\'s Son Escape',                   'translated'), 
		('The Rebirth of Han Yuxi',                                                     'The Rebirth of Han Yuxi',                                                     'translated'), 
		('Just the Two of Us in this Vast World',                                       'Just the Two of Us in this Vast World',                                       'translated'), 
		('Rescuing the Blackened Male Lead',                                            'Rescuing the Blackened Male Lead',                                            'translated'), 
		('Potatoes are the Only Thing Needed in This World!',                           'Potatoes are the Only Thing Needed in This World!',                           'translated'), 
		('i swear i won’t bother you again!',                                           'i swear i won’t bother you again!',                                           'translated'), 
		('my husband with scholar syndrome',                                            'my husband with scholar syndrome',                                            'translated'), 
		('parallel lines',                                                              'parallel lines',                                                              'translated'), 
		('The Fierce Illegitimate Miss',                                                'The Fierce Illegitimate Miss',                                                'translated'), 
		('Wangye\'s Maid is the Sect Leader',                                           'Wangye\'s Maid is the Sect Leader',                                           'translated'), 
		('Legendary Dragon God',                                                        'Legendary Dragon God',                                                        'oel'), 
	]
	
	
	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
	
	
	if item['tags'] == ['Uncategorized']:
		urlfrag = [    
			('isohungrytls.com/consort-overturning-world',                         'Consort Overturning the World',                                               'translated'), 
			('isohungrytls.com/expelled-paradise-',                                'Expelled From Paradise',                                                      'translated'), 
			('isohungrytls.com/phoenix-rising-world-chapter-',                     'Phoenix Rising Over the World',                                               'translated'), 
			('isohungrytls.com/wangye-wangfei-cat-chapter-',                       'Wangye, Wangfei is a Cat',                                                    'translated'), 
			('isohungrytls.com/accompanying-phoenix-chapter-'    ,                 'Accompanying the Phoenix',                                                    'translated'), 
			('isohungrytls.com/wangyes-maid-sect-leader-chapter-',                 'Wangye\'s Maid is the Sect Leader',                                           'translated'), 
			('isohungrytls.com/wife-outragoeus-chapter-',                          'Wife is Outrageous',                                                          'translated'), 
			('isohungrytls.com/wife-outrageous-chapter-',                          'Wife is Outrageous',                                                          'translated'),
			('isohungrytls.com/trac-chapter',                                      'The Transmigration Routine of Always Being Captured by the ML',               'translated'), 
			('isohungrytls.com/bewitching-prince-chapter-',                        'Bewitching Prince Spoils His Wife: Genius Doctor Unscrupulous Consort',       'translated'), 
			('isohungrytls.com/captivating-crown-prince-',                         'The Captivating Crown Prince',                                                'translated'), 
			('isohungrytls.com/raising-fox-consort-',                              'Raising a Fox into a Consort',                                                'translated'), 
			('isohungrytls.com/wild-malicious-consort-chapter',                    'Wild Malicious Consort: Good For Nothing Ninth Miss',                         'translated'), 
			('/quick-transmigration-rescuing-the-blackened-male-lead-chapter',     'Quick Transmigration: Rescuing the Blackened Male Lead',                      'translated'), 
		]
	
		for key, name, tl_type in urlfrag:
			if key in item['linkUrl'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
	
		titlemap = [
			('RFEBW Chapter ',                                                              'Rebirth of the Film Emperor\'s Beloved Wife Chapter',                         'translated'), 
			('BBPDOW Chapter',                                                              'Black Bellied President Dotes on Wife',                                       'translated'), 
			('Reborn as a mom Chapter',                                                     'Reborn as a Mom',                                                             'oel'),
			('RFEBW ',                                                                      'Rebirth of the Film Emperor’s Beloved Wife',                                  'translated'),
			('Wife is Outrageous Chapter ',                                                 'Wife is Outrageous',                                                          'translated'),
			('How to die as heavy as mount tai',                                            'How to die as heavy as mount tai',                                            'translated'), 
			('Black Bellied President Chapter ',                                            'Black Bellied President Dotes on Wife',                                       'translated'), 
			('Exclusive Sweetheart Chapter ',                                               'Super Sweet Love: The School Prince\'s Exclusive Sweetheart',                 'translated'), 
			('Rebirth of the Film Emperor’s Beloved Wife Chapter',                          'Rebirth of the Film Emperor\'s Beloved Wife Chapter',                         'translated'), 
		]
	
		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False