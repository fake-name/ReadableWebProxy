def extractKirikoTranslations(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
	if 'KnW' in item['tags'] or 'KnW Chapter' in item['title']:
		postfix = item['title'].split(':', 1)[-1].strip()
		return buildReleaseMessageWithType(item, 'Konjiki no Wordmaster', vol, chp, frag=frag, postfix=postfix)
		
		

	tagmap = [
		('Shinwa Densetsu',                                                          'Shinwa Densetsu no Eiyuu no Isekaitan',                                                        'translated'),
		('Common Sense of a Warrior House',                                          'Common Sense of a Warrior House',                                                              'translated'),
		('AkaHoshi',                                                                 'The Different World with the Red Star Chapters',                                               'translated'),
		('The Magnificent Battle Records of a Former Noble Lady',                    'The Magnificent Battle Records of a Former Noble Lady',                                        'translated'),
		('After the Ending the Magical Girl Earnestly Hides Her True Identity',      'After the Ending the Magical Girl Earnestly Hides Her True Identity',                          'translated'),
		('mt. hororyuu',                                                             'The Life of Mt. Dragonends: The Forefather of all Life and Magic at 4.6 Billion Years Old',    'translated'),
		
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


		
	return False