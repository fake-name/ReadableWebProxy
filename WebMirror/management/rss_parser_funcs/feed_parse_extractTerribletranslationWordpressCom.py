def extractTerribletranslationWordpressCom(item):
	'''
	Parser for 'terribletranslation.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Film Emperor\'s Adorable Wife From Ancient Times',              'Film Emperor\'s Adorable Wife From Ancient Times',                             'translated'),
		('There\'s A Beauty',                                             'There\'s A Beauty',                                                            'translated'),
		('End of the world\'s reborn cannon fodder counterattacks',       'The End of The World\'s Reborn Cannon fodder Counter-attacks',                 'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False