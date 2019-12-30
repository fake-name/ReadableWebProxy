def extractFlowermoontranslationsWordpressCom(item):
	'''
	Parser for 'flowermoontranslations.wordpress.com'
	'''

	if 'Manga' in item['tags']:
		return None
	if 'Notice' in item['tags']:
		return None
	if 'schedule' in item['tags']:
		return None

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	chp_prefixes = [
			('Case Files of the Genius Asshole',  'Case Files of the Genius Asshole',               'translated'),
			('Cat ',    'Me and My Beloved Cat (Girlfriend)',                                  'translated'),
		]

	for prefix, series, tl_type in chp_prefixes:
		if item['title'].lower().startswith(prefix.lower()):
			return buildReleaseMessageWithType(item, series, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)



	return False