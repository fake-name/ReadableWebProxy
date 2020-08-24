def extractPiookyWordpressCom(item):
	'''
	Parser for 'piooky.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('quit the empress',       'I’ll Quit The Empress',                      'translated'),
		('beware of brothers',       'Beware of Brothers',                      'translated'),
		('abandoned empress 3',       'The Abandoned Empress',                      'translated'),
		('abandoned empress 4',       'The Abandoned Empress',                      'translated'),
		('abandoned empress 5',       'The Abandoned Empress',                      'translated'),
		('abandoned empress 6',       'The Abandoned Empress',                      'translated'),
		('abandoned empress 7',       'The Abandoned Empress',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False