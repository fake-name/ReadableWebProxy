def extractWeissnoveltranslationWordpressCom(item):
	'''
	Parser for 'weissnoveltranslation.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The School Prince is a Girl',         'The School Prince is a Girl',                        'translated'),
		('Mr. President, Unbridled Love',       'Mr. President, Unbridled Love',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	return False