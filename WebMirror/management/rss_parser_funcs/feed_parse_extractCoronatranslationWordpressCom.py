def extractCoronatranslationWordpressCom(item):
	'''
	Parser for 'coronatranslation.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('ldm',       'Lazy Dungeon Master',                      'translated'),
		('pmz',       'I was reincarnated as a villainess, but since I have become the beautiful woman of my dreams, that\'s plus-minus zero.',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False