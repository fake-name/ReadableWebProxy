def extractCosysphereWordpressCom(item):
	'''
	Parser for 'cosysphere.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Into the World of Medicine',                       'Into the World of Medicine',                      'translated'), 
		('MGSSGW',                                           'Major General Spoils his Soul-guiding Wife',                      'translated'), 
		('Major General Spoils his Soul-guiding Wife',       'Major General Spoils his Soul-guiding Wife',                      'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False