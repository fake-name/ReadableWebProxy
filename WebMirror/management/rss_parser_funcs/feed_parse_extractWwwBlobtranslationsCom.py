def extractWwwBlobtranslationsCom(item):
	'''
	Parser for 'www.blobtranslations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		
	if "(Teaser)" in item['title']:
		return None

	tagmap = [
		('Side Character Transmigrations : The Final Boss is No Joke',       'Side Character Transmigrations : The Final Boss is No Joke',     'translated'),
		('Liu Yao: The Revitalization of Fuyao Sect',                        'Liu Yao: The Revitalization of Fuyao Sect',                      'translated'),
		('Demon Lord, Retry',                                                'Demon Lord, Retry',                                              'translated'),
		('Sheng Shi Wang Fei',                                               'Sheng Shi Wang Fei',                                             'translated'),
		('Lord and Dragon',                                                  'Lord and Dragon',                                                'translated'),
		('Perfect Superstar',                                                'Perfect Superstar',                                              'translated'),
		('My Youth Begins With Loving You',                                  'My Youth Begins With Loving You',                                'translated'),
		('Garudeina Oukoku Koukoku Ki',                                      'Garudeina Oukoku Koukoku Ki',                                    'translated'),
		('Sorrowful Legend of Kanashi Village',                              'Sorrowful Legend of Kanashi Village',                            'translated'),
		('herscherik',                                                       'Herscherik (Reincarnated Prince Series)',                        'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	urlfrag = [
		('/side-character-transmigrations-the-final-boss-is-no-joke/chapter-',       'Side Character Transmigrations : The Final Boss is No Joke',     'translated'),
	]

	for key, name, tl_type in urlfrag:
		if key in item['linkUrl'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False