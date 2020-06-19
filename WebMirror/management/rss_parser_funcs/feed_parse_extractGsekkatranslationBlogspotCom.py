def extractGsekkatranslationBlogspotCom(item):
	'''
	Parser for 'gsekkatranslation.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('skkn',                                  'Saikyou Kenja no Kosodate Nikki ～Uchi no Musume ga Sekaiichi Kawaii Ken ni Tsuite～',                      'translated'),
		('saikyou kenja no kosodate nikki',       'Saikyou Kenja no Kosodate Nikki ～Uchi no Musume ga Sekaiichi Kawaii Ken ni Tsuite～',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False