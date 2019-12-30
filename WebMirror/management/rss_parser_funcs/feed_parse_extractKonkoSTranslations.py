def extractKonkoSTranslations(item):
	"""
	Parser for 'Konko's Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('I Bought a Girl',                           'I Bought a Girl',                                  'translated'), 
		('Elf',                                       'Kuishinbo Elf',                                    'translated'), 
		('The strongest 10 years old magician',       'Juu Sai no Saikyou Madoushi',                      'translated'), 
		('Cheat na Kaineko',                          'Cheat na Kaineko no Okage de Rakuraku Level Up',   'translated'), 
		('Pervert Healer',                            'I Work As A Healer In Another World\'s Labyrinth City',   'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False