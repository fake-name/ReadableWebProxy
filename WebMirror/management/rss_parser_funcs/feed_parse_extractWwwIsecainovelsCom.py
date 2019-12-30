def extractWwwIsecainovelsCom(item):
	'''
	Parser for 'www.isecainovels.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Upstart Pastry Chef',                       'Upstart Pastry Chef ~Territory Management of a Genius Pâtissier~',                      'translated'),
		('Sono Mono Nochi ni',                        'That Person. Later on…',                                                                'translated'),
		('Starship Officer Becomes Adventurer',       'The Starship Officer Becomes An Adventurer',                                            'translated'),
		('The Wolf Lord\'s Lady',                     'The Wolf Lord\'s Lady',                                                                 'translated'),
		('Black Tea Specialist',                      'I am The Black Tea Specialist Cheat of The Chivalric Order!',                           'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False