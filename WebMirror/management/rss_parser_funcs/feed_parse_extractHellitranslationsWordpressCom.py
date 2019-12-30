def extractHellitranslationsWordpressCom(item):
	'''
	Parser for 'hellitranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Rebirth of the Wolfish Silkpants Bottom',       'Rebirth of the Wolfish Silkpants Bottom',                      'translated'),
		('Demon Boss in the Human World',                 'Demon Boss in the Human World [Entertainment Circle]',         'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('RWSB Chapter',                'Rebirth of the Wolfish Silkpants Bottom',         'translated'),
		('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',                      'translated'),
		('Master of Dungeon',           'Master of Dungeon',                               'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False