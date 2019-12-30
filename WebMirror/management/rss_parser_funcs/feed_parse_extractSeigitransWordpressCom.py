def extractSeigitransWordpressCom(item):
	'''
	Parser for 'seigitrans.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	tagmap = [
		('Ex-Hero Candidate',       'Ex-Hero Candidate\'s, Who Turned Out To Be A Cheat From Lv2, Laid-back Life In Another World',                      'translated'),
		('Kujibiki Tokushou',       'Kujibiki Tokushou: Musou Hāremu ken',                                                                               'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False