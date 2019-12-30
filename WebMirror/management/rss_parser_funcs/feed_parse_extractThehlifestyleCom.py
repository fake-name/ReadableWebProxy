def extractThehlifestyleCom(item):
	'''
	Parser for 'thehlifestyle.com'
	'''
	
	tstr = str(item['tags']).lower()
	if 'review' in tstr:
		return None
	if 'actors' in tstr:
		return None
	if 'game' in tstr:
		return None

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Beloved Imperial Consort translation',       'The Beloved Imperial Consort',                      'translated'),
		('Good Morning, Miss Undercover Translation',      'Good Morning, Miss Undercover',                     'translated'),
		('Hilarous Pampered Consort Translation',          'Hilarous Pampered Consort',                         'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False