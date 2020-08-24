def extractFoxaholicWordpressCom(item):
	'''
	Parser for 'foxaholic.wordpress.com'
	'''
	
	badwords = [
			'preview',
			'protected',
		]
	ltitle = item['title'].lower()
	if any([bad in ltitle for bad in badwords]):
		return None



	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol):
		return None

	if item['tags'] == ['Uncategorized'] or item['tags'] == ['Novel'] or item['tags'] == ['darkness7913'] or item['tags'] == ['Uncategorized', 'darkness7913']:
		
		if '100 Ways to Get the Male God Chapter ' in item['title'] and chp != 100:
			return buildReleaseMessageWithType(item, '100 Ways to Get the Male God', vol, chp, frag=frag, postfix=postfix, tl_type='translated')
			
			
		titlemap = [
			('Skill Taker’s World Domination ~ Building a Slave Harem from Scratch Chapter ',  'Skill Taker’s World Domination ~ Building a Slave Harem from Scratch',      'translated'),
			('New Chapter: Legend of Great Tang’s Twin Dragons, ',                             'Legend of Great Tang’s Twin Dragons',                                       'translated'),
			('New Chapter: I am a Good Man – Chapter ',                                        'I am a Good Man',                                                           'translated'),
			('New Chapter: Hazure Waku Ch. ',                                                  'Hazure Waku',                                                               'translated'),
			('New Ch: How To Say I Love You – ',                                               'How To Say I Love You',                                                     'translated'),
			('New Ch: Cannon Fodder Counter Attack System ',                                   'Cannon Fodder Counter Attack System',                                       'translated'),
			('Quick Transmigration: The Villain is delicate and soft – ',                      'Quick Transmigration: The Villain is delicate and soft',                    'translated'),
			('The Yandere came During the Night – Chapter ',                                   'The Yandere came During the Night',                                         'translated'),
			('New Ch: Time – ',                                                                'Time ',                                                                     'translated'),
			('How To Become A Great White Moonlight Chapter ',                                 'How To Become A Great White Moonlight',                                     'translated'),
			('Transmigrating into a demon spirit',                                             'Transmigrating into a demon spirit to blow up the entire world',            'translated'),
			('Transmigrating into the ML’s Villainess Older Sis',                              'Transmigrating into the ML’s Villainess Older Sister',                      'translated'),
			('A crowd of evil spirit',                                                         'A crowd of evil spirit lines up to confess to me',                          'translated'),
			('A crowd of evil spirit lines up to confess to me',                               'A crowd of evil spirit lines up to confess to me',                          'translated'),
			('After Being Transported into a Book, I Adopted the Villain Chapter',             'After Being Transported into a Book, I Adopted the Villain',                'translated'),
			('Demon King of Phantom Thief',                                                    'Demon King of Phantom Thief',                                               'translated'),
			('Quick Wear: Male God, Shine Bright! Chapter ',                                   'Quick Wear: Male God, Shine Bright!',                                       'translated'),
			('Granting You a Dreamlike Life Chapter ',                                         'Granting You a Dreamlike Life',                                             'translated'),
			('Undying Patient ',                                                               'Undying Patient',                                                           'translated'),
			('The Noble Woman’s Guide On How to Tease One’s Husband – Chapter ',               'The Noble Woman’s Guide On How to Tease One’s Husband',                     'translated'),
			('Love Experiment Chapter ',                                                       'Love Experiment',                                                           'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	tagmap = [
		('The Law of Transmigration: The Black-Hearted God’s Domineering Love',                     'The Law of Transmigration: The Black-Hearted God’s Domineering Love',                                    'translated'),
		('Quick Transmigration\'s Strategical Attack: 100 Ways to Get the Male God',                'Quick Transmigration\'s Strategical Attack: 100 Ways to Get the Male God',                               'translated'),
		('Oh My General',                                                                           'Oh My General',                                                                                          'translated'),
		('Good Man Operation Guide',                                                                'Good Man Operation Guide',                                                                               'translated'),
		('Male God Shine Bright!',                                                                  'Male God Shine Bright!',                                                                                 'translated'),
		('The Queen\'s Husband',                                                                    'The Queen\'s Husband',                                                                                   'translated'),
		('Rebirth and Redemption',                                                                  'Rebirth and Redemption',                                                                                 'translated'),
		('the legend of the ghost concubine',                                                       'the legend of the ghost concubine',                                                                      'translated'),
		('The Black-Hearted God\'s Domineering Love',                                               'The Black-Hearted God\'s Domineering Love',                                                              'translated'),
		('granting you a dreamlike life',                                                           'granting you a dreamlike life',                                                                          'translated'),
		('certificate of conformity',                                                               'certificate of conformity',                                                                              'translated'),
		('the major general\'s smart and gorgeous wife',                                            'the major general\'s smart and gorgeous wife',                                                           'translated'),
		('the husbands from the republic of china',                                                 'the husbands from the republic of china',                                                                'translated'),
		('road of the king',                                                                        'road of the king',                                                                                       'translated'),
		('what do i want to do with this magnificent beauty?',                                      'what do i want to do with this magnificent beauty?',                                                     'translated'),
		('Every Vicious Woman Needs a Loyal Man',                                                   'Every Vicious Woman Needs a Loyal Man',                                                                  'translated'),
		('My Amazing WeChat is Connected to the Three Realms',                                      'My Amazing WeChat is Connected to the Three Realms',                                                     'translated'),
		('the warm breeze is not as warm as you',                                                   'the warm breeze is not as warm as you',                                                                  'translated'),
		('quick transmigration: the villain is delicate and soft',                                  'Quick Transmigration: The Villain is delicate and soft',                                                 'translated'),
		('Every World Seems Not Quite Right',                                                       'Every World Seems Not Quite Right',                                                                      'translated'),
		('the rebirth waste strikes back',                                                          'the rebirth waste strikes back',                                                                         'translated'),
		('luoyang brocade',                                                                         'luoyang brocade',                                                                                        'translated'),
		('rebirth of the general’s granddaughter',                                                  'Rebirth of the General’s Granddaughter',                                                                 'translated'),
		('ordered to marry thrice, the mysterious wangfei 奉旨三嫁，赖上神秘王妃',                  'Ordered to Marry Thrice, The Mysterious Wangfei',                                                        'translated'),
		('i don’t dare to oppose a protagonist anymore',                                            'i don’t dare to oppose a protagonist anymore',                                                           'translated'),
		('Dangerous Survival in the Apocalypse',                                                    'Dangerous Survival in the Apocalypse',                                                                   'translated'),
		('descent of the phoenix',                                                                  'Descent of the Phoenix: 13 Year Old Princess Consort',                                                   'translated'),
		('the banished villainess\' husband',                                                       'the banished villainess\' husband',                                                                      'translated'),
		('sonata: fleeing to avoid an arranged marriage',                                           'Sonata: Fleeing to Avoid an Arranged Marriage',                                                          'translated'),
		('dota madness',                                                                            'dota madness',                                                                                           'translated'),
		('game of gods',                                                                            'game of gods',                                                                                           'translated'),
		('seizing a good marriage, the virtuous medical consort',                                   'seizing a good marriage, the virtuous medical consort',                                                  'translated'),
		('chairman husband, too boorish',                                                           'chairman husband, too boorish',                                                                          'translated'),
		('my girlfriend is really a superstar',                                                     'my girlfriend is really a superstar',                                                                    'translated'),
		('Being An Author Is A High Risk Occupation',                                               'Being An Author Is A High Risk Occupation',                                                              'translated'),
		('congratulations, empress',                                                                'congratulations, empress',                                                                               'translated'),
		('my engagement got broken, but i don’t remember getting engaged in the first place',       'my engagement got broken, but i don’t remember getting engaged in the first place',                      'translated'),
		('warm marriage: honourable wife is a little cute',                                         'warm marriage: honourable wife is a little cute',                                                        'translated'),
		('the whole tribe wants to have baby with me',                                              'the whole tribe wants to have baby with me',                                                             'translated'),
		('one hundred ways to become a god',                                                        'one hundred ways to become a god',                                                                       'translated'),
		('you can’t be fierce towards me',                                                          'you can’t be fierce towards me',                                                                         'translated'),
		('100 ways to get the male god',                                                            '100 ways to get the male god',                                                                           'translated'),
		('rebirth of a counterattack: godly doctor shizi fei',                                      'rebirth of a counterattack: godly doctor shizi fei',                                                     'translated'),
		('rebirth of the abandoned woman: godly doctor taizi fei',                                  'rebirth of the abandoned woman: godly doctor taizi fei',                                                 'translated'),
		('exile [farming]',                                                                         'exile [farming]',                                                                                        'translated'),
		('boss dresses as a cutie',                                                                 'boss dresses as a cutie',                                                                                'translated'),
		('shan he biao li',                                                                         'shan he biao li',                                                                                        'translated'),
		('the little merman',                                                                       'the little merman',                                                                                      'translated'),
		('the case files of jeweler richard',                                                       'the case files of jeweler richard',                                                                      'translated'),
		('Three Marriages',                                                                         'Three Marriages',                                                                                        'translated'),
		("i'm bearing my love rival's child",                                                       "i'm bearing my love rival's child",                                                                      'translated'),
		('the chant of the sinking moon',                                                           'the chant of the sinking moon',                                                                          'translated'),
		('evil-natured husband, don’t tease!',                                                      'evil-natured husband, don’t tease!',                                                                     'translated'),
		('in the future, my whole body is a treasure',                                              'in the future, my whole body is a treasure',                                                             'translated'),
		('a joyful happening in the house',                                                         'a joyful happening in the house',                                                                        'translated'),
		('Rebirth of a CV Star',                                                                    'Rebirth of a CV Star',                                                                                   'translated'),
		('the yakuza\'s love towards the kitchenmaid is too heavy',                                 'the yakuza\'s love towards the kitchenmaid is too heavy',                                                'translated'),
		('fake holy sword',                                                                         'Fake Holy Sword Story ～I Was Taken Along When I Sold My Childhood Friend～',                            'translated'),
		('earth-san level up',                                                                      'Earth-san Has Leveled Up ～Heroic Tale of A Girl With Non-Concealed Principle～',                        'translated'),
		('rebirth in the novel: indulging the female side character',                               'rebirth in the novel: indulging the female side character',                                              'translated'),
		('becoming the male lead\'s white moonlight',                                               'becoming the male lead\'s white moonlight',                                                              'translated'),
		('Yang Shu Mei Ying',                                                                       'Yang Shu Mei Ying',                                                                                      'translated'),
		('Rebirth into an Interstellar Marriage',                                                   'Rebirth into an Interstellar Marriage',                                                                  'translated'),
		('World Strongest Rearguard',                                                               'World Strongest Rearguard',                                                                              'translated'),
		('5 big shots kneeled and called me mom',                                                   '5 big shots kneeled and called me mom',                                                                  'translated'),
		('hidden marriage sweet pampering: the conglomerate’s little wife',                         'hidden marriage sweet pampering: the conglomerate’s little wife',                                        'translated'),
		('abandoned concubine: kidnapping a cute baby to break out into the world',                 'abandoned concubine: kidnapping a cute baby to break out into the world',                                'translated'),
		('yun family’s little nine is super mischievous',                                           'yun family’s little nine is super mischievous',                                                          'translated'),
		('brothel open for business (h)',                                                           'brothel open for business (h)',                                                                          'translated'),
		('i have refined qi for 3000 years',                                                        'i have refined qi for 3000 years',                                                                       'translated'),
		('my sister told me to give up my fiancé',                                                  'my sister told me to give up my fiancé',                                                                 'translated'),
		('slag gong wants to kill me',                                                              'slag gong wants to kill me',                                                                             'translated'),
		('CPVTTF',                                                                                  'The Counterattack Plan of A Villain With Ten Thousand Fans',                                             'translated'),
		('transmigrated female support: male god, addicted to teasing',                             'transmigrated female support: male god, addicted to teasing',                                            'translated'),
		('transmigrated female support: male god addicted to teasing',                              'transmigrated female support: male god, addicted to teasing',                                            'translated'),
		('quick transmigration system: pounce on male gods which family’s stronger',                'quick transmigration system: pounce on male gods which family’s stronger',                               'translated'),
		('quick transmigration: the villain\'s sweet wife',                                         'quick transmigration: the villain\'s sweet wife',                                                        'translated'),
		('the villain is happy being a father [quick',                                              'the villain is happy being a father',                                                                    'translated'),
		('Winter Begonia',                                                                          'Winter Begonia',                                                                                         'translated'),
		('fairyland lovers',                                                                        'fairyland lovers',                                                                                       'translated'),
		('leisurely beast world: plant some fields have some cubs',                                 'leisurely beast world: plant some fields, have some cubs',                                               'translated'),
		('leisurely beast world: plant some fields, have some cubs',                                'leisurely beast world: plant some fields, have some cubs',                                               'translated'),
		('vhbf',                                                                                    'the villain is happy being a father [quick transmigration]',                                             'translated'),
		('want to ascend then fall in love',                                                        'want to ascend then fall in love',                                                                       'translated'),
		('undying patient',                                                                         'undying patient',                                                                                        'translated'),
		('the villains i raised all died',                                                          'the villains i raised all died',                                                                         'translated'),
		('black iron magician',                                                                     'black iron magician',                                                                                    'translated'),
		('i am a gao fushuai villain',                                                              'i am a gao fushuai villain',                                                                             'translated'),
		('tbddm',                                                                                   'The Basketball Captain is Determined to Date Me',                                                        'translated'),
		('tbcddm',                                                                                  'The Basketball Captain is Determined to Date Me',                                                        'translated'),
		('supernatural rebirth genius girl diviner',                                                'supernatural rebirth genius girl diviner',                                                               'translated'),
		('apocalypse rebirth: chief, don’t move!',                                                  'apocalypse rebirth: chief, don’t move!',                                                                 'translated'),

		('av filming guidebook',                                               'av filming guidebook',                                                              'translated'),
		('not allowed to leak a single drop',                                  'not allowed to leak a single drop',                                                 'translated'),
		('the transmigrated cannon fodder overthrows the male protagonist',    'the transmigrated cannon fodder overthrows the male protagonist',                   'translated'),
		('after being extorted',                                               'after being extorted',                                                              'translated'),
	
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]






	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False