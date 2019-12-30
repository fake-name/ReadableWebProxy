def extractLuukiaTumblrCom(item):
	'''
	Parser for 'luukia.tumblr.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('alsar',                   'Alsar',                                      'translated'),
		('Devil\'s Origin',         'The Devil\'s Origin',                        'translated'),
		('PRC',         'PRC',                        'translated'),
		('Loiterous',   'Loiterous',                  'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	titlemap = [
		('Alsar',       'Alsar',                      'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False