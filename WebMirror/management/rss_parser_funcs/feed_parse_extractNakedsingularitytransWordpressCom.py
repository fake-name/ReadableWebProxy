def extractNakedsingularitytransWordpressCom(item):
	'''
	Parser for 'nakedsingularitytrans.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Alice Tale',                            'Nekama Shiyou to Omottara, Isekai Tensei Shite Onna ni Natta n da ga!',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False