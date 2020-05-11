def extractAswTenanBlogspotCom(item):
	'''
	Parser for 'asw-tenan.blogspot.com'
	'''
	if 'English' not in item['tags']:
		return None
	if 'Bahasa Indonesia' in item['tags']:
		return None

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('mushoku no eiyuu',       'Mushoku no Eiyuu ~Betsu ni Skill Nanka Iranakattan daga~',                      'translated'),
		('s-rank girls',           'S Rank Boukensha de aru Ore no Musume-tachi wa Juudo no Father Con deshita',    'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False