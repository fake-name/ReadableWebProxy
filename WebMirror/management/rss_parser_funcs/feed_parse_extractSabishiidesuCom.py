def extractSabishiidesuCom(item):
	'''
	Parser for 'sabishiidesu.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Isekai Sagishi',                 'The Other World Con Artist’s Management Techniques',                      'translated'),
		('Saikyou no Budouka',             'Saikyou no Budouka',                                                      'translated'),
		('Saikyou no Butouka',             'Saikyou no Budouka',                                                      'translated'),
		('maou-sama kansatsu nikki',       'maou-sama kansatsu nikki',                                                'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False