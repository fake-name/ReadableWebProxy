def extractEndlessfantasyTranslations(item):
	"""
	Parser for 'EndlessFantasy Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	
	if 'fanfic' in item['title'].lower():
		return None

	
	titlemap = [		
		('My Father-in-law is Lu Bu – ',                                        'My Father-in-law is Lu Bu',                                      'translated'), 
		('My Father-in-law is Lu Bu Chapter',                                   'My Father-in-law is Lu Bu',                 'translated'), 
		('Masked Knight – ',                                                    'Masked Knight',                                                  'translated'), 
		('Masked Knight Chapter',                                               'Masked Knight',                                                  'translated'), 
		('Epoch of Twilight – Chapter',                                         'Epoch of Twilight',                                              'translated'), 
			
		('Age of Cosmic Exploration – Chapter',                                 'Age of Cosmic Exploration',                                      'translated'), 
		('MMORPG: Rebirth of the Legendary Guardian- Chapter',                  'MMORPG: Rebirth of the Legendary Guardian',                      'translated'), 
		('MMORPG: Rebirth of the Legendary Guardian – Chapter',                 'MMORPG: Rebirth of the Legendary Guardian',                      'translated'), 
		('MMORPG: Rebirth of the Legendary Guardian : Chapter',                 'MMORPG: Rebirth of the Legendary Guardian',                      'translated'), 
		
		('Full Marks Hidden Marriage: Pick Up a Son, Get a Free Husband –',     'Full Marks Hidden Marriage: Pick Up a Son, Get a Free Husband',  'translated'), 
		('I Am Supreme – Chapter',                                              'I am Supreme',                                                   'translated'), 
		('Pursuit of the Truth –',                                              'Pursuit of the Truth',                                           'translated'), 
			
			
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
		
	return False