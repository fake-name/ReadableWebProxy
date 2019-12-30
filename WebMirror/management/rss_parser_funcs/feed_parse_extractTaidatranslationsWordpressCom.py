def extractTaidatranslationsWordpressCom(item):
	'''
	Parser for 'taidatranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Nightmare Game',           'Nightmare Game',                          'translated'),
		('Escape the Chamber',       'Escape the Chamber',                      'translated'),
		('Sha Qing',                 'Sha Qing',                                'translated'),
		('IWY',                      'I Am Incomplete Without You',             'translated'),
		('KoD',                      'Kaleidoscope of Death',                   'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False