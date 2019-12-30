def extractDreamsofyesteryearWordpressCom(item):
	'''
	Parser for 'dreamsofyesteryear.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if item['title'].startswith("Chapter "):
		return buildReleaseMessageWithType(item, "Emperor of the Human Way", vol, chp, frag=frag, postfix=postfix)

	return False