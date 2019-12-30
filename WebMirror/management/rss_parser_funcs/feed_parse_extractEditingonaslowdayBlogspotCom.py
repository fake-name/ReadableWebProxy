def extractEditingonaslowdayBlogspotCom(item):
	'''
	Parser for 'editingonaslowday.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Rebirth on the Doors to the Civil Affairs Bureau',       'Rebirth on the Doors to the Civil Affairs Bureau',                      'translated'),
		('Slowly Falling For Changkong',                           'Slowly Falling For Changkong',                                          'translated'),
		('please confess to me [rebirth]',                         'please confess to me [rebirth]',                                        'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False