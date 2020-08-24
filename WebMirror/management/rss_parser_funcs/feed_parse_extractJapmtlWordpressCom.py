def extractJapmtlWordpressCom(item):
	'''
	Parser for 'japmtl.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('one day, the engagement was suddenly cancelled. ......my little sister\'s.',       'one day, the engagement was suddenly cancelled. ......my little sister\'s.',                      'translated'),
		('villainess (?) and my engagement cancellation',                                    'villainess (?) and my engagement cancellation',                                                   'translated'),
		('beloved villain flips the skies',                                                  'beloved villain flips the skies',                                                                 'translated'),
		('slow life villainess doesn\'t notice the prince\'s fondness',                      'slow life villainess doesn\'t notice the prince\'s fondness',                                     'translated'),
		('is the villain not allowed to fall in love?',                                      'is the villain not allowed to fall in love?',                                                     'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False