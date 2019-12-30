def extractBcnovelsCom(item):
	'''
	Parser for 'bcnovels.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		
	if 'Manga' in item['tags']:
		return None

	tagmap = [
		('When the Protagonist of a Fanfiction',               'When a Fanfic Protagonist Transmigrated into the Original Novel',     'translated'),
		('Reader and Protagonist',                             'The Reader and Protagonist Definitely Have to Be in True Love',       'translated'),
		('Everyday the Protagonist Wants to Capture Me',       'Everyday the Protagonist Wants to Capture Me',                        'translated'),
		('Prince\'s Loyal Lover',                              'Prince\'s Loyal Lover',                                               'translated'),
		('The Scum Villain’s Self-Saving System',              'The Scum Villain\'s Self-Saving System',                              'translated'),
		('I Can’t Write Any ‘Below the Neck’ Love Scenes',     'I Can\'t Write Any \'Below the Neck\' Love Scenes',                   'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False