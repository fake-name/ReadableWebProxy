def extractXiaxuenovelsWordpressCom(item):
	'''
	Parser for 'xiaxuenovels.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Bleach: Secret Intentions',                                        'Bleach: Secret Intentions',                                                        'translated'),
		('The Black Technology Chat Group of the Ten Thousand Realms',       'The Black Technology Chat Group of the Ten Thousand Realms',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False