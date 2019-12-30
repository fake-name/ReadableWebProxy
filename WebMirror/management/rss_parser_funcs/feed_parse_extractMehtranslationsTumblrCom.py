def extractMehtranslationsTumblrCom(item):
	'''
	Parser for 'mehtranslations.tumblr.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Space Rebirth',            'Space and Rebirth: The Favored Genius Doctor and Businesswoman',                      'translated'),
		('the favored genius',       'Space and Rebirth: The Favored Genius Doctor and Businesswoman',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False