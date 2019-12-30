def extractSakuraidreaderWordpressCom(item):
	'''
	Parser for 'sakuraidreader.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('ring ring',                             'ring ring',                                            'translated'), 
		('Graceling: The Girl With Time',         'Graceling: The Girl With Time',                        'oel'), 
		('Imagine Online: The Game',              'Imagine Online: The Game',                             'oel'), 
		('Suzaku: The Phoenix God of Fire',       'Suzaku: The Phoenix God of Fire',                      'oel'), 
		('1 Soul, 2 lives',                       '1 Soul, 2 lives',                                      'oel'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False