def extractKaede721WordpressCom(item):
	'''
	Parser for 'kaede721.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Hakata Tonkotsu Ramens',                  'Hakata Tonkotsu Ramens',                      'translated'),
		('htr',                                     'Hakata Tonkotsu Ramens',                      'translated'),
		('durarara x hakata tonkotsu ramens',       'Durarara!! x Hakata Tonkotsu Ramens',         'translated'),
		('Durarara x HTR Crossover',                'Durarara!! x Hakata Tonkotsu Ramens',         'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False