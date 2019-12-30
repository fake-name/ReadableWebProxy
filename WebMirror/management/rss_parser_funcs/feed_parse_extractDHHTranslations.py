def extractDHHTranslations(item):
	"""
	# 'DHH Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
	
	if 'Video Games' in item['tags']:
		return None
		

	tagmap = [
		("god's left hand",                             "god's left hand",                             'translated'),
		("you're beautiful when you smile",             "You're Beautiful When You Smile",             'translated'),
		('undefeatable - league of legends',            'Undefeated - League of Legends',              'translated'),
		('fish playing while trapped in a secret room', 'Fish Playing While Trapped in a Secret Room', 'translated'),
		('Shui Fu Shen Qing',                           'Shui Fu Shen Qing',                           'translated'),
		('The Most Majestic You',                       'The Most Majestic You',                       'translated'),
		('Mo Bao Fei Bao',                              'Mo Bao Fei Bao',                              'translated'),
		('Starlight Has No Past',                       'Starlight Has No Past',                       'translated'),
		('Those Sweet Times',                           'Those Sweet Times',                           'translated'),

		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	if item['title'].startswith('Tea of Summer - Chapter'):
		return buildReleaseMessageWithType(item, 'Tea of Summer', vol, chp, frag=frag, postfix=postfix)
	return False