def extractBetwixtedtranslationsBlogspotCom(item):
	'''
	Parser for 'betwixtedtranslations.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Transmigrated Senior Martial Brother',                          'Transmigrated Senior Martial Brother',                                         'translated'),
		('Part-Time Taoist Priest',                                       'Part-Time Taoist Priest',                                                      'translated'),
		('Criminal Psychology',                                           'Criminal Psychology',                                                          'translated'),
		('Death Progress Bar',                                            'Death Progress Bar',                                                           'translated'),
		('King of Classical Music',                                       'King of Classical Music',                                                      'translated'),
		('Everyday I Get up to See the Villain Stealing the Show',        'Everyday I Get up to See the Villain Stealing the Show',                       'translated'),
		('where is our agreement to be each other\'s arch rivals?',       'where is our agreement to be each other\'s arch rivals?',                      'translated'),
		('Gentle Beast',                                                  'Gentle Beast',                                                                 'translated'),
		('Epiphanies of Rebirth',                                         'Epiphanies of Rebirth',                                                        'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False