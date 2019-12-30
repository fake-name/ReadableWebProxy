def extractDiwasteman(item):
	"""

	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or 'commentary' in item['title'].lower():
		return False
		
	tagmap = [
		('Parameter remote controller',      'Parameter remote controller',                  'translated'),
		('maou no hajimekata',               'Maou no Hajimekata',                           'translated'),
		('Is my reality a love game??',      'Is my reality a love game??',                  'translated'),
		('Ero Gacha',                        'Ero Gacha',                                    'translated'),
		('Women gather in a cheap house',    'The Gathering of Women in a Cheap House',      'translated'),
	]

	for tagname, name, tl_type in tagmap:
		if tagname in item['tags']:
			return buildReleaseMessageWithType(item, name, vol, chp, frag=frag, postfix=postfix, tl_type=tl_type)

		
	return False