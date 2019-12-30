def extractHoneypeachtxtHomeBlog(item):
	'''
	Parser for 'honeypeachtxt.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if item['tags'] == ['tidak dikategorikan']:
		titlemap = [
			('Long Live Your Majesty Chapter ',           'Long Live Your Majesty',               'translated'),
			('Across A Millennium to Love You Chapter ',  'Across A Millennium to Love You',      'translated'),
			('Your Majesty Please Calm Down Chapter ',    'Your Majesty Please Calm Down',        'translated'),
			('War Love Snow Chapter ',                    'War Love Snow',                        'translated'),
			('Tensei Shoujo no Rirekisho',                'Tensei Shoujo no Rirekisho',           'translated'),
			('Master of Dungeon',                         'Master of Dungeon',                    'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	tagmap = [
		('war love snow',                       'war love snow',                                      'translated'),
		('Your Majesty Please Calm Down',       'Your Majesty Please Calm Down',                      'translated'),
		('long live your majesty',              'long live your majesty',                             'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False