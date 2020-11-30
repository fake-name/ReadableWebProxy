def extractShinTranslations(item):
	"""
	# Shin Translations

	"""
	
	
	badwords = [
			'Status Update',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None


	
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		
	tagmap = [
		('THE NEW GATE',                                                     'The New Gate',                                          'translated'),
		('starting a new life for the discarded all-rounder',                'Starting a New Life for the Discarded All-Rounder',     'translated'),
		('dar',                                                              'Starting a New Life for the Discarded All-Rounder',     'translated'),
		('previous life was sword emperor. this life is trash prince.',      'Previous Life was Sword Emperor. This Life is Trash Prince.',                               'translated'),
		('twem',                'i was summoned to another world, but also called useless and kicked out. ~this world was easy mode for me~',                               'translated'),
		('i was summoned to another world, but also called useless and kicked out. ~this world was easy mode for me~',                'i was summoned to another world, but also called useless and kicked out. ~this world was easy mode for me~',                               'translated'),
		('bbyw',                'i\'m a bastard but you\'re worse!',                               'translated'),
		('i\'m a bastard but you\'re worse!',                'i\'m a bastard but you\'re worse!',                               'translated'),
		('PRC',                'PRC',                               'translated'),
		('Loiterous',          'Loiterous',                         'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False