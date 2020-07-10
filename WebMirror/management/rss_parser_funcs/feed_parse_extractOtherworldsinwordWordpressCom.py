def extractOtherworldsinwordWordpressCom(item):
	'''
	Parser for 'otherworldsinword.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('riad',                              'The Roommates Were Ecstatic to See Their Roommate in a Dress',                      'translated'),
		('bwc',                               'the boss wants to be coaxed',                      'translated'),
		('the boss wants to be coaxed',       'the boss wants to be coaxed',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False