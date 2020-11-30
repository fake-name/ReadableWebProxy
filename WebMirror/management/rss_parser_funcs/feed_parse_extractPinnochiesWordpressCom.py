def extractPinnochiesWordpressCom(item):
	'''
	Parser for 'pinnochies.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('reslw',       'Rebirth to Eighties : Shrewd Little Wife',                      'translated'),
		('atswm',       'After Transmigrating into a Short-lived White Moonlight, had a HE with the Villain',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False