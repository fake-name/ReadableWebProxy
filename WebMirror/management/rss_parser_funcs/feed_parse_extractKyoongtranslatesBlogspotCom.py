def extractKyoongtranslatesBlogspotCom(item):
	'''
	Parser for 'kyoongtranslates.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('monster inn rectification report',       'Monster Inn Rectification Report',                      'translated'),
		('after the vicious male partner marries the disabled villain',       'after the vicious male partner marries the disabled villain',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False