def extractLazyfaerygardenWordpressCom(item):
	'''
	Parser for 'lazyfaerygarden.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('S:FAAM',       'Sonata: Fleeing to Avoid an Arrange Marriage',                                                'translated'),
		('adp',         'Addicted Pampering You: The Mysterious Pampered Wife of The Military Ye',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False