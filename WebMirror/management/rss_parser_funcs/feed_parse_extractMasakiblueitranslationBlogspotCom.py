def extractMasakiblueitranslationBlogspotCom(item):
	'''
	Parser for 'masakiblueitranslation.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('chichi wa eiyuu',                                      'My Father is a Hero, My Mother is a Spirit, the Daughter (Me) is a Reincarnator.',                               'translated'),
		('i want to be a receptionist of the magic world',       'I Want to Be a Receptionist in the Magic World',                                                                 'translated'),
		('Hazure Skill',                                         'Hazure Skill \'Mapping\' wo Te ni Shita Ore wa, Saikyou Party to Tomo ni Dungeon ni Idomu',                      'translated'),
		('mapping skill',                                        'Hazure Skill \'Mapping\' wo Te ni Shita Ore wa, Saikyou Party to Tomo ni Dungeon ni Idomu',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False