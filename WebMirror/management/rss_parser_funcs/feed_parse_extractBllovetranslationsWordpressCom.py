def extractBllovetranslationsWordpressCom(item):
	'''
	Parser for 'bllovetranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('CDAW',                            'Continuation of the Dream in Another World',                      'translated'),
		('aak',                             'ai wo ataeru kemono-tachi',                      'translated'),
		('ai wo ataeru kemono-tachi',       'ai wo ataeru kemono-tachi',                      'translated'),
		('Sweet Daydream',                  'Sweet Daydream',                                 'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False