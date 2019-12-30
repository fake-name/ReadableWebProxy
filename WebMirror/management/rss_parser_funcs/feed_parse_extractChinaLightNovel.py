def extractChinaLightNovel(item):
	"""
	China Light Novel
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('Twin Sword',                 'Twin Sword',                                'translated'),
		('Devil\'s Examination',       'Devil\'s Examination',                      'translated'),
		('Against the Fate',           'Against the Fate',                          'translated'),
		('a thief\'s bravery',         'a thief\'s bravery',                        'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False