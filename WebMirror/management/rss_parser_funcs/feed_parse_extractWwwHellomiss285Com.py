def extractWwwHellomiss285Com(item):
	'''
	Parser for 'www.hellomiss285.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('diotev',       'Death Is The Only Ending for The Villainess',                      'translated'),
		('isbmdc',       'I\'m Only Stepmother But My Daughter Just Too Cute',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False