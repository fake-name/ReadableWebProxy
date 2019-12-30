def extractHikokitranslationsWordpressCom(item):
	'''
	Parser for 'hikokitranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	titlemap = [
		('Isekai Mahou wa Okureteru! (LN)',  'Isekai Mahou wa Okureteru! (LN)',      'translated'),
		('Isekai Mahou wa Okureteru!',       'Isekai Mahou wa Okureteru!',           'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False