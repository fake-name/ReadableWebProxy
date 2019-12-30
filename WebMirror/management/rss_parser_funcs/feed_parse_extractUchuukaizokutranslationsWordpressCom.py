def extractUchuukaizokutranslationsWordpressCom(item):
	'''
	Parser for 'uchuukaizokutranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('ballistic weaponry',       'Me, Her, and the Ballistic Weaponry [Antique]',                      'translated'),
		('kochugunshikan boukensha ni naru',       'Kochugunshikan Boukensha ni Naru',                      'translated'),
		('i woke up piloting the strongest starship, so i became a space mercenary',       'I Woke Up Piloting the Strongest Starship, so I Became a Space Mercenary',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False