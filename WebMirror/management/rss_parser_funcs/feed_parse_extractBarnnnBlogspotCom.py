def extractBarnnnBlogspotCom(item):
	'''
	Parser for 'barnnn.blogspot.com'
	'''
	
	if 'Voice Drama' in item['tags']:
		return None

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None
	if 'Lower Bound Volume' in item['title'] and vol is None:
		vol = 2
	if 'Upper Bound Volume' in item['title'] and vol is None:
		vol = 1

	tagmap = [
		('yuri in which the world will end in ten days',       'yuri in which the world will end in ten days',                      'translated'),
		('Monster Hunter: Cross Soul',       'Monster Hunter: Cross Soul',                      'translated'),
		('The Girl Who Ate The Death God',   'The Girl Who Ate The Death God',                  'translated'),
		('kino\'s journey',                  'Kino\'s Journey',                                 'translated'),
		('Cross Road',                       'Cross Road: In Their Cases',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False