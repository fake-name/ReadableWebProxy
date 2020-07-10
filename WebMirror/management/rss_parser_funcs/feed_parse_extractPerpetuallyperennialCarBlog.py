def extractPerpetuallyperennialCarBlog(item):
	'''
	Parser for 'perpetuallyperennial.car.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('please don&#039;t eat me',                     'Please Don’t Eat Me',                      'translated'),
		('the villainess needs a tyrant',                'The Villainess Need A Tyrant',                      'translated'),
		('a villain is a good match for a tyrant',       'A Villain Is A Good Match For A Tyrant',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False