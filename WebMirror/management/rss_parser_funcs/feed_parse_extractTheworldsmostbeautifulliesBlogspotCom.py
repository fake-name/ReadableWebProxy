def extractTheworldsmostbeautifulliesBlogspotCom(item):
	'''
	Parser for 'theworldsmostbeautifullies.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Under The Plum Blossom',   'Under The Plum Blossom',                  'translated'),
		('The Elixir of Life',       'The Elixir of Life',                      'translated'),
		('Beseeching Love',          'Beseeching Love',                         'translated'),
		('2:30 am',                  '2:30 am',                                 'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False