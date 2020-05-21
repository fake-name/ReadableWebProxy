def extractJunktranslatesWordpressCom(item):
	'''
	Parser for 'junktranslates.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('intl',       'It’s Not Too Late to Meet Again After Rebirth',                      'translated'),
		('smwom',      'Second Marriage of a Wealthy Old Man',                      'translated'),
		('rolm',       'Reborn Out of Love and Murder',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False