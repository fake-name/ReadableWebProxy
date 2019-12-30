def extractOtomeshishizaWordpressCom(item):
	'''
	Parser for 'otomeshishiza.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		
	if item['title'].startswith("Protected: "):
		return None

	tagmap = [
		('Love You 59 Seconds',                                            '[Online Gaming] Love You 59 Seconds',                             'translated'),
		('The Pregnant Woman Next Door How Are You Doing?',                'The Pregnant Woman Next Door, How Are You Doing?',                'translated'),
		('Ever Since I Take Home An Adonis Who Has Lost His Business',     'Ever Since I Take Home An Adonis Who Has Lost His Business',      'translated'),
		('The Love Story of A Passerby',                                   'The Love Story of A Passerby',                                    'translated'),
		('The Paternity Guard',                                            'The Paternity Guard',                                             'translated'),
		('Reincarnation of a Superstar',                                   'Reincarnation of a Superstar',                                    'translated'),
		('Friends With Benefits',                                          'Friends With Benefits',                                           'translated'),
		('YDXJ10',                                                         'Yandai Xie Jie No. 10',                                           'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False