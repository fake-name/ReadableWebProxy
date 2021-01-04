def extractBeanylandCom(item):
	'''
	Parser for 'beanyland.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('fight for love and peace',                'Fight for Peace and Love',                               'translated'),
		('i’m bearing my love rival’s child',       'i’m bearing my love rival’s child',                      'translated'),
		('turn on the love system',                 'turn on the love system',                                'translated'),
		('crossing to the primitive',               'crossing to the primitive',                              'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False