def extractNyxtranslationHomeBlog(item):
	'''
	Parser for 'nyxtranslation.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('garbage brave isekai english translation',       'Garbage Brave: Isekai Ni Shoukan Sare Suterareta Yuusha No Fukushuu Monogatari',                      'translated'),
		('blacksmith novel translation',                   'Although it\'s the weakest an unprofitable occupation,『Blacksmith』, has become the strongest. ~Realized he can make anything he wants, the man started his leisurely life~',                      'translated'),
		('evasion healer novel english translation',       'Kanzen Kaihi Healer no Kiseki',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False