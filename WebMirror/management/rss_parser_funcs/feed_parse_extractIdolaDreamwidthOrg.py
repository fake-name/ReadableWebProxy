def extractIdolaDreamwidthOrg(item):
	'''
	Parser for 'idola.dreamwidth.org'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('the legend of the legendary heroes',       'densetsu no yuusha no densetsu',                      'translated'),
		('densetsu no yuusha no densetsu',           'densetsu no yuusha no densetsu',                      'translated'),
		('the legend of the fallen black hero',       'the legend of the fallen black hero',                      'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False