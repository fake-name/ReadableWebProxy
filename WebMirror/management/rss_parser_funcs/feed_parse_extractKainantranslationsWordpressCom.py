def extractKainantranslationsWordpressCom(item):
	'''
	Parser for 'kainantranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Redemption of The Blue Rose Princess',       'Redemption of The Blue Rose Princess',                      'translated'),
		('I\'ll Live My Second Life!',                 'I\'ll Live My Second Life!',                                'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False