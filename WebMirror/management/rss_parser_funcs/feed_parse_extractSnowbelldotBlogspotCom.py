def extractSnowbelldotBlogspotCom(item):
	'''
	Parser for 'snowbelldot.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Cold King',                            'Cold King, the Doctor Fei Is Running Away',                      'translated'),
		('the Doctor Fei Is Running Away',       'Cold King, the Doctor Fei Is Running Away',                      'translated'),
		('Wife’s Color is Addicting',            'Wife\'s Color is Addicting',                                     'translated'),
		('PRC',                                  'PRC',                      'translated'),
		('Loiterous',                            'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False