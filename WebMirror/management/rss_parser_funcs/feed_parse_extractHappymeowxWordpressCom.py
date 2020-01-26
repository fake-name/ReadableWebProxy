def extractHappymeowxWordpressCom(item):
	'''
	Parser for 'happymeowx.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('generous poor & really stingy',       'generous poor & really stingy',          'translated'),
		('heart has ling xi',                   'Heart has Ling Xi',                      'translated'),
		('your husband\'s leg is broken',       'Your Husband\'s Leg is Broken',          'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False