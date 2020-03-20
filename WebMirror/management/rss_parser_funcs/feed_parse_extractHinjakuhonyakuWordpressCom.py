def extractHinjakuhonyakuWordpressCom(item):
	'''
	Parser for 'hinjakuhonyaku.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('hellmode',                               'Hellmode ~Gamer Who Likes to Speedrun Becomes Peerless in a Parallel World with Obsolete Setting~',               'translated'),
		('the sole monster tamer in the world',    'The Sole Monster Tamer in the World ~I was Mistaken as the Demon King When I Changed My Job~',                    'translated'),
		('smt',                                    'The Sole Monster Tamer in the World ~I was Mistaken as the Demon King When I Changed My Job~',                    'translated'),
		('rose princess of hellrage',              'Rose Princess of Hellrage: Although I got Killed for Political Reasons, I got Revived as the Strongest Undead',   'translated'),
		('rph',                                    'Rose Princess of Hellrage: Although I got Killed for Political Reasons, I got Revived as the Strongest Undead',   'translated'),
		('my reality is a romance game',           'My Reality is a Romance Game',                                                                                    'translated'),
		('rrg',                                    'My Reality is a Romance Game',                                                                                    'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False