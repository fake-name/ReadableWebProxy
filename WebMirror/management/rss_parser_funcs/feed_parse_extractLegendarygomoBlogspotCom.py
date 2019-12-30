def extractLegendarygomoBlogspotCom(item):
	'''
	Parser for 'legendarygomo.blogspot.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('The Land of Gods',                   'The Land of Gods',                                  'oel'),
		('Explosive Flame Artist Ruche',       'Explosive Flame Artist Ruche',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False