def extractCrappyasstranslationsCom(item):
	'''
	Parser for 'crappyasstranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Civil Officer Can Have Sweet Dreams',                'The Civil Officer Can Have Sweet Dreams',                      'translated'),
		('Konyaku-sha ga Akuyaku de Komattemasu',                  'Konyaku-sha ga Akuyaku de Komattemasu',                        'translated'),
		('wants normality but ain\'t normal magician',             'The Sorcerer Wants Normality',                                 'translated'),
		('Lady Philia D\'la Love\'s Mistakes',                     'Lady Philia D\'la Love\'s Mistakes',                           'translated'),
		('The Me Who Wants To Escape The Princess Training',       'The Me Who Wants To Escape The Princess Training',                      'translated'),
		('The Black Cat Prince Laughed At The Moon',               'The Black Cat Prince Laughed At The Moon',                      'translated'),
		('timid countess',                                         'The Timid Count’s Daughter Doesn’t Wish for Quarrel',                      'translated'),
		('i\'m spying on the heroine',                             'I\'m Spying on the Heroine in an Otome Game World',                      'translated'),
		('The Reincarnated Young Lady Aim to Be an Adventurer',    'The Reincarnated Young Lady Aim to Be an Adventurer',                   'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False