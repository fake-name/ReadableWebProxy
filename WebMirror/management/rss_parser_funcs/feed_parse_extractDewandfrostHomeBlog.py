def extractDewandfrostHomeBlog(item):
	'''
	Parser for 'dewandfrost.home.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('I Have Amnesia, Don\'t Be Noisy!',       'I Have Amnesia, Don\'t Be Noisy!',                      'translated'),
		('holy institution',                       'holy institution',                                      'translated'),
		('don\'t discriminate against species',    'Don’t Discriminate Against Species',                      'translated'),
		('speciesism is not allowed',              'Don\'t Discriminate Against Species',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False