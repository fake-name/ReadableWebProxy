def extractCottoncandyteaCom(item):
	'''
	Parser for 'cottoncandytea.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Lady is a Stalker',                 'The Lady is a Stalker',                                'translated'),
		('Your Majesty is So Handsome',           'Your Majesty is So Handsome',                          'translated'),
		('the princess is going on strike',       'the princess is going on strike',                      'translated'),
		('For my Hero',                           'For my Hero',                                          'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False