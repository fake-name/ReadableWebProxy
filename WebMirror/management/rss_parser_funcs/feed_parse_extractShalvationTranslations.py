def extractShalvationTranslations(item):
	"""
	Shalvation Translations
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Dungeon Defense',                                           'Dungeon Defense',                                           'translated'),
		('Your and My Asylum',                                        'Your and My Asylum',                                        'translated'),
		('We Should Have Slept While Only Holding Hands, and Yet?!',  'We Should Have Slept While Only Holding Hands, and Yet?!',  'translated'),
		('Million Dollar Bill',                                       'Million Dollar Bill',                                       'translated'),
		('dungeon defense (wn)',                                      'dungeon defense (wn)',                                                     'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
		
	return False