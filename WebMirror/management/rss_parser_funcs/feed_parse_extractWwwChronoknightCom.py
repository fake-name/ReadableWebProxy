def extractWwwChronoknightCom(item):
	'''
	Parser for 'www.chronoknight.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The World Is Overflowing with Monster',       'The World Is Overflowing with Monster, I’m Taking a Liking to This Life',                      'translated'),
		('The Auto-Mode Broke',                         'On the 6th Playthrough of the Otome Game, the Auto-Mode Broke',                                'translated'),
		('Kaifuku Jutsushi no Yarinaoshi ~ Sokushi Mahou to Skill Copy no Choetsu Heal',       'Kaifuku Jutsushi no Yarinaoshi ~ Sokushi Mahou to Skill Copy no Choetsu Heal',                      'translated'),
		('kuro no maou',                                'Kuro no Maou',                                                                                 'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False