def extractNovelbeartranslation001WordpressCom(item):
	'''
	Parser for 'novelbeartranslation001.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] == ['Uncategorized']:
		titlemap = [
			('To Be A Heartthrob In A Horror Movie ',               'To Be A Heartthrob In A Horror Movie',                   'translated'),
			('Rebirth: Degenerate Slave Abuses Tyrant ',            'Rebirth: Degenerate Slave Abuses Tyrant',                'translated'),
			('The Cold Regent Keeps a Fox as a Consort ',           'The Cold Regent Keeps a Fox as a Consort',               'translated'),
			('Holding On to My Man ',                               'Holding On to My Man',                                   'translated'),
			('Picking Up a General to Plow the Fields ',            'Picking Up a General to Plow the Fields',                'translated'),
			('So What If It’s an RPG World? ',                      'So What If It’s an RPG World?',                          'translated'),
			('Escape the Infinite Chamber ',                        'Escape the Infinite Chamber',                            'translated'),
			('True Star ',                                          'True Star',                                              'translated'),
			('The Marshals Want to Get Divorced ',                  'The Marshals Want to Get Divorced',                      'translated'),
			('Great Tang Idyll ',                                   'Great Tang Idyll',                                       'translated'),
			('I’ve Led the Villain Astray, How Do I Fix It? ',      'I’ve Led the Villain Astray, How Do I Fix It?',          'translated'),
			('Taoist Doctor ',                                      'Taoist Doctor',                                          'translated'),
			('The Dark King ',                                      'The Dark King',                                          'translated'),
			('Assassin Farmer ',                                    'Assassin Farmer',                                        'translated'),
			('Superstar Aspirations ',                              'Superstar Aspirations',                                  'translated'),
			('Superstar Aspiration ',                               'Superstar Aspiration',                                   'translated'),
			('Chu Wang Fei ',                                       'Chu Wang Fei',                                           'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False