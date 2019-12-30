def extractTenseikenWordpressCom(item):
	'''
	Parser for 'tenseiken.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Tensei Shitara Ken Deshita',       'I Was a Sword When I Reincarnated',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	titlemap = [
		('Tensei Shitara Ken Deshita!',  'I Was a Sword When I Reincarnated',                                                                          'translated'),
		('TSKD ',                        'I Was a Sword When I Reincarnated',                                                                          'translated'),
		('Jingai Musume ',               'I Became the Demon Lord so I Created a Dungeon and Spend Heartwarming Time There with Non-Human Girls',      'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False