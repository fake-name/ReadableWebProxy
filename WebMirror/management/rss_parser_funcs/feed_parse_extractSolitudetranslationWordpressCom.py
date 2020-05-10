def extractSolitudetranslationWordpressCom(item):
	'''
	Parser for 'solitudetranslation.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('shi ni modori, subete wo sukuu tame ni saikyou he to itaru',       'shi ni modori, subete wo sukuu tame ni saikyou he to itaru',                      'translated'),
		('subete wo sukuu tame ni saikyou he to itaru',                      'shi ni modori, subete wo sukuu tame ni saikyou he to itaru',                      'translated'),
		('shi ni modori',                                                    'shi ni modori, subete wo sukuu tame ni saikyou he to itaru',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False