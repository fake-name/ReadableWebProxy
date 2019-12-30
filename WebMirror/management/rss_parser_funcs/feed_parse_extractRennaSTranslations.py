def extractRennaSTranslations(item):
	"""
	Parser for 'Renna's Translations'
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	if 'asks' in item['tags']:
		return None
		
	tagmap = [
		('The Schoolgirl Detective and Eccentric Author',       'The Schoolgirl Detective and Eccentric Author',                      'translated'),
		('Picture Book of My First Love',                       'Picture Book of My First Love',                                      'translated'),
		('a solution for jealousy',                             'a solution for jealousy',                                            'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False