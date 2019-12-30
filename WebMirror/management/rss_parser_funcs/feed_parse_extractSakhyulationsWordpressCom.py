def extractSakhyulationsWordpressCom(item):
	'''
	Parser for 'sakhyulations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Villain\'s White Lotus Halo',                          'The Villain\'s White Lotus Halo',                                         'translated'),
		('Heaven Official\'s Blessing',                              'Heaven Official\'s Blessing',                                             'translated'),
		('My Former Significant Others Were All Alphas [abo]',       'My Former Significant Others Were All Alphas [abo]',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	titlemap = [
		('I’ve Led the Villain Astray, How Do I Fix It?',      'I’ve Led the Villain Astray, How Do I Fix It?',      'translated'), 
		('The Promotion Record of a Crown Princess Chapter ',  'The Promotion Record of a Crown Princess',      'translated'), 
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False