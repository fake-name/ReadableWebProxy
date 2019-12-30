def extractRosettaarchiveWordpressCom(item):
	'''
	Parser for 'rosettaarchive.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	if "R.A.M." in item['tags']:
		return buildReleaseMessageWithType(item, "R.A.M.", vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False