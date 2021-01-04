def extractThat1VillainessWordpressCom(item):
	'''
	Parser for 'that1villainess.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('ibmv',      'I Became the Master of the Villain',                      'translated'),
		('cam',       'The Count and the Maid',                      'translated'),
		('yma',       'Your Majesty is Very Annoying!',                      'translated'),
		('ysr',       'You are the Supporting Role',                      'translated'),
		('pcp',       'Please Cry Prettily',                      'translated'),
		('tpcp',      'The Predator’s Contract Partner',                      'translated'),
		('illyml',    'I Lost the Leash of the Yandere Male Lead',                      'translated'),
		('ba',        'Beloved Angela',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False