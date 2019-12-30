def extractThebrilliantjadeinaiWordpressCom(item):
	'''
	Parser for 'thebrilliantjadeinai.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Marielle Clarac\'s Engagement',                                                        'Marielle Clarac\'s Engagement',                                       'translated'),
		('The Magician wants Normality',                                                         'The Magician wants Normality',                                        'translated'),
		('TMWN',                                                                                 'The Magician wants Normality',                                        'translated'),
		('I am a princess responsible for settling circumstances',                               'I am a princess responsible for settling circumstances',              'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	if item['tags'] != ['Senza categoria']:
		return False
		
	titlemap = [
		('The Magician Wants Normality',  'The Magician Wants Normality',      'translated'),
		('Master of Dungeon',           'Master of Dungeon',               'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False