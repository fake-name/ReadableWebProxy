def extractEdentranslationsblogWordpressCom(item):
	'''
	Parser for 'edentranslationsblog.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if "School Beauty Personal Bodyguard" in item['tags']:
		return buildReleaseMessageWithType(item, "School Beauty Personal Bodyguard", vol, chp, frag=frag, postfix=postfix)

	return False