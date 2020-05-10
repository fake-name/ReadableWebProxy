def extractPbtlsWordpressCom(item):
	'''
	Parser for 'pbtls.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('ore wo suki',            'Ore wo Suki Nano wa Omae Dake ka yo',                      'translated'),
		('ore wo suki nano',       'Ore wo Suki Nano wa Omae Dake ka yo',                      'translated'),
		('bocchi no kanojo',       'Bocchi no Kanojo',                                         'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False