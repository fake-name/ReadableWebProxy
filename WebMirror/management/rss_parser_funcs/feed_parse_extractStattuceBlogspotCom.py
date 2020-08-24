def extractStattuceBlogspotCom(item):
	'''
	Parser for 'stattuce.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('(陪你十三年) with you for thirteen years (eng',       'With you for thirteen years',                      'translated'),
		('(伪装下的爱) love in disguise (eng)',       'love in disguise',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False