def extractWwwSakuranovelsCom(item):
	'''
	Parser for 'www.sakuranovels.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('I\'m Back in the Other World?',       'I\'m Back in the Other World?',                      'translated'),
		('Reincarnated Into Werewolf',          'Reincarnated Into Werewolf',                         'translated'),
		('Flash Marriage',                      'Flash Marriage',                                     'translated'),
		('Unexpected Marriage',                 'Unexpected Marriage',                                'translated'),
		('Magicraft Meister',                   'Magicraft Meister',                                  'translated'),
		('Spice of Life',                       'Spice of Life',                                      'translated'),
		('Awakening',                           'Awakening',                                          'translated'),
		('Law of the Devil',                    'Law of the Devil',                                   'translated'),
		('Help Gooogle Sensei',                 'Help Gooogle Sensei',                                'translated'),
		('Botsuraku',                           'Botsuraku Youtei Nanode, Kajishokunin wo Mezasu',    'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False