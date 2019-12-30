def extractFeedProxy(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if item['title'].startswith('Comment'):
		return None
	
	bad_tags = [
			'TVB',
			'drama thoughts',
			'modern drama',
			'RAW',
			'Manga',
		]
	
	if any([tmp in item['tags'] for tmp in bad_tags]):
		return None
	
	tagmap = [
		('Princess Weiyang',                             'The Princess Wei Yang',                                                                              'translated'),
		('Ookura Teruko Detective Story Compilation',    'Ookura Teruko Detective Story Compilation',                                                          'translated'),
		('The Man Picked up by the Gods',                'Kamitachi ni Hirowareta Otoko',                                                                      'translated'),
		('Goblin Kingdom',                               'Goblin Kingdom',                                                                                     'translated'),
		('Growth Cheat',                                 "I've Became Able to Do Anything With My Growth Cheat, but I Can't Seem to Get Out of Being Jobless", 'translated'),
		('Invincible Saint',                             'Invincible Saint ~Salaryman, the Path I Walk to Survive in This Other World~',                       'translated'),
		('I came back but the world is still a fantasy', 'Kaettekite mo Fantasy!?',                                                                            'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	titlemap = [
		('The Man Picked up by the Gods -', 'Kamitachi ni Hirowareta Otoko', 'translated'),
		('Goblin Kingdom -',                'Goblin no Oukoku',              'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
	
	
	# So. this guy has zero useful tags. LOTS of useless tags, but zero useful ones.
	if '/~r/Xiakeluojiao/' in item['linkUrl']:
		if any(['Book' in tag for tag in item['tags']]):
			return buildReleaseMessageWithType(item, 'Zhu Xian', vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)
	
	return False