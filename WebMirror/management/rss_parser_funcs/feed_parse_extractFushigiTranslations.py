def extractFushigiTranslations(item):
	'''
	Parser for 'Fushigi Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
		
	tagmap = [
		('Isekai Quest After School!',       'Isekai Quest After School!',                      'translated'),
		("Yuusha no Segare",                 "Yuusha no Segare",                                'translated'), 
		("Majo no Tabitabi",                 "Majo no Tabitabi",                                'translated'), 
		("Diego no Kyojin",                  "Diego no Kyojin",                                 'translated'), 
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		


	return False