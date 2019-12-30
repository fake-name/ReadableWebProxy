def extractDandanmeintranslationsWordpressCom(item):
	'''
	Parser for 'dandanmeintranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Feng Mang',       'Feng Mang',                      'translated'),
		('Blood Contract',       'Blood Contract',                      'translated'),
		('Aloof King and Cool-Acting Queen',       'Aloof King and Cool-Acting Queen',                      'translated'),
		('Bring Along a Ball and Hiding from Foreign Devils',       'Bring Along a Ball and Hiding from Foreign Devils',                      'translated'),
		('The Wife is First',       'The Wife is First',                      'translated'),
		('Begging You to Break Off This Engagement!',       'Begging You to Break Off This Engagement!',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False