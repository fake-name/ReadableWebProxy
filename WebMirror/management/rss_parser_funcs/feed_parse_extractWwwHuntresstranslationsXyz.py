def extractWwwHuntresstranslationsXyz(item):
	'''
	Parser for 'www.huntresstranslations.xyz'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Male Lead You\'re Overpowered',       'Quick Transmigration: Male Lead, You\'re Overpowered?',                      'translated'),
		('MLYO',                                'Quick Transmigration: Male Lead, You\'re Overpowered?',                      'translated'),
		('PRC',                                 'PRC',                      'translated'),
		('Loiterous',                           'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False