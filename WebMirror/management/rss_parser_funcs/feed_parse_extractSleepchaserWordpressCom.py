def extractSleepchaserWordpressCom(item):
	'''
	Parser for 'sleepchaser.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Violant of the Silver',                   'Violant of the Silver',                                  'translated'),
		('Nurturing the Hero to Avoid Death',       'Nurturing the Hero to Avoid Death',                      'translated'),
		('Fei Pin Ying Qiang',                      'Fei Pin Ying Qiang',                                     'translated'),
		('The Job of an Imperial Concubine',        'The Job of an Imperial Concubine',                       'translated'),
		('Villain Days',                            'Villain Days',                                           'translated'),
		('Story of Yanxi Palace',                   'Story of Yanxi Palace',                                  'translated'),
		('the times spent in pretense',             'the times spent in pretense',                            'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)




	return False