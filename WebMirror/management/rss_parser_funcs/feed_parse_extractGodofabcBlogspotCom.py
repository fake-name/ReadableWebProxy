def extractGodofabcBlogspotCom(item):
	'''
	Parser for 'godofabc.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('RE:Yandere',                                          'RE:Yandere',                                                         'translated'),
		('Synthesis',                                           'Synthesis',                                                          'translated'),
		('These Dangerous Girls Placed Me Into Jeopardy',       'These Dangerous Girls Placed Me Into Jeopardy',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False