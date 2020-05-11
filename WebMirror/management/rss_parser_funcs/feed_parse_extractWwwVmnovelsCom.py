def extractWwwVmnovelsCom(item):
	'''
	Parser for 'www.vmnovels.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Big Landlord',                         'The Big Landlord',                                        'translated'),
		('Let Me Shoulder This Blame',               'Let Me Shoulder This Blame',                              'translated'),
		('Quickly Wear The Face of The Devil',       'Quickly Wear The Face of The Devil',                      'translated'),
		('didn’t love you enough',                   'didn\'t love you enough',                                 'translated'),
		('let me shoulder this blame!',              'let me shoulder this blame!',                             'translated'),
		('transmigrated into a school idol',         'transmigrated into a school idol',                        'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	if 'ml 2 and ml 3 happy ending!' in item['tags']:
		if chp == 2 or chp == 3:
			return None
		return buildReleaseMessageWithType(item, 'Male Lead 2 and Male Lead 3 Happy Ending!', vol, chp, frag=frag, postfix=postfix, tl_type='translated')

	if item['tags'] == ['Uncategorized'] or item['tags'] == ['fanfiction']:
		titlemap = [
			('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
			('Tightrope',                   'Tightrope',                       'oel'),
			('Master of Dungeon',           'Master of Dungeon',               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False