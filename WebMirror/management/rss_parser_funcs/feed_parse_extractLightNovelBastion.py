def extractLightNovelBastion(item):
	"""
	Parser for 'Light Novel Bastion'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	titlemap = [
		('Isaac',                                 'Isaac',                                                 'translated'),
		('Isekai Tensei Soudouki',                'Isekai Tensei Soudouki',                                'translated'),
		('The Youngest Son of Sunyang',           'The Youngest Son of Sunyang',                           'translated'),
		('Hunter of the Ruined World',            'Hunter of the Ruined World',                            'translated'),
		('The Tutorial Is Too Hard',              'The Tutorial Is Too Hard',                              'translated'),
		('The World After the Fall',              'The World After the Fall',                              'translated'),
		('KnM ',                                  'Kuro no Maou',                                          'translated'),
		('Kuro no Maou',                          'Kuro no Maou',                                          'translated'),
		('Nidome no Yuusha V',                    'Nidome no Yuusha',                                      'translated'),
		('White Wolves',                          'White Wolves',                                          'translated'),
		('Dungeon Maker ',                        'Dungeon Maker',                                         'translated'),
		('Max LeveL Newbie',                      'Max LeveL Newbie',                                      'translated'),
		('The Lazy Swordmaster',                  'The Lazy Swordmaster',                                  'translated'),
		('The Lazy  Swordmaster',                 'The Lazy Swordmaster',                                  'translated'),
		('You shine in the moonlit night',        'You Shine in the Moonlit Night',                        'translated'),
		('Death Mage',                            'The Death Mage that doesn\'t want a fourth time',       'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False