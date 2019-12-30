def extractInsanitycavePoetryBlog(item):
	'''
	Parser for 'insanitycave.poetry.blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('hollywood hunter',                              'hollywood hunter',                               'translated'),
		('almighty game designer',                        'almighty game designer',                         'translated'),
		('mediterranean hegemon of ancient greece',       'Mediterranean Hegemon of Ancient Greece',        'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False