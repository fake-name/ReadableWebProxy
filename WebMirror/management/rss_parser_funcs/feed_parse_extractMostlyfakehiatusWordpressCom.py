def extractMostlyfakehiatusWordpressCom(item):
	'''
	Parser for 'mostlyfakehiatus.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if "Baobei Baobei" in item['tags']:
		return buildReleaseMessageWithType(item, "Baobei Baobei", vol, chp, frag=frag, postfix=postfix)

	return False