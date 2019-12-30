def extractMythoroidtranslationsBlogspotCom(item):
	'''
	Parser for 'mythoroidtranslations.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Nobunaga Cheat',       'Oda Nobunaga Toyuu Nazo no Shokugyou ga Mahou Kenshi yori Cheat datta node, Oukoku wo Tsukuru Koto ni Shimashita',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False