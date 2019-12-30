def extractMaddertranslatesCom(item):
	'''
	Parser for 'maddertranslates.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Form A Slaves Only Harem Guild',                                  'An S Rank Adventurer Me Along With Those Girls Who Are Slaves, Form A Slaves Only Harem Guild',                      'translated'),
		('IT IS A DIFFERENT WORLD AND YET I AM CULTIVATING MONSTERS',       'It Is A Different World And Yet I Am Cultivating Monsters',                                                          'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('The Bloodshot One-Eyed Zombie Emperor ',                                                         'The Bloodshot One-Eyed Zombie Emperor',                                                              'translated'),
		('An S Rank Adventurer Me Along With Those Girls Who Are Slaves, Form A Slaves Only Harem Guild',  'An S Rank Adventurer Me Along With Those Girls Who Are Slaves, Form A Slaves Only Harem Guild',      'translated'),
		('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
		('Master of Dungeon',           'Master of Dungeon',               'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False