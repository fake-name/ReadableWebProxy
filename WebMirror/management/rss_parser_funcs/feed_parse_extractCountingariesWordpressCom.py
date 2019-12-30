def extractCountingariesWordpressCom(item):
	'''
	Parser for 'countingaries.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('HCTCTM',                               'How Could This Cat Tease Me?',                        'translated'),
		('Scholar…I Don\'t Want Any…Meow',       'Scholar…I Don\'t Want Any…Meow',                      'translated'),
		('AUP',                                  'Appreciation of Unconventional Plants',               'translated'),
		('LCU',                                  'The Last Cat in the Universe',                        'translated'),
		('QTSGF',                                'Quick Transmigration: Snatching Golden Fingers',      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False