def extractStrictlybromanceCom(item):
	'''
	Parser for 'strictlybromance.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('grave robbers\' chronicles',        'grave robbers\' chronicles',                       'translated'),
		('haunted houses\' chronicles',       'haunted houses\' chronicles',                      'translated'),
		('the trial game of life',            'the trial game of life',                           'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False