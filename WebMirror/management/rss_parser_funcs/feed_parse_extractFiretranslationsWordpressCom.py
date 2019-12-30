def extractFiretranslationsWordpressCom(item):
	'''
	Parser for 'firetranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Konjiki no Word Master',       'Konjiki no Moji Tsukai',                      'translated'),
		('Konjiki no Moji Tsukai',       'Konjiki no Moji Tsukai',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False