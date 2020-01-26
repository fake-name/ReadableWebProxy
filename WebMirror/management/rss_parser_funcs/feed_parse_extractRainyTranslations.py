def extractRainyTranslations(item):
	"""
	Parser for 'Rainy Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	tagmap = [
		('rain',                   'rain',                                  'translated'),
		('F',                      'F ーエフー',                            'translated'),
		('Light and Shadow',       'Light and Shadow',                      'translated'),
		('The Daybreak',           'The Daybreak',                          'translated'),
		('adonis',                 'Adonis: Reminiscence',                  'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	if 'rain' in item['tags']:
		return buildReleaseMessageWithType(item, 'rain', vol, chp, frag=frag, postfix=postfix)
		
	return False