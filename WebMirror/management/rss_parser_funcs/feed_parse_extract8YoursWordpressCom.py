def extract8YoursWordpressCom(item):
	'''
	Parser for '8yours.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if "23:11" in item['tags'] or "11/23":
		return buildReleaseMessageWithType(item, "23:11", vol, chp, frag=frag, postfix=postfix)

	return False