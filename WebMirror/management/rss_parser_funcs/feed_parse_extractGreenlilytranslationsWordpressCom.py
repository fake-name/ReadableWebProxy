def extractGreenlilytranslationsWordpressCom(item):
	'''
	Parser for 'greenlilytranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('MDWTTMED',       'My Disciple Wants to Tease Me Every Day',                      'translated'),
		('SVSSS',          'Scum Villain’s Self Saving System',                            'translated'),
		('ncpe',           'The Noble Consort’s Pet Empress',                              'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False