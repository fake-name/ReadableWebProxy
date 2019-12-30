def extractMistyCloudTranslations(item):
	"""
	Misty Cloud Translations
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
		
	tagmap = [
		('Genius Doctor : The Black Belly Miss',                   'Genius Doctor: Black Belly Miss',                          'translated'),
		('Genius Doctor: Black Belly Miss',                        'Genius Doctor: Black Belly Miss',                          'translated'),
		('Prodigiously Amazing Weaponsmith',                       'Prodigiously Amazing Weaponsmith',                         'translated'),
		('Insanely Pampered Wife: Divine Doctor Fifth Young Miss', 'Insanely Pampered Wife: Divine Doctor Fifth Young Miss',   'translated'),
		('Insanely Pampered Wife: Genius Doctor Fifth Young Miss', 'Insanely Pampered Wife: Divine Doctor Fifth Young Miss',   'translated'),
		('Accompanying the Phoenix',                               'Accompanying the Phoenix',                                 'translated'),
		('Mesmerizing Ghost Doctor',                               'Mesmerizing Ghost Doctor',                                 'translated'), 
		('Overlord Love Me Tender',                                'Overlord, Love Me Tender',                                 'translated'), 
		('Godly Empress Doctor',                                   'Godly Empress Doctor',                                     'translated'), 
		('The Anarchic Consort',                                   'The Anarchic Consort',                                     'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
		
	return False