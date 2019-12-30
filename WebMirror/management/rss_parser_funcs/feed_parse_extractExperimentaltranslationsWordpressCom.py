def extractExperimentaltranslationsWordpressCom(item):
	'''
	Parser for 'experimentaltranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Harrasing Thief Girl',       'Harrasing Thief Girl',                                          'translated'),
		('Armored Girl Monette',       'Armored Girl Monette',                                          'translated'),
		('Lucy Blanchett Remembered',  'Lucy Blanchett Remembered',                                     'translated'),
		('Slow Prison Life',           'Slow Prison Life',                                              'translated'),
		('grimoire master',            'Grimoire Master of an Everchanging World',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False