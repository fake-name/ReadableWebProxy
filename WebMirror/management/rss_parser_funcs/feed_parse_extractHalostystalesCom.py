def extractHalostystalesCom(item):
	'''
	Parser for 'halostystales.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('I\'m Gonna be a Wizard When I Grow up Again!',         'I\'m Gonna be a Wizard When I Grow up Again!',                'oel'),
		('blood',                                                'Blood',                                                       'oel'),
		('The Immortal Berserker',                               'The Immortal Berserker',                                      'oel'),
		('Strength',                                             'The Only Thing I Can Upgrade Is Strength',                    'oel'),
		('uwom',                                                 'Unspoken Words of Magic',                                     'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False