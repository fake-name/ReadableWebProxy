def extractRavenbluesdayWordpressCom(item):
	'''
	Parser for 'ravenbluesday.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Counterattack Plan of A Villain With Ten Thousand Fans',       'The Counterattack Plan of A Villain With Ten Thousand Fans',                      'translated'),
		('CPVTTF',                                                           'The Counterattack Plan of A Villain With Ten Thousand Fans',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False