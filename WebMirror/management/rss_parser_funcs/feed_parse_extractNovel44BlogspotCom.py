def extractNovel44BlogspotCom(item):
	'''
	Parser for 'novel44.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	
	tagmap = [
		('Is my elixir due to brainwashing effect? I wander in a different world',          'I use semen in another world and live by relying on other\'s power.',              'translated'),
		('Saikyou Juzoku Tensei',                                                           'Saikyou Juzoku Tensei',                                                            'translated'),
		('Isekai Majutsushi wa Mahou wo Tonaenai',                                          'Isekai Majutsushi wa Mahou wo Tonaenai',                                           'translated'),
		('Different world dungeon life',                                                    'Different World Dungeon Life',                                                     'translated'),
		('As The Spirit-Sama Says',                                                         'As The Spirit-Sama Says',                                                          'translated'),
		('I use semen in another world and live by relying on other\'s power.',             'I Use Semen in Another World and Live by Relying on Other\'s Power',               'translated'),
		('Flirting With Beast Girls! Doing Nothing but Copulation!',                        'Flirting With Beast Girls! Doing Nothing but Copulation!',                         'translated'),
		('Level Maker',                                                                     'Level Maker',                                                                      'translated'),
		('Fantasy world Oiliel',                                                            'Fantasy world Oiliel',                                                             'translated'),
		('Library of Heaven’s Path',                                                        'Library of Heaven’s Path',                                                         'translated'),
		('Isekai Cheat',                                                                    'Isekai Cheat',                                                                     'translated'),
		('Artifact planting space',                                                         'Artifact planting space',                                                          'translated'),
		
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	
	return False