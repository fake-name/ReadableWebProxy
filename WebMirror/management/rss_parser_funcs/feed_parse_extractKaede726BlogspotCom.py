def extractKaede726BlogspotCom(item):
	'''
	Parser for 'kaede726.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Epitome of Eighteen Histories',       'Durarara!! Epitome of Eighteen Histories',           'translated'),
		('Hakata Tonkotsu Ramens',              'Hakata Tonkotsu Ramens',                             'translated'),
		('Loiterous',                           'Loiterous',                                          'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('Durarara!! x Hakata Tonkotsu Ramens: Chapter ',  'Durarara!! x Hakata Tonkotsu Ramens',      'translated'),
		('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
		('Master of Dungeon',           'Master of Dungeon',               'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False