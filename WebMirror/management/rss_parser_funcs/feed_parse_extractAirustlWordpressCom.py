def extractAirustlWordpressCom(item):
	'''
	Parser for 'airustl.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('my seatmate tries to make me fall in love with her by teasing me repeatedly, but somehow she was the one who fell',       'my seatmate tries to make me fall in love with her by teasing me repeatedly, but somehow she was the one who fell',                      'translated'),
		('i want to confess to my childhood friend',                                                                                'i want to confess to my childhood friend',                                                                                               'translated'),
		('venomous tongue',                                                                                                         'I Quit the Going-Home Club for a Girl with a Venomous Tongue',                                                                           'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False