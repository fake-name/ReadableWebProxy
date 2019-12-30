def extractIsogashiineetoWordpressCom(item):
	'''
	Parser for 'isogashiineeto.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('NEET Hello Work',       'NEET dakedo Hello Work ni Ittara Isekai ni Tsuretekareta',                      'translated'),
		('Dark Magician Hero',    'Dark Magician as a Hero',                                                       'translated'),
		('Hatena☆Illusion',      'Hatena☆Illusion',                                                               'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False