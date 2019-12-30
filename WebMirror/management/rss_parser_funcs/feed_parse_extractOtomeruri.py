def extractOtomeruri(item):
	'''
	Parser for 'OtomeRuri'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The World of the Pirate Consort',             'The World of the Pirate Consort',       'translated'),
		('Every Vicious Woman Needs a Loyal Man',       'Every Vicious Woman Needs a Loyal Man', 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False