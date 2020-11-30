def extractPerpetualdaydreamsCom(item):
	'''
	Parser for 'perpetualdaydreams.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('iwal',       'I Won a Lottery So I Moved to the Other World',                      'translated'),
		('fpyq',       'Fei Pin Ying Qiang',                      'translated'),
		('TYQHM',      'Those Years in Quest of Honor Mine',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False