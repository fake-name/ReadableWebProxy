def extractAurarealmCom(item):
	'''
	Parser for 'aurarealm.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp is not None or vol is not None) or "preview" in item['title'].lower():
		return False


	tagmap = [
		('Dragon Blood Warrior',       'Dragon Blood Warrior',                      'translated'),
		('Against the Fate',           'Against the Fate',                          'translated'),
		('Almighty Student',           'Almighty Student',                          'translated'),
		('Hell\'s Cinema',             'Hell\'s Cinema',                            'translated'),
		('Noire de Plaisir',           'Noire de Plaisir ~ Pleasure Training of the Fallen Vampire Princess~',                      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False