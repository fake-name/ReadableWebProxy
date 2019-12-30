def extractFoxscoffeetimeWordpressCom(item):
	'''
	Parser for 'foxscoffeetime.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Otherworld dining hall (WN)',                                  'The Other World Dining Hall (WN)',                                                                'translated'), 
		('Tensei Saki ga Shoujo Manga no Shiro Buta Reijou datta',       'Tensei Saki ga Shoujo Manga no Shiro Buta Reijou datta',                                          'translated'), 
		('Troubled Knight',                                              'A Knight Troubled by Duke’s Daughter Who Drew Near, will Run away for the Time Being',            'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False