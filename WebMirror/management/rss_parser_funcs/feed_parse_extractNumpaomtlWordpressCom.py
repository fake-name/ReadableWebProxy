def extractNumpaomtlWordpressCom(item):
	'''
	Parser for 'numpaomtl.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
		
	if '100WTGMG' in item['tags'] and chp == 100 or frag == 100:
		return None

	tagmap = [
		('Lovable Package',       'Lovable Package',                                                                  'translated'),
		('100WTGMG',              '100 Ways to Get the Male God',                                                     'translated'),
		('TMGFIADTF',             'The Male God\'s Favorable Impressions Are Difficult to Farm',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False