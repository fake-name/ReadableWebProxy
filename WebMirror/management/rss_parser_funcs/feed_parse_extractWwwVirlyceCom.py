def extractWwwVirlyceCom(item):
	'''
	Parser for 'www.virlyce.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('The Blue Mage Raised by Dragons', 'The Blue Mage Raised by Dragons',                'oel'),
		('TBMRbD',                          'The Blue Mage Raised by Dragons',                'oel'),
		('The Godking\'s Legacy',           'The Godking\'s Legacy',                          'oel'),
		('Demon\'s Journey',                'Demon\'s Journey',                               'oel'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False