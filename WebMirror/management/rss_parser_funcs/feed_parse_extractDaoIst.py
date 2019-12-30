def extractDaoIst(item):
	'''
	Parser for 'dao.ist'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('zombie master',                            'Zombie Master',                         'translated'),
		('Master\'s Smile',                          'Master\'s Smile',                       'translated'),
		('I became the Villainess’s Brother',        'I became the Villainess\'s Brother',    'translated'), 
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False