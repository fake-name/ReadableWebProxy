def extractNaedatranslationsHomeBlog(item):
	'''
	Parser for 'naedatranslations.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('TBAFIAHM',       'To Be a Heartthrob in a Horror Movie',                      'translated'),
		('TBAHIAHM',       'To Be a Heartthrob in a Horror Movie',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False