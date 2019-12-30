def extractSporadicsporesBlogspotCom(item):
	'''
	Parser for 'sporadicspores.blogspot.com'
	'''
	
	if 'Songs' in item['tags']:
		return None

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Chairman Husband Too Boorish',             'Chairman Husband Too Boorish',                            'translated'),
		('Heartbeat at the Tip of the Tongue',       'Heartbeat at the Tip of the Tongue',                      'translated'),
		('Love O2O',                                 'Love O2O',                                                'translated'),
		('Heart Protection',                         'Heart Protection',                                        'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False