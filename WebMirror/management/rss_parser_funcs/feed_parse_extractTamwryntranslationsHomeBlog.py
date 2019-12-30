def extractTamwryntranslationsHomeBlog(item):
	'''
	Parser for 'tamwryntranslations.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Boss\'s Death Guide',              'Boss\'s Death Guide',                             'translated'),
		('Always with the Old Attack',       'Always with the Old Attack',                      'translated'),
		('Unlimited Cycles of Death',        'Unlimited Cycles of Death',                       'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False