def extractChaspoilerishtranslationsWordpressCom(item):
	'''
	Parser for 'chaspoilerishtranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('I heard you are an alien',              'I heard you are an alien',                             'translated'),
		('Different World Business Symbol',       'Different World Business Symbol',                      'translated'),
		('I\'m Not Shouldering This Blame',       'I\'m Not Shouldering This Blame',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False