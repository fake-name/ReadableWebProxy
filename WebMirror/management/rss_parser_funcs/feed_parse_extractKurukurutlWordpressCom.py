def extractKurukurutlWordpressCom(item):
	'''
	Parser for 'kurukurutl.wordpress.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return None

	tagmap = [
		('I reincarnated, but I think the Prince (fiancé) has given up',       'I reincarnated, but I think the Prince (fiancé) has given up',                      'translated'),
		('Kedama wo hirotte 10 nen tattara',                                   'Kedama wo hirotte 10 nen tattara',                                                  'translated'),
		('Kedama hirotte 10 nen tattara',                                      'Kedama wo hirotte 10 nen tattara',                                                  'translated'),
		('Mahoutsukai no Konyakusha',                                          'Mahoutsukai no Konyakusha',                                                         'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			if 'Kedama wo hirotte 10 nen tattara' in item['tags'] and chp == 10:
				return None
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

	titlemap = [
		('Mahoutsukai no Konyakusha',                                          'Mahoutsukai no Konyakusha',                                                         'translated'),
		('I reincarnated, but I think the Prince (fiancé) has given up',       'I reincarnated, but I think the Prince (fiancé) has given up',                      'translated'),
		('Kedama hirotte 10 nen tattara',                                      'Kedama hirotte 10 nen tattara',                                                     'translated'),
		('Tensei Shoujo no Rirekisho',  'Tensei Shoujo no Rirekisho',      'translated'),
		('Master of Dungeon',           'Master of Dungeon',               'oel'),
	]

	for titlecomponent, name, tl_type in titlemap:
		if titlecomponent.lower() in item['title'].lower():
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)


	return False