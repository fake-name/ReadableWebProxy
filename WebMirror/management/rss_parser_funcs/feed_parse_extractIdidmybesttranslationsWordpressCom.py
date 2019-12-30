def extractIdidmybesttranslationsWordpressCom(item):
	'''
	Parser for 'ididmybesttranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	if item['tags'] == ['Uncategorized']:
		titlemap = [
			('After Being Transported into a Book, I Adopted the Villain Chapter ',  'After Being Transported into a Book, I Adopted the Villain',      'translated'),
			('After Being Transported into a Book, I Adopted the Villain Ch. ',      'After Being Transported into a Book, I Adopted the Villain',      'translated'),
			('After Being Transported into a Book, I Adopted the Villain Ch.',      'After Being Transported into a Book, I Adopted the Villain',      'translated'),
			('Tensei Shoujo no Rirekisho',                                           'Tensei Shoujo no Rirekisho',                                      'translated'),
			('Master of Dungeon',                                                    'Master of Dungeon',                                               'oel'),
		]

		for titlecomponent, name, tl_type in titlemap:
			if titlecomponent.lower() in item['title'].lower():
				return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False