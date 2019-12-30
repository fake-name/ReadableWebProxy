def extractAshtranslationsWordpressCom(item):
	'''
	Parser for 'ashtranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Someone Explain This Situation!',              'Someone Explain This Situation!',                      'translated'),
		('Someone Please Explain This Situation!',       'Someone Explain This Situation!',                      'translated'),
		('PRC',                                          'PRC',                                                  'translated'),
		('Loiterous',                                    'Loiterous',                                            'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False