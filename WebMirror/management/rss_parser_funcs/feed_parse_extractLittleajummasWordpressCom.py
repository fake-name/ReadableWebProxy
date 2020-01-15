def extractLittleajummasWordpressCom(item):
	'''
	Parser for 'littleajummas.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('imtmlip',       'I met the male lead in prison',                                'translated'),
		('smvb',          'the system for mentoring villain bosses',                      'translated'),
		('ladybaby',      'lady baby',                                                    'translated'),
		('ihtdd',         'i hid the duke\'s daughter',                                   'translated'),
		('isinqtbe',      'i\'m sorry i\'m not qualified to be empress',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False