def extractUntamedalleyCom(item):
	'''
	Parser for 'untamedalley.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('marshal\'s cannon fodder spouse',       'marshal\'s cannon fodder spouse',                      'translated'),
		('back to the age of the 80s',       'back to the age of the 80s',                      'translated'),
		('forced to be favored by the whole stars',       'forced to be favored by the whole stars',                      'translated'),
		('great at acting, now i\'m reborn',       'great at acting, now i\'m reborn',                      'translated'),
		('corpse wins after the end of the world',       'corpse wins after the end of the world',                      'translated'),
		('a hundred ways to kill a hearthrob',       'a hundred ways to kill a hearthrob',                      'translated'),
		('he has a dual personality',       'he has a dual personality',                      'translated'),
		('my family\'s idol\'s vest fell off',       'my family\'s idol\'s vest fell off',                      'translated'),
		('i\'m raking in billions in the aristocracy',       'i\'m raking in billions in the aristocracy',                      'translated'),
		('ttyiwftwwcoc',       'The Three Years When I Was Forced To Wear Women’s Clothing On Campus',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False