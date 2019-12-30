def extractJamesParkMe(item):
	'''
	Parser for 'james-park.me'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Tutorial Is Too Hard',       'The Tutorial Is Too Hard',                      'translated'),
		('Sword Whisperer',                'Sword Whisperer',                               'translated'),
		('GOM',                            'God of Music',                                  'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False