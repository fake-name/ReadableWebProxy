def extractWuxiaHeroes(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'preview' in item['title'].lower():
		return None
		
	if 'Blood Hourglass' in item['title']:
		return buildReleaseMessageWithType(item, 'Blood Hourglass', vol, chp, frag=frag, postfix=postfix)
		
		
	tagmap = [
		('The Nine Cauldrons',           'The Nine Cauldrons',               'translated'),
		('Nine Yang Sword Saint',        'Nine Yang Sword Saint',            'translated'),
		('Conquest',                     'Conquest',                         'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('My Father in Law is Lu Bu Chapter',  'My Father in Law is Lu Bu Chapter',   'translated'),
		('Blood Hourglass',                    'Blood Hourglass',                     'translated'),
		('Era of Cultivation: Chapter',        'Era of Cultivation',                  'translated'),
		('Conquest Chapter',                   'Conquest',                            'translated'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


		
	return False