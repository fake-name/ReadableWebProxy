def extractWorkNwongNet(item):
	'''
	Parser for 'work.nwong.net'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('Poison-Wielding Fugitive',                        'Poison-Wielding Fugitive',                                       'translated'),
		('I Said Make My Abilities Average!',               'I Said Make My Abilities Average',                               'translated'),
		('I Said Make My Abilities Average',                'I Said Make My Abilities Average',                               'translated'),
		('Head Over Heels from the Scarf I Lent Her',       'Head Over Heels from the Scarf I Lent Her',                      'translated'),
		('Dimension Wave',                                  'Dimension Wave',                                                 'translated'),
		('Crowbar Nurse',                                   'Crowbar Nurse',                                                  'translated'),
		('PRC',       'PRC',                      'translated'),
		('Loiterous', 'Loiterous',                'oel'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False