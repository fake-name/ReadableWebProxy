def extractLemontreetranslationsWordpressCom(item):
	'''
	Parser for 'lemontreetranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('qt second female lead',                                          'Quick Transmigration Second Female Lead’s Counter Attack',                      'translated'),
		('Quick Transmigration Second Female Lead’s Counter Attack',       'Quick Transmigration Second Female Lead’s Counter Attack',                      'translated'),
		('Di Daughter\'s Rebirth: Sheng Shi Wang Fei',                     'Di Daughter\'s Rebirth: Sheng Shi Wang Fei',                                    'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False