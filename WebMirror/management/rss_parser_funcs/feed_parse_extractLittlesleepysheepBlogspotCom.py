def extractLittlesleepysheepBlogspotCom(item):
	'''
	Parser for 'littlesleepysheep.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('transmigrated to another world where only men exist～bl isn\'t allowed!～',       'Transmigrated to Another World Where Only Men Exist ～BL isn\'t allowed!～',        'translated'),
		('this cannon fodder is covered by me!',                                            'This Cannon Fodder is Covered by Me!',                                              'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False