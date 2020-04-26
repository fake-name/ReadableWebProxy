def extractWwwTherovinggriotCom(item):
	'''
	Parser for 'www.therovinggriot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None


	badwords = [
			'review',
		]
	if any([bad in item['tags'] for bad in badwords]):
		return None



	tagmap = [
		('recapture the entertainment industry',       'recapture the entertainment industry',                      'translated'),
		('recapturetheentertainmentindustry',          'recapture the entertainment industry',                      'translated'),
		('rtei',                                       'recapture the entertainment industry',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False