def extractXiintranslationsWordpressCom(item):
	'''
	Parser for 'xiintranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('WTMT',                                          'Who Touched My Tail!',                                         'translated'),
		('Who Touched My Tail!',                          'Who Touched My Tail!',                                         'translated'),
		('Raising a Bun with a Daily Life System',        'Raising a Bun with a Daily Life System',                       'translated'),
		('BTTA',                                          'Back To The Apocalypse',                                       'translated'),
		('KDSP',                                          'Knight, the Dragon Snatched a Princess Again!',                'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False