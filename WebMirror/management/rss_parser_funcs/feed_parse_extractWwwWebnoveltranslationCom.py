def extractWwwWebnoveltranslationCom(item):
	'''
	Parser for 'www.webnoveltranslation.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('the universal plugins for online games',       'the universal plugins for online games',                      'translated'),
		('the city\'s strongest immortal emperor',       'the city\'s strongest immortal emperor',                      'translated'),
		('desperate mobile game',                        'desperate mobile game',                                       'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False