def extractJiamintranslationCom(item):
	'''
	Parser for 'jiamintranslation.com'
	'''
	if 'Calligraphy' in item['tags']:
		return None

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('HAWRR',       'Quick Transmigration: Heroine Arrives, Woman Rapidly Retreats!',        'translated'),
		('VNG',         'The Inner Palace Tale of a Villainess Noble Girl',                      'translated'),
		('TTTW',        'Traveler of the Ten Thousand Worlds',                                   'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False