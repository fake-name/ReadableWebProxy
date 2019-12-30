def extractBurstingchrysanthemumsTumblrCom(item):
	'''
	Parser for 'burstingchrysanthemums.tumblr.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Reader and Protagonist Definitely Have to Be in True Love',                'The Reader and Protagonist Definitely Have to Be in True Love',                               'translated'),
		('The Daily Task of Preventing My Disciple from Turning to the Dark Side',       'The Daily Task of Preventing My Disciple from Turning to the Dark Side',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False