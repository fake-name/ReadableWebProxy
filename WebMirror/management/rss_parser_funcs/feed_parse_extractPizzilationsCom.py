def extractPizzilationsCom(item):
	'''
	Parser for 'pizzilations.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Liu Yao',                                  'Liu Yao: The Revitalization of Fuyao Sect',               'translated'),
		('Scum Villain\'s Self-Saving System',       'Scum Villain\'s Self-Saving System',                      'translated'),
		('Feng Yu Jiu Tian',                         'Feng Yu Jiu Tian',                                        'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False