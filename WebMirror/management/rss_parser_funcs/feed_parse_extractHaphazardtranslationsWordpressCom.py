def extractHaphazardtranslationsWordpressCom(item):
	'''
	Parser for 'haphazardtranslations.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('elf court magician',       'Elf no Kuni no Kyuutei Madoushi ni Naretanode, Toriaezu Himesama ni Seitekina Itazura wo Shitemimashita',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False