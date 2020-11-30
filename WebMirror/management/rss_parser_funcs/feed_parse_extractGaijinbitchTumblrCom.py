def extractGaijinbitchTumblrCom(item):
	'''
	Parser for 'gaijinbitch.tumblr.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('prohibited isekai life',       'The Prohibited Isekai Life of a Certain Transmigrating Brother and Sister',                      'translated'),
		('he\'s not a lizard but a dragon',       'He’s Not a Lizard, But a Dragon ',                      'translated'),
		('story of gothic lady',       'The Story of Gothic Lady Who Met a Grave Keeper in Another World',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False