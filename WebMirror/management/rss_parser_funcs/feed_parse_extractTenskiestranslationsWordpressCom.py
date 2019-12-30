def extractTenskiestranslationsWordpressCom(item):
	'''
	Parser for 'tenskiestranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Automode ga kiremashita',       'Otome Game Rokkushuume, Automode ga Kiremashita',                      'translated'),
		('Otome Game Rokkushuume',        'Otome Game Rokkushuume, Automode ga Kiremashita',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False