def extractPandaTranslations(item):
	"""
	Parser for 'Panda Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Divine Genius Healer, Abandoned Woman',       'Divine Genius Healer, Abandoned Woman: Demonic Tyrant in Love with a Mad Little Consort',   'translated'), 
		('World Destroying Demonic Emperor',            'World Destroying Demonic Emperor',                                                          'translated'), 
		('Mechanical God Emperor',                      'Mechanical God Emperor',                                                                    'translated'), 
		('The Assassin\'s Apprentice',                  'The Assassin\'s Apprentice',                                                                'translated'), 
		('Curse the Gods, Obliterate the Heavens',      'Curse the Gods, Obliterate the Heavens',                                                    'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	titlemap = [
		('Divine Godly Healer, Abandoned Woman',         'Divine Genius Healer, Abandoned Woman: Demonic Tyrant in Love with a Mad Little Consort',      'translated'),
		('Divine Genius Healer, Abandoned Woman',        'Divine Genius Healer, Abandoned Woman: Demonic Tyrant in Love with a Mad Little Consort',      'translated'),
		('DGHAW',                                        'Divine Genius Healer, Abandoned Woman: Demonic Tyrant in Love with a Mad Little Consort',      'translated'),
		('World Destroying Demonic Emperor',             'World Destroying Demonic Emperor',                                                             'translated'),
		('WDDE: ',                                       'World Destroying Demonic Emperor',                                                             'translated'),
		('TAA: ',                                        'The Assassin\'s Apprentice',                                                                   'translated'),
		('The Assassin’s Apprentice',                    'The Assassin\'s Apprentice',                                                                   'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False