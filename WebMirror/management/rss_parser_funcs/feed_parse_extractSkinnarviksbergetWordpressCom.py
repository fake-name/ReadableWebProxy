def extractSkinnarviksbergetWordpressCom(item):
	'''
	Parser for 'skinnarviksberget.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] == ['未分类']:
		titlemap = [
			('Sinister Ex-Girlfriend',      'Sinister Ex-Girlfriend',          'translated'),
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
			('Handsome Friend',             'Handsome Friend',                 'translated'),
			('Strategy to Capture Men',     'Strategy to Capture Men',         'translated'),
			('before the divorce',          'before the divorce',              'translated'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	tagmap = [
		('handsome friend',          'handsome friend',                         'translated'),
		('before the divorce',       'before the divorce',                      'translated'),
		('stcm',                     'Strategy to Capture Men',                 'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False