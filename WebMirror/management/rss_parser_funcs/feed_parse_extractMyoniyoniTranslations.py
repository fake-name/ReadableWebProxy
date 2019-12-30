def extractMyoniyoniTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
		
	tagmap = [
		('Prince of the Octagon',          'Prince of the Octagon',          'translated'),
		('Beautiful Top Star',             'Beautiful Top Star',             'translated'),
		('Swordmaster Healer',             'Swordmaster Healer',             'translated'),
		('Valhalla Saga',                  'Valhalla Saga',                  'translated'),
		('Top Management',                 'Top Management',                 'translated'),
		('The King of the Battlefield',    'The King of the Battlefield',    'translated'),
		('Sovereign of Judgement',         'Sovereign of Judgement',         'translated'),
		('Taming Master',                  'Taming Master',                  'translated'),
		("God's Song",                     "God's Song",                     'translated'),
		('Life Mission',                   'Life Mission',                   'translated'),
		('Demon King & Hero',              'Demon King & Hero',              'translated'),
		('Sovereign of Judgment',          'Sovereign of Judgment',          'translated'),
		('God of Tennis',                  'God of Tennis',                  'translated'),
		('Kill the Hero',                  'Kill the Hero',                  'translated'),
		('Grand Slam',                     'Grand Slam',                     'translated'),
		('The Overlord of Blood and Iron', 'The Overlord of Blood and Iron', 'translated'),
		('Spirit Sword',                   'Spirit Sword',                   'translated'),
		('The Legendary Engie',            'The Legendary Engie',            'translated'),
		('Suspicious Manager Moon',        'Suspicious Manager Moon',        'translated'),
		('Absolute on the Mound',          'Absolute on the Mound',          'translated'),
		('I Became the Hero\'s Bride',     'I Became the Hero\'s Bride',     'translated'),
		
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False