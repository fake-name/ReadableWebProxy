def extractDummynovelsCom(item):
	'''
	Parser for 'dummynovels.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('transmigrating into the heartthrob\'s cannon fodder childhood friend',       'transmigrating into the heartthrob\'s cannon fodder childhood friend',                      'translated'),
		('meow! a kitten stumbles into a ceo novel!',                                  'meow! a kitten stumbles into a ceo novel!',                                                 'translated'),
		('paper lover',                                                                'paper lover',                                                                               'translated'),
		('The People Who’re Suppose to Kill Me All Fell for Me Instead',               'The People Who’re Suppose to Kill Me All Fell for Me Instead',                              'translated'),
		('my nemesis has finally gone bankrupt',                       'my nemesis has finally gone bankrupt',                                      'translated'),
		('The General\'s cat always wants to climb into my bed',       'The General\'s cat always wants to climb into my bed',                      'translated'),
		('the people who\'re supposed to kill me fell for me instead', 'the people who\'re supposed to kill me fell for me instead',                'translated'),
		('i have a sickness',                                          'i have a sickness',                                                         'translated'),
		('The target always thinks that I like him',                   'The target always thinks that I like him',                                  'translated'),
		('could you not tease me',                                     'could you not tease me',                                                    'translated'),
		('fake demon lord',                                            'fake demon lord',                                                           'translated'),
		('sea monster alliance',                                       'sea monster alliance',                                                      'translated'),
		('Lovable Package',                                            'Lovable Package',                                                           'translated'),
		('good god stop',                                              'good god stop',                                                             'translated'),
		('why do i wake up as a cheater every time',                   'why do i wake up as a cheater every time',                                  'translated'),
		('pastel colours',                                             'pastel colours',                                                            'translated'),
		('Sect Master and Psycho',                                     'Sect Master and Psycho',                                                    'translated'),
		('asylum live broadcast room',                                 'asylum live broadcast room',                                                'translated'),
		('a filthy rich hamster in the apocalypse',                    'a filthy rich hamster in the apocalypse',                                   'translated'),
		('the villain has been coveting me for a long time',           'the villain has been coveting me for a long time',                          'translated'),
		('bite your fingertips',                                       'bite your fingertips',                                                      'translated'),
		('i have a sickness [world-hopping]',                          'i have a sickness [world-hopping]',                                         'translated'),
		('how could this cat tease me?',                               'how could this cat tease me?',                                              'translated'),
		('marriage agreement',                                         'marriage agreement',                                                        'translated'),
		('why do i wake up as a cheater every time?',                  'why do i wake up as a cheater every time?',                                 'translated'),
		('the target always thinks that i like him!',                  'the target always thinks that i like him!',                                 'translated'),
		('everyone loves pei jiyu',                                    'everyone loves pei jiyu',                                                   'translated'),
		('forensic traversing notes',                                  'forensic traversing notes',                                                 'translated'),
		('could you not tease me?',                                    'could you not tease me?',                                                   'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False