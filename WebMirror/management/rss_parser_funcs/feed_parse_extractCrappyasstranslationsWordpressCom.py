def extractCrappyasstranslationsWordpressCom(item):
	'''
	Parser for 'crappyasstranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Konyaku-sha ga Akuyaku de Komattemasu',                  'Konyaku-sha ga Akuyaku de Komattemasu',                                 'translated'),
		('kuroneko ouji wa tsukiyo ni warau',                      'The Black Cat Prince Laughed At The Moon',                              'translated'),
		('The Black Cat Prince Laughed At The Moon',               'The Black Cat Prince Laughed At The Moon',                              'translated'),
		('The Me Who Wants To Escape The Princess Training',       'The Me Who Wants To Escape The Princess Training',                      'translated'),
		('The Civil Officer Can Have Sweet Dreams',                'The Civil Officer Can Have Sweet Dreams',                               'translated'),
		('Everyday Is Fun Mob',                                    'I May Be A Mob But Because My Favorite Is Here, Everyday Is Fun',       'translated'),
		('Lady Philia D\'la Love\'s Mistakes',                     'Lady Philia D\'la Love\'s Mistakes',                                    'translated'),
		('The Reincarnated Young Lady Aim to Be an Adventurer',     'The Reincarnated Young Lady Aim to Be an Adventurer',                    'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False