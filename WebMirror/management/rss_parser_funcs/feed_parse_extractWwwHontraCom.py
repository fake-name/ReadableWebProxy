def extractWwwHontraCom(item):
	'''
	Parser for 'www.hontra.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Ex-Hero-Book',       'The Laid-back Life in Another World of the Ex-Hero Candidate Who Turned out to be a Cheat from Level 2',                      'translated'),
		('PRC',                'PRC',                      'translated'),
		('Loiterous',          'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False