def extractDeltatranslationsOrg(item):
	'''
	Parser for 'deltatranslations.org'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Summoning the Holy Sword',        'Summoning the Holy Sword',                       'translated'), 
		('King of Mercenaries',             'King of Mercenaries',                            'translated'), 
		('For a Prosperous World',          'For a Prosperous World',                         'translated'), 
		('Battle of the Third Reich',       'Battle of the Third Reich',                      'translated'), 
		('EDSG',                            'Eight Desolate Sword God',                       'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False