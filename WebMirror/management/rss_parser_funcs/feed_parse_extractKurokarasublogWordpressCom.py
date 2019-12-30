def extractKurokarasublogWordpressCom(item):
	'''
	Parser for 'kurokarasublog.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('POTATOES ARE THE ONLY THING THAT’S NEEDED IN THIS WORLD! Chapter ',   'Potatoes Are the Only Thing That\'s Needed in This World!',      'translated'),
		('Potatoes are the only things that’s needed in this world! Chapter ',  'Potatoes Are the Only Thing That\'s Needed in This World!',      'translated'),
		('LITERARY SUPERSTAR – CHAPTER ',                                       'Literary Superstar',                                             'translated'),
		('Master of Dungeon',           'Master of Dungeon',               'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	tagmap = [
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False